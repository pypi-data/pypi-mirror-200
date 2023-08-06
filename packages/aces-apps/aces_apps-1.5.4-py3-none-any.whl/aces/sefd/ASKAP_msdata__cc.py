from __future__ import print_function

"""
File ASKAP_msdata.py

Defines the class msData that provides a convenient interface to ASKAP measurement sets.
Derived from the earlier beta6.py that was narrowly defined for the 6-antenan BETA.

10 March 2016
"""

__author__ = 'Dave McConnell <david.mcconnell@csiro.au>'

import sys
import re
import glob
import itertools
import inspect
from casacore.tables import *

# =======================================================
# Method for accessing globals within the function
# This comes from a CASACamp_template.py tutorial
# boilerplate - handles the global namespace acquisition
#    myf is the means of accessing the globals within the function
#
# Modified on 23-Jan-2018 from 'ipython console' to 'ipython'

a = inspect.stack()
stacklevel = 0
for k in range(len(a)):
    if a[k][1].find('ipython') > 0:
        stacklevel = k
myf = sys._getframe(stacklevel).f_globals
if 'me' in myf:
    me = myf['me']
if 'ms' in myf:
    ms = myf['ms']
if 'tb' in myf:
    tb = myf['tb']


def get_msname(schbid, tele='ASKAP', msdir=None, mset_inx=None):
    # Returns ms name. 
    # Prior to October 2017, ms names have form 2017-09-01_100058.ms
    # Later they are like: 2017-10-01_100058_1.ms
    # This routine handles both.
    # If old, mset_inx arg effectively ignored.
    # If new, mset_inx arg determines which file, default name returned is for mset_inx=0
    #
    # schbid  Sched block ident
    # tele     Telescope name (determines which directory to search)
    # msdir    If given, overrides default directory for telescope)
    # mset_inx     If given, and if ms names have mset_inx reference, choose the
    #              corresponding file.
    dnames = ["/astro/askaprt/askapops/askap-scheduling-blocks/",
              "/askapbuffer/ingest/askap-scheduling-blocks/",
              "/askapbuffer/payne/askap-scheduling-blocks/"]
    if mset_inx is None:
        fnames = []
        i = 0
        while len(fnames) == 0 and i < len(dnames):
            dname = dnames[i]
            dtmpl = dname + "{:d}/*.ms".format(schbid)
            fnames = glob.glob(dtmpl)
            i += 1
        # dtmpl = dname + "{:d}/*.ms".format(schbid)
        # if dname_alt is not None:
        #     dtmpl_alt = dname_alt + "{:d}/*.ms".format(schbid)
    else:
        fnames = []
        i = 0
        while len(fnames) == 0 and i < len(dnames):
            dname = dnames[i]
            dtmpl = dname + "{:d}/*_{:d}.ms".format(schbid, mset_inx)
            fnames = glob.glob(dtmpl)
            i += 1

    if len(fnames) > 0:
        return fnames[0]
    else:
        raise IOError("Can't find ms files for SB{} at {}".format(schbid, dtmpl))


class MSData(object):
    attached = False

    def __init__(self, fname):
        t = table(fname)
        self.tab = t
        self.tname = t.name()
        MSData.attached = True
        self.beams = self._get_beams()

        self.n_beams = len(self.beams)
        self.chan_freq, chan_wid = self._get_channels()
        self.n_chans = self.chan_freq.shape[0]
        self.bw = abs(chan_wid * self.n_chans)
        self.a_names = self._get_antenna_names()
        self.ants = self._get_ants(self.a_names)
        self.n_ants = len(self.a_names)
        self.n_products = self.n_ants * (self.n_ants - 1) // 2 + self.n_ants
        self.baselines = self._gen_baselines()

    def _get_beams(self):
        tfn = self.tname + '/FEED'
        tf = table(tfn)
        feeds = tf.getcol('FEED_ID')
        beams = sorted(list(set(feeds)))
        return beams

    def _get_channels(self):
        tfn = self.tname + '/SPECTRAL_WINDOW'
        tf = table(tfn)
        frq = tf.getcol('CHAN_FREQ')[0, :]
        chw = tf.getcol('CHAN_WIDTH')[0, :][0]
        return frq, chw

    def _get_antenna_names(self):
        tan = self.tname + '/ANTENNA'
        ta = table(tan)
        names = ta.getcol('NAME')
        return names

    @staticmethod
    def _get_ants(a_names):
        nums = [int(re.findall('[0-9]{2}', ant)[0]) for ant in a_names]
        return nums

    def _gen_baselines(self):
        ants = self.ants
        n_ants = self.n_ants
        temp = [['%dx%d' % (ants[j], ants[i]) for i in range(j, n_ants)] for j in range(n_ants)]
        return list(itertools.chain.from_iterable(temp))

    def get_data_w(self, feed, nchans, chan1, scan=None, start=0.0, n_sec=0.0):
        # Read data from the ms.
        # read across whole set of baselines, specified channel range and specified time range.
        # the result is an array with three axes:
        #  x[4, nCH, M]
        # where M is product of number of baselines NB and number of cycles NT.
        # The order is all baselines for time 1, then for time 2 etc.
        # within the NB visibilities for each time, the baselines are ordered:
        # 0 0
        # 0 1
        # 0 2
        # ..
        # 0 NA-1
        # 1 1
        # ..
        # NA-1 NA-1
        # where the antenna numbers correspond the the antenna names in the ANTENNA table.
        #
        # for output, convert the array to four dimensions:
        #  vis[0:3, 0:nch-1, 0:NT-1, 0:NB-1]
        #
        qf = "FEED1={:d}".format(feed)
        tq1 = self.tab.query(query=qf)
        if scan is not None:
            qs = "SCAN_NUMBER={:d}".format(scan)
            tq2 = tq1.query(query=qs)
        else:
            tq2 = tq1
        t0 = tq2.getcol('TIME')[0]
        t1 = t0 + start
        if n_sec == 0.0:
            t2 = tq2.getcol('TIME')[-1]
        else:
            t2 = t1 + n_sec
        qt1 = "TIME>{:f}".format(t1)
        qt2 = "TIME<{:f}".format(t2)
        tq3 = tq2.query(query=qt1)
        tq4 = tq3.query(query=qt2)
        ch1, ch2 = chan1, chan1 + nchans
        da = tq4.getcol('DATA')[:, ch1:ch2, :]
        fl = tq4.getcol('FLAG')[:, ch1:ch2, :]
        vis0 = np.ma.masked_array(da, mask=fl)
        sh = vis0.shape
        nsh = [sh[0] // self.n_products, self.n_products, sh[1], sh[2]]
        vis = np.reshape(vis0, nsh)
        vis = np.rollaxis(vis, 2, 0)
        vis = np.rollaxis(vis, 3, 0)
        uvw = tq4.getcol('UVW')
        return vis, uvw

    def get_time(self, scan):
        qs = "SCAN_NUMBER={:d}".format(scan)
        tbs = self.tab.query(query=qs)
        # tbs.summary()
        ti = tbs.getcol('TIME')
        dt = tbs.getcol('INTERVAL')[0]
        nant = self.n_ants
        nbas = nant * (nant - 1) // 2 + nant
        nsh = [ti.shape[0] // nbas, nbas]
        print(" ti: {} nsh:{} ".format(type(ti), type(nsh)))
        tir = np.reshape(ti, nsh)
        return tir[:, 0], dt

    def get_t_integ(self, scan=0):
        # return integration time in seconds
        time, t_integ = self.get_time(scan)
        # t_integ = (time[-1] - time[0]) / len(time)
        return t_integ

    def get_ch_bw(self):
        # return channel bandwidth in Hz
        return self.bw / self.n_chans

    def get_scan_posn(self, az, el):
        # Expects a msData object scanData, and the azimuth and elevation  in radians.
        # returns RA and Dec along scan, in radians
        j1 = 30

        me.doframe(me.observatory('ASKAP'))

        direc = {'m0': {'unit': 'rad', 'value': az},
                 'm1': {'unit': 'rad', 'value': el},
                 'refer': 'azel',
                 'type': 'direction'}
        times = self.get_time(0)
        t1 = [me.epoch('UTC', v0={'value': t, 'unit': 's'}) for t in times[j1:]]
        rd = []

        for ti in t1:
            me.doframe(ti)
            r = me.measure(direc, 'J2000')
            rd.append([r['m0']['value'], r['m1']['value']])
        radec = np.array(rd)

        ra = (2.0 * np.pi + radec[:, 0]) % (2.0 * np.pi)
        dec = radec[:, 1]
        return ra, dec

    def get_beam_id(self):
        beams = self.tab.getcol('FEED1')
        if len(set(beams)) == 1:
            beam = beams[0]
        else:
            print("Several beams in this file")
            raise RuntimeError("Several beams in this file {}.".format(self.tab.name()))
        return beam

    def get_scan_info(self):
        ts = self.tab.getcol('SCAN_NUMBER')
        scans = sorted(list(set(ts)))
        interval = self.tab.getcol('INTERVAL')[0]
        ret = {}
        for s in scans:
            qs = "SCAN_NUMBER={:d}".format(s)
            tbs = self.tab.query(query=qs)
            ti = tbs.getcol('TIME')
            time = ti[0]
            dur = ti[-1] - time + interval
            t_int = len(set(ti)) * interval
            f_id = tbs.getcol('FIELD_ID')[0]
            tf = table(self.tname + '/FIELD')
            fn = tf.getcol('NAME')[f_id]
            ret[s] = (time, dur, t_int, fn)
        return ret

    @staticmethod
    def get_az_el():
        # returns the Az,El of the first antenna at the first time. For drift scans
        # this is sufficient. For tracking observations, more would be required.
        # Returned in degrees.
        pname = "%s/POINTING" % ms.name()
        tb.open(pname)
        az = tb.getcol('AZIMUTH', 0, 1)
        el = tb.getcol('ELEVATION', 0, 1)
        parang = tb.getcol('POLANGLE', 0, 1)
        return np.array([az[0], el[0], parang])

    @classmethod
    def is_open(cls):
        return cls.attached
