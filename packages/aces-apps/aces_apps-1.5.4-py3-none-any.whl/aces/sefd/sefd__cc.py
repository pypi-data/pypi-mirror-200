from __future__ import print_function

"""
A class providing a standard estimation of the System Equivalent FLux Density for Beta data files
taken on the source B1934-638.
"""

__author__ = 'Dave McConnell <david.mcconnell@csiro.au>'

import logging
import numpy as np
import os
import re
import time
import logging
import pickle
import aces.sefd.ASKAP_msdata__cc as akms
import aces.sefd.flux_of_1934 as fl
from aces.beamset.sefdset import SEFDSet
from aces.askapdata.schedblock import SchedulingBlock
import Ice

import itertools
from numpy.fft import rfft2

import matplotlib as mpl

mpl.use('Agg')  # this line must precede pylab import to suppress display
import matplotlib.pylab as plt  # noqa

logger = logging.getLogger(__name__)

pols = [0, 1, 2, 3]
pi = np.pi

antrel01 = np.array([[0.000, 0.000],
                     [26.978, -13.011],
                     [35.950, 7.490],
                     [-8.979, 35.008],
                     [-73.992, 31.503],
                     [135.660, 112.000],
                     [242.860, -109.980],
                     [-37.810, -238.510],
                     [-244.210, 110.550],
                     [-96.316, 279.496],
                     [267.951, 340.539],
                     [395.925, 269.476],
                     [438.720, -364.005],
                     [-24.860, -460.009],
                     [-739.700, -157.993],
                     [-636.115, 365.440],
                     [-496.818, 522.519],
                     [-106.785, 375.509],
                     [217.814, 481.520],
                     [506.320, 315.027],
                     [686.168, 322.006],
                     [845.840, 335.982],
                     [-0.708, -657.007],
                     [78.472, -978.523],
                     [-613.617, 653.507],
                     [-393.336, 667.503],
                     [-1070.503, 940.975],
                     [249.765, 1198.511],
                     [565.930, 753.210],
                     [1229.056, 798.468],
                     [2220.949, 992.985],
                     [3024.925, -2507.046],
                     [25.026, -2810.965],
                     [-2975.009, -2006.978],
                     [-2170.998, 992.991],
                     [23.232, 3190.068]])

ASKAP_antennas = range(1, 37)


class ASKAP_array(object):
    def __init__(self, name):
        self.name = name
        if name == "ASKAP":
            self.arrayAntennas = ASKAP_antennas
        else:
            logger.info('ASKAP_array: Unknown name %s' % name)
            self.arrayAntennas = []
        self.antennas = [a for a in self.arrayAntennas]
        self.baselines = []
        self.gen_baselines()

    def select_antennas(self, antennas):
        self.antennas = [a for a in self.arrayAntennas if a in antennas]
        self.gen_baselines()

    def gen_baselines(self):
        ants = self.antennas
        n_ants = len(self.antennas)
        temp = [['%dx%d' % (ants[j], ants[i]) for i in range(j + 1, n_ants)] for j in range(n_ants)]
        self.baselines = list(itertools.chain.from_iterable(temp))

    def get_ant_names(self):
        ret = ["AK%02d" % a for a in self.antennas]
        return ret


def baseline_2vec(bas):
    a1, a2 = map(int, bas.split('x'))
    vec = antrel01[a1 - 1] - antrel01[a2 - 1]
    return vec


def baseline_2v(a1, a2):
    vec = antrel01[a1 - 1] - antrel01[a2 - 1]
    return vec


def baseline_len(a1, a2):
    vec = antrel01[a1 - 1] - antrel01[a2 - 1]
    return np.sqrt((vec * vec).sum())


def antenna_decompose(products, arr, b_flg):
    # compute antenna specific quantities from the set of n(n-1)/2 products
    # Input products[0:nBas,0:M,0:N] is a n(n-1)/2 entry dictionary, each being an array (could be
    #  M frequency channels and N time samples
    # b_flg - an array of length nBas; value zero to ignore corresponding baseline

    # 1. Set up the coefficients
    nb = len(arr.baselines)
    n_ants = len(arr.antennas)
    ants = arr.antennas
    A = np.zeros([nb, n_ants])
    ki = 0
    k = []
    for i in range(1, n_ants):
        k.append(ki)
        ki += n_ants - i

    for i in range(n_ants):
        for j in range(i + 1, n_ants):
            row = k[i] + j - 1 - i
            A[row][i] = 1 * b_flg[row]
            A[row][j] = 1 * b_flg[row]

    # 2. For each frequency, compute the dependent variable vectors
    bass = []
    ib, ibas = 0, []
    for i in range(n_ants):
        for j in range(i + 1, n_ants):
            bass.append("%dx%d" % (ants[i], ants[j]))
            ibas.append(ib)
            ib += 1

    M = products.shape[1]
    N = products.shape[2]
    result = np.zeros([n_ants, M, N])
    for t in range(N):
        for f in range(M):
            b = products[:, f, t]
            b = np.ma.masked_array(b, np.isinf(b))
            if b.count() > 4:
                Am = 1.0 - np.tile(np.ones(nb) * b.mask, (n_ants, 1)).transpose()
                ba = np.log(b)
                x, res, rnk, sv = np.linalg.lstsq(A * Am, ba)
                result[:, f, t] = np.exp(2 * x)
    return result


def find_factor(n_avg):
    # Find a number nearby that divides 16416. Here is a list of those allowed numbers
    factors = [1, 2, 3, 4, 6, 8, 9, 12, 16, 18, 19, 24, 27, 32, 36, 38, 48, 54]
    n_avg = n_avg
    n_avg = max(n_avg, factors[0])
    n_avg = min(n_avg, factors[-1])
    if n_avg not in factors:
        j = 0
        while n_avg > factors[j]:
            j += 1
        n_avg = factors[j - 1]
    return n_avg


def box_mean(x, n):
    xsh = x.shape
    assert xsh[0] % n == 0
    m = xsh[0] / n
    if len(xsh) == 2:
        newshape = (m, n, xsh[1])
    else:
        newshape = (m, n)
    ret = np.reshape(x, newshape).mean(axis=1)
    return ret


def delfunc(x, f, t, z):
    ph = (0.0 + 1.0j) * 2.0 * pi * (f * x[0] + t * x[1])
    fval = (z * np.exp(ph)).std()
    return fval


class SEFD(object):
    # Define a class to compute and hold SEFD values from visibilities.
    # Allow values to be computed over df x dt cells, defined as dCH, dTi (frequency channels, integration times)
    # and to span a total frequency and time range.
    # In frequency  : dch, ch0, ncF  results in ncF frequency cells, each of dCH channels, starting at channel ch0
    # In time       : dt, tstart, ncT results in ncT time cells, each of dt integration cycles, starting at integration
    #                  cycle tstart in the chosen scan.
    def __init__(self, sbid, file_name=None, mset_inx=0,
                 dch=1, ch0=0, ncf=0, scan=-1, dnt=120,
                 nstart=3, nct=0,
                 uvmin=0.0):
        # Expects:
        # sbid      sched block ID
        # file_name  ms name; if None, work it out from sbid and arr: assume usual archive position
        # mset_inx  mset index
        # dch       frequency cell width in channels
        # chan0     start freq chan number
        # ncF       number of frequency cells; as many as possible if  ncF = 0
        # scan      scan number: if illegal, use the beam number assuming the standard calibration sequence.
        # dnt       time cell width in cycles
        # nstart    start at this integration cycle number
        # nct       number of time cells; as many as possible if nct = 0
        self.sbid = sbid
        self.mset_inx = mset_inx
        self.array = ASKAP_array('ASKAP')
        arr = self.array

        if file_name is not None:
            self.fname = file_name
        else:
            self.fname = akms.get_msname(self.sbid, tele=arr.name, mset_inx=self.mset_inx)
        d = akms.MSData(self.fname)
        self.beam = d.get_beam_id()
        arr.select_antennas(d.ants)

        self.dch = dch
        self.ch0 = ch0

        # fix channel cell details:
        nc_fmax = (d.n_chans - self.ch0) / self.dch
        if ncf == 0:
            self.ncf = nc_fmax
        else:
            self.ncf = min(nc_fmax, ncf)
        self.nChans = int(self.ncf * self.dch)

        # fix time cell details
        if scan >= 0:
            self.scan = scan
        else:
            self.scan = self.beam
        self.times, self.del_t = d.get_time(self.scan)
        self.nt = len(self.times)
        # Limit dnt (2016/10/11)
        self.dnt = min(self.nt - nstart, dnt)
        self.dt = self.dnt * self.del_t
        self.rel_t_start = nstart * self.del_t
        nc_tmax = int((self.times[-1] - (self.times[0] + self.rel_t_start)) / self.dt)
        if nc_tmax == 0:
            nc_tmax = 1
        if nct == 0:
            self.nct = nc_tmax
        else:
            self.nct = min(nc_tmax, nct)
        self.relTstop = self.rel_t_start + self.nct * self.dt
        self.rTstarts = np.arange(self.rel_t_start, self.relTstop, self.dt)

        self.btau = 2.0 * d.get_ch_bw() * self.del_t

        self.uvmin = uvmin
        self.baselines = d.baselines
        self.basants = [list(map(int, bas.split('x'))) for bas in self.baselines]
        self.dataset = d
        self.scratch = []
        self.good_antennas = []
        self.good_baselines = []
        self.sefd = {}
        self.scale = {}
        self.freq = {}
        self.time = {}
        self.sefd_per_ant = {}
        self.scale_per_ant = {}
        self.raw_ampl_per_ant = {}
        self.automean = {}
        self.autostd = {}
        self.nflags = {}
        self.b_flags = {}
        self.meta = self.get_meta()
        self.difference = 'none'

    def summary(self):
        logger.info("SBID : %d   Beam  : %d   Scan : %d" % (self.sbid, self.beam, self.scan))
        logger.info("Integration cells %d x %d (channels x cycles)" % (self.dch, self.dnt))
        cell_wid = self.dch * self.dataset.get_ch_bw() * 1.0e-6
        logger.info("Cell width      %7.4f MHz" % cell_wid)
        logger.info("Cell duration   %7.1f s" % self.dt)
        logger.info("%d x %d = %d integration cells" % (self.ncf, self.nct, self.ncf * self.nct))
        logger.info("Btau = %8.1f" % self.btau)
        logger.info("ms read: %d chans from %d" % (self.nChans, self.ch0))
        logger.info("Length: %6.1f s " % self.dt)

    def calc_sefd(self, difference='none'):
        """

        :param difference: Options are 'none', 'time', 'frequency'
        """
        n_avg = self.dch
        d = self.dataset
        c0, c1 = self.ch0, self.ch0 + self.nChans
        freq = d.chan_freq[c0:c1] * 1.0e-6
        if n_avg > 1:
            freq = box_mean(freq, n_avg)

        bintim = []
        btau = self.btau
        flux1934 = fl.flux_of_1934(freq)
        ssys = {}
        scale = {}
        raw_ampl = {}
        auto_mean = {}
        auto_std = {}
        nflags = {}
        uv_flags = {}
        for ipol in [0, 1, 2, 3]:
            ssys[ipol] = {}
            scale[ipol] = {}
            auto_mean[ipol] = {}
            auto_std[ipol] = {}
            nflags[ipol] = {}
            for bas, basants in zip(self.baselines, self.basants):
                ba = basants
                if ba[0] != ba[1]:
                    ssys[ipol][bas] = []
                    scale[ipol][bas] = []
                    nflags[ipol][bas] = []
                else:
                    auto_mean[ipol][ba[0]] = []
                    auto_std[ipol][ba[0]] = []
        ##########
        logger.info('Reading data: ')
        self.scratch = []
        ant_ok = []
        for i, ti in enumerate(self.rTstarts):
            need_time = True
            logger.info('Reading data: times %5.1f to %5.1f...' % (ti, ti + self.dt))
            vis, uvw = d.get_data_w(self.beam, self.nChans, self.ch0, scan=self.scan, start=ti, n_sec=self.dt)
            uvd = np.sqrt(uvw[:, 0] ** 2 + uvw[:, 1] ** 2)
            
            for bi, bas in enumerate(self.baselines):
                sb = self.basants[bi]
                if uvd[bi] > self.uvmin:
                    uv_flags[bas] = 1
                else:
                    uv_flags[bas] = 0
                if sb[0] != sb[1]:
                    if bool(vis[:, :, :, bi].any()):
                        if need_time:
                            bintim.append(ti + 0.5 * self.dt)
                            need_time = False
                        ant_ok += sb
                        ipol = 0
                        z = vis[ipol, :, :, bi]
                        scalebx = bl_scales(n_avg, z, flux1934)
                        ssysb = bl_noise(z, scalebx, btau, n_avg, difference)
                        scale[ipol][bas].append(scalebx)
                        ssys[ipol][bas].append(ssysb)
                        nflags[ipol][bas].append(np.ma.count_masked(z))

                        ipol = 3
                        z = vis[ipol, :, :, bi]
                        scaleby = bl_scales(n_avg, z, flux1934)
                        ssysb = bl_noise(z, scaleby, btau, n_avg, difference)
                        scale[ipol][bas].append(scaleby)
                        ssys[ipol][bas].append(ssysb)
                        nflags[ipol][bas].append(np.ma.count_masked(z))

                        scalebxy = np.sqrt(scalebx * scaleby)
                        for ipol in [1, 2]:
                            z = vis[ipol, :, :, bi]
                            ssysb = bl_noise(z, scalebxy, btau, n_avg, difference)
                            scale[ipol][bas].append(scalebxy)
                            ssys[ipol][bas].append(ssysb)
                            nflags[ipol][bas].append(np.ma.count_masked(z))
                    else:
                        logger.info("%s masked count = %d  count = %d" % (bas, np.ma.count_masked(vis), np.ma.count(vis)))
                else:
                    # these are the autocorrelations
                    if bool(vis[:, :, :, bi].any()):
                        for ipol in [0, 3]:
                            z = vis[ipol, :, :, bi]
                            auto_mean[ipol][sb[0]].append(np.real(z).mean(axis=1))
                            auto_std[ipol][sb[0]].append(np.real(z).std(axis=1))

        for bi, bas in enumerate(self.baselines):
            sb = self.basants[bi]
            if sb[0] != sb[1]:
                for ip in pols:
                    if len(ssys[ip][bas]) == 0:
                        del ssys[ip][bas]

        mint = min([len(ssys[0][bas]) for bas in ssys[0].keys()])
        for ip in pols:
            for bas in ssys[ip].keys():
                tmp = np.ma.masked_array(ssys[ip][bas])
                ssys[ip][bas] = np.swapaxes(tmp[:mint, :], 0, 1)
                tmp = np.ma.masked_array(scale[ip][bas])
                scale[ip][bas] = np.swapaxes(tmp[:mint, :], 0, 1)
            # for a in auto_mean[ip].keys():
            #     tmp = np.ma.masked_array(auto_mean[ip][a])
            #     auto_mean[ip][a] = np.swapaxes(tmp[:mint,:],0,1)
            #     tmp = np.ma.masked_array(auto_std[ip][a])
            #     auto_std[ip][a] = np.swapaxes(tmp[:mint,:],0,1)

        ant_ok = sorted(list(set(ant_ok)))
        self.good_antennas = ant_ok
        arr = self.array
        arr.select_antennas(ant_ok)
        self.good_baselines = arr.baselines
        logger.info("Found good antennas %s" % self.good_antennas)

        self.sefd = ssys
        self.scale = scale
        self.freq = freq
        self.time = bintim
        self.sefd_per_ant = ssys
        self.scale_per_ant = scale
        self.raw_ampl_per_ant = raw_ampl
        self.automean = auto_mean
        self.autostd = auto_std
        self.nflags = nflags
        self.b_flags = uv_flags
        self.difference = difference

    def decompose(self, what="SEFD"):
        ants = self.good_antennas
        good_array = ASKAP_array(self.array.name)
        good_array.select_antennas(ants)
        if what == "SEFD":
            prod = self.sefd
            lpols = pols
        elif what == "SCALE":
            prod = self.scale
            lpols = [0, 3]
        else:
            raise ValueError('Unrecognised argument %s' % what)

        what_per_ant = decomp(prod, lpols, good_array, self.b_flags)

        if what == "SEFD":
            self.sefd_per_ant = what_per_ant
        elif what == "SCALE":
            self.scale_per_ant = what_per_ant
        elif what == "RAWAMPL":
            self.raw_ampl_per_ant = what_per_ant

    def compare(self, other):
        comparison = {}
        for k1 in self.sefd_per_ant.keys():
            comparison[k1] = {}
            for k2 in self.sefd_per_ant[k1].keys():
                comparison[k1][k2] = other.sefd_A[k1][k2] / self.sefd_per_ant[k1][k2]
        return comparison

    def save_pickle(self, file_name):
        parcel = {"SBID": self.sbid,
                  "META": self.meta,
                  "FLAGS": self.nflags,
                  "FREQ": self.freq,
                  "TIME": self.time,
                  "SEFD": self.sefd_per_ant,
                  "SCALE": self.scale_per_ant,
                  "AUTOM": self.automean,
                  "AUTOS": self.autostd}
        # "RAWAMPL":self.raw_ampl_per_ant,
        # "SCRATCH":self.scratch}
        pickle.dump(parcel, open("%s.pkl" % file_name, 'w'))
        logger.info("SEFD_A saved to {}.pkl".format(file_name))

    def save_hdf5(self, file_name, per_ant=True):
        # Save the SEFD data as an hdf5 file in the "beamset" format.
        # This defines an array with five dimensions: time, ant, beam, pol, frq
        # and in this case assigns a payload of one float to each point in the grid.
        # It will unpack into an object of class SEFDset, based on class beamset.
        # 2017 Oct 23
        sbid = self.sbid
        times = self.time
        if per_ant:
            ants = self.good_antennas
        else:
            ants = self.good_baselines
        beams = [self.beam]
        frqs = self.freq
        meta = self.meta
        md = {'class': 'SEFDSet',
              'times': times,
              'antennas': ants,
              'beams': beams,
              'frequencies': [],
              'freq_range': [frqs[0], frqs[-1], len(frqs)],
              'polarizations': pols, 'payloadshape': (1,),
              'fp_name': meta['footprint.name'],
              'fp_pitch': meta['footprint.pitch'],
              'fp_angle': meta['footprint.rotation'],
              'beamformingSBID': -1,
              'beamformingPA': 0.0,
              'beamformingEpoch': 0.0,
              'holographySBID': -1,
              'holographyEpoch': 0.0,
              'calSBID': sbid,
              'beamType': 'formed',
              'difference': self.difference,
              'history': [time.asctime() + ": First Created"]}

        if 'beam_weights' in meta:
            beam_wts = meta['beam_weights']
            md['beam_weights'] = beam_wts
            # next if block temporary
            if '_' in beam_wts > 0:
                logger.info(f'beam_wts = {beam_wts}')
                try:
                    tmp = beam_wts.split('_')[0]
                    digits = re.findall('[0-9]+', tmp)[0]
                    md['beamformingSBID'] = int(digits)
                except ValueError as ve:
                    logger.info(ve)
                    logger.info('no beam weights found')
        logger.info("Saving hdf5 for mset {:d}".format(self.mset_inx))
        for k, v in md.items():
            logger.info(f"{k}, {v}")
        obj = SEFDSet(metadata=md)

        # Now copy the SEFD data themselves
        nti = len(self.time)
        nch = len(self.freq)
        seli = {'times': range(nti), 'channels': 0}
        selv = {}
        for thing in ['antennas', 'beams', 'polarizations']:
            selv[thing] = obj.metadata[thing]
        selector = obj.get_selector(seli, selv)

        if per_ant:
            output = self.sefd_per_ant
        else:
            output = self.sefd
        for s in selector:
            t, ant, beam, pol, freq = obj.get_vector(s)
            i, j, k, l, m = s

            try:
                qs = output[pol][ant][:nch, i]
                qs = np.ma.masked_array(qs, qs < 10.0)
                qs.mask = np.ma.mask_or(qs.mask, qs > 40000.0)

                obj.data[i, j, k, l, :, 0] = output[pol][ant][:nch, i]
                obj.flags[i, j, k, l, :] = qs.mask
            except KeyError:
                obj.data[i, j, k, l, :, 0] = 0.0
                obj.flags[i, j, k, l, :] = True
                logging.info('Missing item pol, ant :[{}][{}]'.format(pol, ant))

        # Write to a file with default name, unless overridden
        if file_name is None:
            fname = "SEFD_{:d}.hdf5".format(self.sbid)
        else:
            if file_name.endswith(".hdf5"):
                fname = file_name
            else:
                fname = "{}.hdf5".format(file_name)
        #   logging.info('Writing to file {}'.format(fname))
        logger.info('Writing to file {}'.format(fname))
        obj.write_to_hdf5(fname)

    def plot_per_ant(self, plot_file):
        ants = self.good_antennas

        _plot0_per_ant(self.sefd_per_ant, self.freq, ants, plot_file)

    def get_meta(self):
        try:
            sb = SchedulingBlock(self.sbid)
            meta = {'footprint.name': sb.get_footprint_name(),
                    'footprint.pitch': sb.get_footprint_pitch(),
                    'footprint.rotation': sb.get_footprint_rotation(),
                    'beam_weights': sb.get_weights_prefix()}
        except Ice.ConnectTimeoutException:
            logger.info('No Schedblock connection. Using dummy data')
            meta = {'footprint.name': 'square_6x6',
                    'footprint.pitch': 0.9,
                    'footprint.rotation': 0.0,
                    'beam_weights': 'prefix'}
        return meta


# noinspection PyTypeChecker
def bl_scales(n_avg, zvis, flux1934):
    logger.debug(f"Received visibilitoes: {type(zvis)} {zvis.shape}")
    zc = zvis.copy()
    za = np.abs(zc)
    zr = np.real(zc)
    zi = np.imag(zc)
    if n_avg > 1:
        logger.info(f"Box mean being performed for {n_avg=}")
        za = box_mean(za, n_avg)
        zr = box_mean(zr, n_avg)
        zi = box_mean(zi, n_avg)
        zc = zr + (0.0 + 1j) * zi
    
    # The use of .filled(np.nan) and nanpercentile below to avoid read-only memory error with maskedarrays
    # https://github.com/numpy/numpy/issues/21524
    cliplevel = np.nanpercentile(za.flatten().filled(np.nan), 99.5)
    onma = np.ma.masked_outside(za, 0.0, cliplevel)
    zc.mask = onma.mask
    # Compute vector mean piecwise: special code for data with changing phase errors.
    nt = zc.shape[1]
    dt = 0
    # dt = 5
    # 2018-APR-03 : set dt = 0 above to make sure the following block of code is not executed.
    # It does not do as intended (defeat phase slopes in visibilities).
    if dt > 1:
        wi = dt * 2 - 1
        i1 = range(0, nt - nt % dt, dt)
        subvm = np.array([np.abs(zc[:, i:(i + wi)].mean(axis=1)) for i in i1])
        vecmean = np.ma.masked_array(subvm.mean(axis=0), mask=zc.mask.all(axis=1))
    else:
        vecmean = np.ma.masked_array(np.abs(zc.mean(axis=1)), mask=zc.mask.all(axis=1))
    scale = flux1934 / vecmean
    return scale


def bl_noise(zvis, scale, btau, n_avg, diff):
    """

    :param zvis:
    :param scale:
    :param btau:
    :param n_avg:
    :param diff: Options are 'none', 'time', 'frequency'
    :return:
    """
    nf, nt = zvis.shape
    mf, nb = n_avg, nf // n_avg
    n_med_filt = 51
    # zz = np.reshape(zvis.copy(),(mf,nb,nt))
    zz = zvis.copy()
    n_fl = [np.ma.count_masked(zz)]
    za = np.abs(zz)
    zr = np.real(zz)
    zi = np.imag(zz)
    
    # The use of .filled(np.nan) and nanpercentile below to avoid read-only memory error with maskedarrays
    # https://github.com/numpy/numpy/issues/21524
    cliplevel = np.nanpercentile(za.flatten().filled(np.nan), 99.9)
    abs_masked = np.ma.masked_outside(za, 0.0, cliplevel).mean(axis=1)

    if za.shape[0] > 3 * n_med_filt:
        filt = medfilt(abs_masked, n_med_filt)
        abs_masked_normed = np.ma.masked_outside(abs_masked / filt, 0.87, 1.13)
    else:
        abs_masked_normed = abs_masked
    ss = {}
    n_fl.append(np.ma.count_masked(abs_masked_normed))
    for z, r in [(zr, 'real'), (zi, 'imag')]:
        # The use of .filled(np.nan) and nanpercentile below to avoid read-only memory error with maskedarrays
        # https://github.com/numpy/numpy/issues/21524
        # noinspection PyTypeChecker
        clip = np.nanpercentile(z.flatten().filled(np.nan), [0.1, 99.9])
        zcl = np.ma.masked_outside(z, clip[0], clip[1])
        n_fl.append(np.ma.count_masked(zcl))
        zbin = np.reshape(zcl, (nb, mf, nt))
        np.ma.set_fill_value(zbin, np.nan)
        if diff == 'frequency':
            fac = 1.0 / np.sqrt(2)
            zc = zbin.copy()
            zbin[1:, :, :] -= zc[:-1, :, :]
            zbin[0, :, :] *= 1.0 / fac
        elif diff == 'time':
            fac = 1.0 / np.sqrt(2)
            zc = zbin.copy()
            zb = zbin[:, :, 1:] - zc[:, :, :-1]
            zbin = zb
        else:
            fac = 1.0
        zbin = np.ma.masked_equal(zbin, np.nan)
        ons = zbin.std(axis=2).mean(axis=1) * fac
        # ons = zbin.mean(axis=1).std(axis=1)
        ss[r] = np.sqrt(btau) * ons * scale
    ssys = (ss['real'] + ss['imag']) / 2.0
    ssys.mask = abs_masked_normed.mask.all(axis=0)
    n_fl.append(np.ma.count_masked(ssys))
    return ssys


# noinspection PyTypeChecker
def bl_noise_fft(zvis, scale, btau, n_avg):
    nf, nt = zvis.shape
    mf, nb = n_avg, nf / n_avg
    n_med_filt = 51
    # zz = np.reshape(zvis.copy(),(mf,nb,nt))
    zz = zvis.copy()
    za = np.abs(zz)
    zr = np.real(zz)
    zi = np.imag(zz)
    
    # The use of .filled(np.nan) and nanpercentile below to avoid read-only memory error with maskedarrays
    # https://github.com/numpy/numpy/issues/21524
    cliplevel = np.percentile(za.flatten().filled(np.nan), 99.9)
    abs_masked = np.ma.masked_outside(za, 0.0, cliplevel).mean(axis=1)

    if za.shape[0] > 3 * n_med_filt:
        filt = medfilt(abs_masked, n_med_filt)
        abs_masked_normed = np.ma.masked_outside(abs_masked / filt, 0.87, 1.13)
    else:
        abs_masked_normed = abs_masked
    ss = {}
    for z, r in [(zr, 'real'), (zi, 'imag')]:
        # The use of .filled(np.nan) and nanpercentile below to avoid read-only memory error with maskedarrays
    # https://github.com/numpy/numpy/issues/21524
        clip = np.nanpercentile(z.flatten().filled(np.nan), [0.1, 99.9])
        zcl = np.ma.masked_outside(z, clip[0], clip[1])
        zbin = np.reshape(zcl, (nb, mf, nt))
        zst = []
        for i in range(nb):
            zsub = zbin[i, :, :]
            st, am, x, y = fftmeth(zsub)
            zst.append(st)
        ons = np.array(zst)
        # ons = zbin.std(axis=2).mean(axis=0)
        ss[r] = np.sqrt(btau) * ons * scale
    ssys = (ss['real'] + ss['imag']) / 2.0
    ssys.mask = abs_masked_normed.mask.all(axis=0)
    return ssys


def fftmeth(sig):
    # an alternate method to determine the underlying variance in the presence of sinusoidal fringes
    # in real or imag visibilities.

    N, M = sig.shape
    Ns = min(5, N / 10)
    my = 5
    sigu = np.ma.filled(sig, 0.0)
    frat = np.sqrt(N * M)
    tsig = np.ma.masked_array(rfft2(sigu) / frat, mask=False)
    atsig = np.abs(tsig)
    amax = atsig.max()
    xy = np.where(atsig == atsig.max())
    x, y = xy[0][0], xy[1][0]
    y1, y2 = min(0, y - my), max(M, y + my)
    tsig.mask[x, y1:y2] = True
    std = tsig[Ns:-(Ns + 1), :].std()
    return std, amax, x, y


def remove_mean(z):
    n = z.shape[1]
    mean = np.tile(z.mean(axis=1), (n, 1)).transpose()
    return z - mean


def decomp(prod, lpols, arr, flags):
    what_a = {}
    b_flgs = []
    for b in arr.baselines:
        b_flgs.append(flags[b])
    b_flgs = np.array(b_flgs)
    logger.info("Flagging {:d} baselines".format(len(b_flgs) - b_flgs.sum()))
    logger.info(f"List of flagged baselines : {np.where(b_flgs == 0)}")

    for ipol in lpols:
        what_a[ipol] = {}
        products = []
        for b in arr.baselines:
            products.append(prod[ipol][b])
        products = np.array(products)
        resu = antenna_decompose(products, arr, b_flgs)
        for i, a in enumerate(arr.antennas):
            what_a[ipol][a] = resu[i]
    return what_a


def _plot0_per_ant(sefd_per_ant, chan_freq, ants, pltname):
    sxx = sefd_per_ant[0]
    syy = sefd_per_ant[3]
    fig = plt.figure()
    plt.clf()
    par = {'xtick.labelsize': 8, 'ytick.labelsize': 8}
    plt.rcParams.update(par)
    freq = chan_freq
    nvert = len(ants)
    nplots = nvert * 2
    for i, a in enumerate(ants):
        kx = 1 + i * 2
        ky = 1 + i * 2 + 1
        for ss, k in zip([sxx, syy], [kx, ky]):
            # print i,a,k
            ax = fig.add_subplot(nvert, 2, k)
            plt.plot(freq, ss[a] * 0.001)
            plt.ylim(0, 8)
            ax.set_xticks(ax.get_xticks()[::2])
            ax.set_yticks(ax.get_yticks()[::2])
            if k < (nplots - 1):
                ax.set_xticklabels([])
            if k % 2 == 0:
                ax.set_yticklabels([])
            plt.text(900, 6.0, "AK%02d" % a)
            plt.grid()
    fig.suptitle(pltname)
    plt.savefig("%s.png" % pltname, dpi=300)
    logger.info('Plot file %s.png written to %s' % (pltname, os.getcwd()))


"""
def _plot_C(comparison, s1, s2):
    # If ever this routine is n=made to work, the frequencies of the two files
    # must match - check and enforce.
    freq = s1.dataset.chan_freq * 1.0e-6
    cx = comparison[0]
    cy = comparison[3]
    fig = plt.figure()
    plt.clf()
    par = {'xtick.labelsize': 8, 'ytick.labelsize': 8}
    plt.rcParams.update(par)
    pltname = 'Comparison : SEFD_ID%d/SEFD_ID%d' % (s1.sbid, s2.sbid)
    freq = chan_freq * 1.0e-6
    for i, a in enumerate(Ants):
        kx = 1 + i * 2
        ky = 1 + i * 2 + 1
        for c, k in zip([cx, cy], [kx, ky]):
            ax = fig.add_subplot(6, 2, k)
            plt.plot(freq, ss[a] * 0.001)
            plt.ylim(0, 8)
            ax.set_xticks(ax.get_xticks()[::2])
            ax.set_yticks(ax.get_yticks()[::2])
            if k < 11:
                ax.set_xticklabels([])
            if k % 2 == 0:
                ax.set_yticklabels([])
            plt.text(900, 6.0, "AK%02d" % a)
            plt.grid()
    fig.suptitle(pltname)
    plt.savefig("%s.png" % pltname, dpi=300)
    print 'Plot file %s_compare.png written to %s' % (pltname, os.getcwd())
"""


def medfilt(x, k):
    """Apply a length-k median filter to a 1D array x.
    Boundaries are extended by repeating endpoints.
    """
    assert k % 2 == 1, "Median filter length must be odd."
    assert x.ndim == 1, "Input must be one-dimensional."
    k2 = (k - 1) // 2
    y = np.zeros((len(x), k), dtype=x.dtype)
    y[:, k2] = x
    for i in range(k2):
        j = k2 - i
        y[j:, i] = x[:-j]
        y[:j, i] = x[0]
        y[:-j, -(i + 1)] = x[j:]
        y[-j:, -(i + 1)] = x[-1]
    return np.median(y, axis=1)
