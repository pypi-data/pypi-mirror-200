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
import inspect
import string
import numpy as np
import itertools

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
    if string.find(a[k][1], 'ipython') > 0:
        stacklevel = k
myf = sys._getframe(stacklevel).f_globals
if 'me' in myf:
    me = myf['me']
if 'ms' in myf:
    ms = myf['ms']
if 'tb' in myf:
    tb = myf['tb']


##########################

def get_msname(schbid, tele='ASKAP', msdir=None, beam=None):
    # Returns ms name. 
    # Prior to October 2017, ms names have form 2017-09-01_100058.ms
    # Later they are like: 2017-10-01_100058_1.ms
    # This routine handles both.
    # If old, beam arg effectively ignored.
    # If new, beam arg determines which file, default name returned is for beam=0
    #
    # schbid  Sched block ident
    # tele     Telescope name (determines which directory to search)
    # msdir    If given, overrides default directory for telescope)
    # beam     If given, and if ms names have beam reference, choose the
    #              corresponding file.
    if msdir:
        dname = msdir
    else:
        if tele == "BETA":
            dname = "/scratch2/askap/askapops/archive/beta-scheduling-blocks/"
        else:
            dname = "/astro/askaprt/askapops/askap-scheduling-blocks/"
    dtmpl1 = dname + "%d/*.ms" % schbid
    if beam is None:
        dtmpl2 = ""
    else:
        dtmpl2 = dname + "%d/*_%d.ms" % (schbid, beam)
    fnames1 = glob.glob(dtmpl1)
    fnames2 = glob.glob(dtmpl2)
    if len(fnames2) > 0:
        print(fnames2)
        return fnames2[0]
    else:
        if len(fnames1) > 0:
            return fnames1[0]
        else:
            raise IOError("Can't find ms files for SB{} at {} or {}".format(schbid, dtmpl2, dtmpl1))


# Routines for accessing ms data

class MSData(object):
    attached = False

    def __init__(self, fname):
        ms.open(fname)
        MSData.attached = True
        axis_info = ms.getdata(['axis_info'])
        feeds = list(set(ms.getdata(['feed1'])['feed1']))
        feeds.sort()
        self.beams = feeds

        self.n_beams = len(self.beams)
        iscan = 0
        self.chan_freq = axis_info['axis_info']['freq_axis']['chan_freq'][:, iscan]
        self.n_chans = self.chan_freq.shape[0]
        self.bw = abs(axis_info['axis_info']['freq_axis']['resolution'][0][iscan] * self.n_chans)
        self.a_names = self._get_ant_names()
        self.ants = self._get_ants(self.a_names)
        self.n_ants = len(self.a_names)
        self.n_products = self.n_ants * (self.n_ants - 1) / 2 + self.n_ants
        self.baselines = self._gen_baselines()

    @staticmethod
    def close():
        ms.done()
        MSData.attached = False

    @staticmethod
    def _get_ant_names():
        name = "%s/ANTENNA" % ms.name()
        tb.open(name)
        a_names = tb.getcol('NAME')
        return a_names

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
        sel = {'feed1': [feed]}
        ms.selectinit(datadescid=0)
        if scan is not None:
            sc = ms.getscansummary()
            scan = "%d" % scan
            t1 = 86400.0 * sc[scan]['0']['BeginTime'] + start
            if n_sec == 0.0:
                t2 = 86400.0 * sc[scan]['0']['EndTime']
            else:
                t2 = t1 + n_sec
            sel['time'] = [t1, t2]
        ms.select(sel)
        ms.selectchannel(nchans, chan1, 1, 1)
        x = ms.getdata(['data', 'flag'])
        vis0 = np.ma.masked_array(x['data'], mask=x['flag'])
        sh = vis0.shape
        nsh = [sh[0], sh[1], sh[2] / self.n_products, self.n_products]
        vis = np.reshape(vis0, nsh)
        return vis

    @staticmethod
    def get_time(scan, feed=0):
        sc = ms.getscansummary()
        scan = "%d" % scan
        t1 = 86400.0 * sc[scan]['0']['BeginTime']
        t2 = 86400.0 * sc[scan]['0']['EndTime']
        sel = {'antenna1': [0], 'antenna2': [1], 'feed1': [feed], 'time': [t1, t2]}
        ms.selectinit(datadescid=0)
        ms.select(sel)
        print (sel)
        # print ms.getdata(['time'])
        time = ms.getdata(['time'])['time']
        return time

    def get_t_integ(self, scan=0, feed=0):
        # return integration time in seconds
        time = self.get_time(scan, feed)
        t_integ = (time[-1] - time[0]) / len(time)
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
