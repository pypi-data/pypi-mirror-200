from __future__ import print_function

"""A class providing a standard estimation of the System Equivalent FLux Density for Beta data files
taken on the source B1934-638."""

__author__ = 'Dave McConnell <david.mcconnell@csiro.au>'

import numpy as np
import matplotlib.pylab as plt
import os
import pickle
import ASKAP_msdata as akms
import flux_of_1934 as fl
from aces.askapdata.schedblock import SchedulingBlock

import itertools
from numpy.fft import rfft2

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
            print('ASKAP_array: Unknown name %s' % name)
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


def antenna_decompose(products, arr):
    # compute antenna specific quantities from the set of n(n-1)/2 products
    # Input products[0:nBas][0:M] is a n(n-1)/2 entry dictionary, each being an array (could be M frequency channels
    # or M time samples

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
            A[row][i] = 1
            A[row][j] = 1

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
    def __init__(self, sbid, file_name=None, beam=0, dch=1, ch0=0, ncf=0, scan=0, dnt=120, nstart=3, nct=0):
        # Expects:
        # sbid      sched block ID
        # file_name  ms name; if None, work it out from sbid and arr: assume usual archive position
        # Beam      beam number
        # dch       frequency cell width in channels
        # chan0     start freq chan number
        # ncF       number of frequency cells; as many as possible if  ncF = 0
        # scan      scan number
        # dnt       time cell width in cycles
        # nstart    start at this integration cycle number
        # nct       number of time cells; as many as possible if nct = 0
        self.sbid = sbid
        self.beam = beam
        self.array = ASKAP_array('ASKAP')
        arr = self.array

        if file_name is not None:
            self.fname = file_name
            print ("file_name = %s" % file_name)
        else:
            self.fname = akms.get_msname(self.sbid, tele=arr.name, beam=self.beam)
            print ("%d %s --> %s" % (self.sbid, arr.name, self.fname))
        d = akms.MSData(self.fname)
        arr.select_antennas(d.ants)

        self.dch = dch
        self.ch0 = ch0

        # fix channel cell details:
        nc_fmax = (d.n_chans - self.ch0) / self.dch
        if ncf == 0:
            self.ncf = nc_fmax
        else:
            self.ncf = min(nc_fmax, ncf)
        self.nChans = self.ncf * self.dch

        # fix time cell details 
        self.scan = scan
        self.times = d.get_time(self.scan, feed=self.beam)
        self.nt = len(self.times)
        self.del_t = d.get_t_integ(feed=self.beam)
        # Limit dnt (2016/10/11)
        self.dt = min(self.nt - nstart, dnt) * self.del_t
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

        self.baselines = d.baselines
        self.basants = [map(int, bas.split('x')) for bas in self.baselines]
        self.dataset = d
        self.scratch = []
        self.good_antennas = []
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
        self.meta = self.get_meta()

    def summary(self):
        print ("SBID : %d   Beam  : %d   Scan : %d" % (self.sbid, self.beam, self.scan))
        print ("Integration cells %d x %d (channels x cycles)" % (self.dch, self.dt))
        cell_wid = self.dch * self.dataset.get_ch_bw() * 1.0e-6
        print ("Cell width      %7.4f MHz" % cell_wid)
        print ("Cell duration   %7.1f s" % self.dt)
        print ("%d x %d = %d integration cells" % (self.ncf, self.nct, self.ncf * self.nct))
        print ("Btau = %8.1f" % self.btau)
        print ("ms read: %d chans from %d" % (self.nChans, self.ch0))
        print ("         %6.1f s " % self.dt)

    def calc_sefd(self):
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
        for ipol in [0, 1, 2, 3]:
            ssys[ipol] = {}
            scale[ipol] = {}
            auto_mean[ipol] = {}
            auto_std[ipol] = {}
            nflags[ipol] = {}
            for bas, basants in zip(self.baselines, self.basants):
                if basants[0] != basants[1]:
                    ssys[ipol][bas] = []
                    scale[ipol][bas] = []
                    nflags[ipol][bas] = []
                else:
                    auto_mean[ipol][basants[0]] = []
                    auto_std[ipol][basants[0]] = []
        ##########
        print ('Reading data: ')
        self.scratch = []
        ant_ok = []
        for i, ti in enumerate(self.rTstarts):
            bintim.append(ti + 0.5 * self.dt)
            print ('Reading data: times %5.1f to %5.1f...' % (ti, ti + self.dt), end=' ')
            vis = d.get_data_w(self.beam, self.nChans, self.ch0, scan=self.scan, start=ti, n_sec=self.dt)
            print (' ')
            for bi, bas in enumerate(self.baselines):
                sb = self.basants[bi]
                if sb[0] != sb[1]:
                    if bool(vis[:, :, :, bi].any()):
                        ant_ok += sb
                        ipol = 0
                        z = vis[ipol, :, :, bi]
                        scalebx = bl_scales(n_avg, z, flux1934)
                        ssysb = bl_noise(z, scalebx, btau, n_avg)
                        scale[ipol][bas].append(scalebx)
                        ssys[ipol][bas].append(ssysb)
                        nflags[ipol][bas].append(np.ma.count_masked(z))

                        ipol = 3
                        z = vis[ipol, :, :, bi]
                        scaleby = bl_scales(n_avg, z, flux1934)
                        ssysb = bl_noise(z, scaleby, btau, n_avg)
                        scale[ipol][bas].append(scaleby)
                        ssys[ipol][bas].append(ssysb)
                        nflags[ipol][bas].append(np.ma.count_masked(z))

                        scalebxy = np.sqrt(scalebx * scaleby)
                        for ipol in [1, 2]:
                            z = vis[ipol, :, :, bi]
                            ssysb = bl_noise(z, scalebxy, btau, n_avg)
                            scale[ipol][bas].append(scalebxy)
                            ssys[ipol][bas].append(ssysb)
                            nflags[ipol][bas].append(np.ma.count_masked(z))
                    else:
                        print ("%s masked count = %d  count = %d" % (bas, np.ma.count_masked(vis), np.ma.count(vis)))
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
        print ("Found good antennas %s" % self.good_antennas)

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

        what_per_ant = decomp(prod, lpols, good_array)

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
        print ("SEFD_A saved to %s.pkl" % file_name)

    def plot_per_ant(self, plot_file):
        ants = self.good_antennas

        _plot0_per_ant(self.sefd_per_ant, self.freq, ants, plot_file)

    def get_meta(self):
        sb = SchedulingBlock(self.sbid)
        meta = {'footprint.name': sb.get_footprint_name(),
                'footprint.pitch': sb.get_footprint_pitch(),
                'footprint.rotation': sb.get_footprint_rotation(),
                'beam_weights': sb.get_weights_prefix()}

        return meta


# noinspection PyTypeChecker
def bl_scales(n_avg, zvis, flux1934):
    zc = zvis.copy()
    za = np.abs(zc)
    zr = np.real(zc)
    zi = np.imag(zc)
    if n_avg > 1:
        za = box_mean(za, n_avg)
        zr = box_mean(zr, n_avg)
        zi = box_mean(zi, n_avg)
        zc = zr + (0.0 + 1j) * zi
    cliplevel = np.percentile(za.flatten(), 99.5)
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


def bl_noise(zvis, scale, btau, n_avg):
    """

    :param zvis:
    :param scale:
    :param btau:
    :param n_avg:
    :return:
    """
    nf, nt = zvis.shape
    mf, nb = n_avg, nf / n_avg
    n_med_filt = 51
    # zz = np.reshape(zvis.copy(),(mf,nb,nt))
    zz = zvis.copy()
    n_fl = [np.ma.count_masked(zz)]
    za = np.abs(zz)
    zr = np.real(zz)
    zi = np.imag(zz)
    cliplevel = np.percentile(za.flatten(), 99.9)
    abs_masked = np.ma.masked_outside(za, 0.0, cliplevel).mean(axis=1)

    if za.shape[0] > 3 * n_med_filt:
        filt = medfilt(abs_masked, n_med_filt)
        abs_masked_normed = np.ma.masked_outside(abs_masked / filt, 0.87, 1.13)
    else:
        abs_masked_normed = abs_masked
    ss = {}
    n_fl.append(np.ma.count_masked(abs_masked_normed))
    for z, r in [(zr, 'real'), (zi, 'imag')]:
        # noinspection PyTypeChecker
        clip = np.percentile(z.flatten(), [0.1, 99.9])
        zcl = np.ma.masked_outside(z, clip[0], clip[1])
        n_fl.append(np.ma.count_masked(zcl))
        zbin = np.reshape(zcl, (mf, nb, nt))
        ons = zbin.std(axis=2).mean(axis=0)
        ss[r] = np.sqrt(btau) * ons * scale
    ssys = (ss['real'] + ss['imag']) / 2.0
    ssys.mask = abs_masked_normed.mask.all(axis=0)
    n_fl.append(np.ma.count_masked(ssys))
    print (','.join(["%8d" % nfi for nfi in n_fl]))
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
    cliplevel = np.percentile(za.flatten(), 99.9)
    abs_masked = np.ma.masked_outside(za, 0.0, cliplevel).mean(axis=1)

    if za.shape[0] > 3 * n_med_filt:
        filt = medfilt(abs_masked, n_med_filt)
        abs_masked_normed = np.ma.masked_outside(abs_masked / filt, 0.87, 1.13)
    else:
        abs_masked_normed = abs_masked
    ss = {}
    for z, r in [(zr, 'real'), (zi, 'imag')]:
        clip = np.percentile(z.flatten(), [0.1, 99.9])
        zcl = np.ma.masked_outside(z, clip[0], clip[1])
        zbin = np.reshape(zcl, (mf, nb, nt))
        zst = []
        for i in range(nb):
            zsub = zbin[:, i, :]
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


def decomp(prod, lpols, arr):
    what_a = {}
    for ipol in lpols:
        what_a[ipol] = {}
        products = []
        for b in arr.baselines:
            products.append(prod[ipol][b])
        products = np.array(products)
        resu = antenna_decompose(products, arr)
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
    print ('Plot file %s.png written to %s' % (pltname, os.getcwd()))


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
