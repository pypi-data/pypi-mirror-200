#!/usr/bin/env python
from __future__ import print_function

"""
sefd_summary
Produces the one-page summary plot of the ASKAP SEFD values.

 $Author: mcc381 $


"""
import sys
import argparse as ap
import matplotlib as mpl
from numpy.core.multiarray import ndarray

mpl.use('Agg')  # this line must precede pylab import to suppress display
import matplotlib.pyplot as plt  # noqa
from matplotlib.patches import Wedge  # noqa
from matplotlib.colors import rgb2hex  # noqa
import numpy as np  # noqa
from numpy import pi  # noqa
import scipy.optimize as op  # noqa

from askap.jira import Jira  # noqa
# noinspection PyPackageRequirements
from aces.obsplan.config import ACESConfig  # noqa
# noinspection PyPackageRequirements
import aces.beamset.beamfactory as bf  # noqa
# noinspection PyPackageRequirements
import aces.display.ant_beam_pol_summary as abp  # noqa
import logging  # noqa
import time  # noqa

big = 1.0e+20


def arg_init():
    parser = ap.ArgumentParser(prog='sefd_summary', formatter_class=ap.RawDescriptionHelpFormatter,
                               description='',
                               epilog='See -x for more explanation')
    # noinspection PyTypeChecker
    parser.add_argument('sbid', type=int, help="SBID")
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-x', '--explain', action='store_true', help='give an expanded explanation')
    # noinspection PyTypeChecker
    parser.add_argument('-j', '--jira', metavar='ISSUE', type=str, help='post jira report to ISSUE')
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
    r = op.leastsq(errf, p0, args=(xx, yy))
    p1 = r[0]
    xf = np.linspace(min(xx), max(xx), 100)
    yf = [func(p1, x) for x in xf]
    res = 0.0
    for u, v in zip(xx, yy):
        res += errf(p1, u, v) ** 2
    res = res / len(xx)
    return p1, xf, yf, res


def find_mode(data, parameters):
    """
    Estimates and returns the mode of those input data that lie within the limits set by the parameters.
    The mode is determined by fitting a guassian function to the peak of the histogram of the logarithms of
    the values.

    :param data: np.array of real values
    :param parameters: dictionary giving the data value bounds
    :return:
    """

    diag_plot = False

    lower = parameters['lower']
    upper = parameters['upper']
    if data.max() < lower:
        return lower
    if data.min() > upper:
        return upper
    cdata = data.compressed()
    if len(cdata) > 0:
        hist_range = (np.log(lower), np.log(upper))
        histdata = np.histogram(np.log(cdata), bins=100, range=hist_range)

        hy = np.array(histdata[0])  # type: ndarray
        hx = np.array(histdata[1])
        hxc = (hx[:-1] + hx[1:]) / 2
        imode = np.where(hy == hy.max())[0][0]
        fit_wid = 5
        i1, i2 = max(0, imode - fit_wid), imode + fit_wid
        p0 = [hy.max(), hxc[imode], 0.3]
        rfit = fit_g(hxc[i1:i2], hy[i1:i2], p0)
        if diag_plot:
            pfile = 'modefit_%f.png' % time.time()
            tf, ax = plt.subplots()
            ax.plot(hxc, hy)
            ax.plot(rfit[1], rfit[2])
            plt.xlim(7.0, 9.0)
            tf.savefig(pfile)
            plt.close(tf)
        return np.exp(rfit[0][1])
    else:
        return -1.0


def dual_half_circle(center, radius, angle=0, ax=None, colors=('w', 'k'),
                     **kwargs):
    """
    Add two half circles to the axes *ax* (or the current axes) with the
    specified facecolors *colors* rotated at *angle* (in degrees).
    """
    if ax is None:
        ax = plt.gca()
    theta1, theta2 = angle, angle + 180
    w1 = Wedge(center, radius, theta1, theta2, ec='none', fc=colors[0], **kwargs)
    w2 = Wedge(center, radius, theta2, theta1, ec='none', fc=colors[1], **kwargs)
    for wedge in [w1, w2]:
        ax.add_artist(wedge)
    return [w1, w2]


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


def get_footprint_pa_zero(name, pitch):
    aces_cfg = ACESConfig()
    fp_factory = aces_cfg.footprint_factory
    # Catch the single beam footprint, which may have zero pitch, disallowed by the footprint factory.
    if pitch == 0.0:
        pitch = 1.0
    fp = fp_factory.make_footprint('ak:' + name, pitch * pi / 180, 0.0)
    return fp


def make_cmap(ssl, ssu):
    # This colour map puts a break 2/3 of the way up from the "hot" scale to blue.
    r0 = 0.0416
    br = 0.98
    b1 = br * 0.365079
    b2 = br * 0.746032
    b3 = br * 1.01
    revtup1 = ((0.0, r0, r0), (b1, 1.0, 1.0), (br, 1.0, 1.0), (b3, 0.8, 0.8), (1.0, 0.8, 0.8))
    revtup2 = ((0.0, 0.0, 0.0), (b1, 0.0, 0.0), (b2, 0.9, 0.9), (br, 0.9, 0.9), (b3, 0.8, 0.8), (1.0, 0.8, 0.8))
    revtup3 = ((0.0, 0.0, 0.0), (b2, 0.0, 0.0), (br, 0.9, 0.9), (b3, 1.0, 1.0), (1.0, 1.0, 1.0))

    cdict = {'red': revtup1, 'green': revtup2, 'blue': revtup3}
    cmap = mpl.colors.LinearSegmentedColormap('my_colormap', cdict, N=256)

    norm = mpl.colors.Normalize(vmin=ssl, vmax=ssu)
    return cmap, norm


def main():
    logging.info('started')
    args = arg_init().parse_args()
    if args.verbose:
        print("ARGS = ", args)

    jira_issue = args.jira

    # These values correspond to Tsys/eff = 60K and 120K
    sefd_scale_range = [1465., 2931.]
    ssl, ssu = sefd_scale_range
    cmap, norm = make_cmap(ssl, ssu)
    kwargs = {'label': 'SEFD (Jy)', 'cmap': cmap,
              'cnorm': norm,
              'minmax': [0.0, 5000.0],
              'annotations': []}
    for sbid in [args.sbid]:
        plot_file = None

        try:
            meth = find_mode
            params = {'lower': 500., 'upper': 20000.}
            obj = bf.load_beamset_class('SEFD_{}.hdf5'.format(sbid))
            if 'difference' in obj.metadata:
                kwargs['annotations'].append("Difference in " + obj.metadata['difference'])
            fig = abp.make_summary_plot(obj, meth, params, **kwargs)
            plot_file = 'SEFD_%d_summary.png' % sbid
            fig.savefig(plot_file, dpi=300)
            logging.info("written plot file : %s" % plot_file)

        except ValueError as ve:
            print ("Footprint name or jira problem?", ve)
        finally:
            if args.jira:
                jira = Jira()
                jira.authenticate()
                if plot_file:
                    jira.add_attachment(jira_issue, plot_file)
                    jira.add_comment(jira_issue, 'SEFD results for *SB{}*:\n!{}|thumbnail!'.format(sbid, plot_file))
                else:
                    jira.add_comment(jira_issue, 'Failed to produce SEFD summary for *SB{}*'.format(sbid))
                del jira

    logging.info('finished')


# ====END of process ================

if __name__ == "__main__":
    # Set up logging
    fmt = '%(asctime)s %(levelname)s  %(name)s %(message)s'
    logging.basicConfig(format=fmt, level=logging.INFO)
    sys.exit(main())
