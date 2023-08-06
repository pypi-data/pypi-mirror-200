#!/usr/bin/env python
from __future__ import print_function

"""
sefd_spectrum
Plots spectra of SEFD files.

 $Author: mcc381 $


"""
import sys
import argparse as ap
import matplotlib as mpl

# mpl.use('Agg')  # this line must precede pylab import to suppress display
import matplotlib.pyplot as plt  # noqa
import numpy as np  # noqa
import scipy.optimize as op  # noqa
import scipy.stats.mstats as ssm

import aces.beamset.beamfactory as bf  # noqa
import logging  # noqa

big = 1.0e+20

explanation = """
A single beam is chosen for each given SBID, and SEFD vs frequency is plotted separately for each antenna.
The beam chosen is the closest to the boresight (footprint dependent). The -b option can be used to force
the spectrum for a particular beam to be plotted.
"""


def arg_init():
    parser = ap.ArgumentParser(prog='sefd_spectrum', formatter_class=ap.RawDescriptionHelpFormatter,
                               description='Plots the spectrum of SEFD measurements',
                               epilog='See -x for more explanation')
    parser.add_argument('sbid', nargs="+", type=int, help="SBIDs to plot - give space-separated list ")
    parser.add_argument('-b', '--o_beam', type=float, default=-1, help="Force beam number to this value")
    parser.add_argument('-f', '--f_delta', type=float, default=4.0, help="Frequency averaging interval (MHz)")
    parser.add_argument('-l', '--label', default=None, help="Optional plot label and file name suffix")
    parser.add_argument('-d', '--display', action='store_true', help="Display plot on screen")
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-x', '--explain', action='store_true', help="Give an expanded explanation")
    return parser


def fitfunc2(p, x):
    return p[0] * np.exp(-((x - p[1]) / p[2]) ** 2)


def errfunc2(p, x, y):
    return fitfunc2(p, x) - y


def linfunc(p, x):
    return p[0] + p[1] * x


def linerr(p, x, y):
    return linfunc(p, x) - y


funcs = {'lin': (linfunc, linerr), 'gau': (fitfunc2, errfunc2)}


def fit_g(x, y, p0, fkey='gau'):
    func = funcs[fkey][0]
    errf = funcs[fkey][1]
    xx = np.array(x)
    yy = np.array(y)
    #    p0 = [max(yy), mean(xx), min(yy)] # Initial guess for the parameters
    r = op.leastsq(errf, p0, args=(xx, yy))
    p1 = r[0]
    xf = np.linspace(min(xx), max(xx), 100)
    yf = [func(p1, x) for x in xf]
    res = 0.0
    for u, v in zip(xx, yy):
        res += errf(p1, u, v) ** 2
    res = res / len(xx)
    return p1, xf, yf, res


def find_mode(data):
    lower, upper = [500, 50000]
    if data.max() < lower:
        return lower
    if data.min() > upper:
        return upper
    cdata = data.compressed()
    if len(cdata) > 0:
        hist_range = (np.log(lower), np.log(upper))
        histdata = np.histogram(np.log(cdata), bins=100, range=hist_range)

        hy = np.array(histdata[0])
        hx = np.array(histdata[1])
        hxc = (hx[:-1] + hx[1:]) / 2
        imode = np.where(hy == hy.max())[0][0]
        i1, i2 = max(0, imode - 8), imode + 8
        p0 = [hy.max(), hxc[imode], 0.3]
        rfit = fit_g(hxc[i1:i2], hy[i1:i2], p0)
        return np.exp(rfit[0][1])
    else:
        return -1.0


def bsect(x, z):
    """
    Find position in array x of value z; assumes x sorted in increasing order.
    Returns j such that x[j] <= z < x[j+1]
  """
    n = len(x)
    if n == 0:
        return 0
    j1 = 0
    j2 = n
    j = j1
    while (j2 - j1) > 1:
        j = (j1 + j2) / 2
        if x[j] == z:
            break
        if x[j] > z:
            j2 = j
        else:
            j1 = j
        if x[j] > z:
            j = j - 1
    return j


def gather_data(obj, delta_freq=4.0, override_beam=-1):
    fp_name = obj.metadata['fp_name']
    if override_beam >= 0:
        beam = override_beam
    else:
        beam = 0
        if 'closepack36' in fp_name:
            beam = 21
        elif 'square_6x6' in fp_name:
            beam = 1
        elif 'boresight' in fp_name:
            beam = 0
        else:
            logging.info("Footprint name %s" % fp_name)

    logging.info("Footprint name %s. Using beam %d." % (fp_name, beam))

    ipols = (0, 3)

    freqs = obj.frequencies
    df = delta_freq
    f1, f2 = freqs[0], freqs[-1] - df
    frq = np.arange(f1, f2, df)
    ss = np.zeros((obj.Na, frq.shape[0]))
    i = 0
    for fr in frq:
        i1 = bsect(freqs, fr)
        i2 = bsect(freqs, fr + df)
        fslice = slice(i1, i2)
        msk = obj.flags[0, :, beam, ipols[0], fslice]
        arr = np.ma.masked_array(obj.data[0, :, beam, ipols[0], fslice], mask=msk)
        for j in range(obj.Na):
            ss[j, i] = np.ma.median(arr[j, :, 0])
            # ss[j, i] = find_mode(arr[j, :, 0])
        i += 1

    return frq + df / 2.0, ss


def plot_all(all_data, label):
    kw1 = {'label': 'geometric mean'}
    kw2 = {'label': 'median'}
    for k in all_data.keys():
        frq, ss = all_data[k]
        tt = np.ma.masked_array(ss * 113.1 / (1380.0 * 2), mask=(np.isnan(ss)))
        tt = np.ma.masked_less(tt, 25.0)
        # for a in range(ss.shape[0]):
        #     plt.plot(frq, tt[a, :], '-k', lw=0.3)
        a_gmean = np.array([ssm.gmean(tt[:, i]) for i in range(tt.shape[1])])
        a_median = np.array([np.ma.median(tt[:, i]) for i in range(tt.shape[1])])
        a_gmean = np.ma.masked_less(a_gmean, 25.0)
        a_median = np.ma.masked_less(a_median, 25.0)
        # plt.plot(frq, a_gmean, '-r', **kw1)
        plt.plot(frq, a_median, '-b', **kw2)
        kw1['label'] = None
        kw2['label'] = None
        # for j in range(a_median.shape[0]):
        #     print frq[j], a_median[j]

    tit = 'Tsys/eff SBs: %s' % (','.join(["%d" % a for a in all_data.keys()]))
    if label:
        ax = plt.gca()
        plt.text(0.03, 0.98, label, transform=ax.transAxes,
                 fontsize=11, fontweight='bold', va='top')
    plt.title(tit)


def plot_end(plot_file):
    plt.ylim(40.0, 120.0)
    # plt.legend()
    plt.xlabel('Frequency (MHz)')
    plt.ylabel('Tsys/eff (K)')
    plt.grid()
    plt.savefig(plot_file, dpi=300)


def main():
    logging.info('started')
    args = arg_init().parse_args()
    if args.verbose:
        print("ARGS = ", args)
    if args.explain:
        print(explanation)
        return
    do_show = args.display
    delta_f = args.f_delta
    label = args.label
    # Set a reasonable lower limit.
    delta_f_lower = 1.0 / 54
    if delta_f < delta_f_lower:
        delta_f = delta_f_lower
        logging.info("Setting freq averaging interval to %.2f MHz" % delta_f)

    all_data = {}
    sbids = args.sbid
    sbid_str = "_".join(["{:d}".format(a) for a in sbids])
    if label:
        plot_file = "sefd_spec_{}_{}.png".format(sbid_str, label)
    else:
        plot_file = "sefd_spec_{}.png".format(sbid_str)

    for sbid in args.sbid:
        obj = bf.load_beamset_class('SEFD_{}.hdf5'.format(sbid))
        all_data[sbid] = gather_data(obj, delta_f, override_beam=args.o_beam)

    plt.clf()
    plot_all(all_data, label)
    plot_end(plot_file)
    if do_show:
        print('plt.show')
        plt.show()
    logging.info("written plot file : %s" % plot_file)
    logging.info('finished')


# ====END of process ================

if __name__ == "__main__":
    # Set up logging
    fmt = '%(asctime)s %(levelname)s  %(name)s %(message)s'
    logging.basicConfig(format=fmt, level=logging.INFO)
    sys.exit(main())
