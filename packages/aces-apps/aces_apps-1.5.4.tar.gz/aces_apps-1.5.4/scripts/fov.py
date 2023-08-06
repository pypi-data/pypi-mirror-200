#!/usr/bin/env python
from __future__ import print_function

"""
fov
Models the ASKAP PAF field of view from SEFD values.

 $Author: mcc381 $


"""
import sys
import argparse as ap
import matplotlib as mpl
mpl.use('Agg')  # this line must precede pylab import to suppress display
import matplotlib.pyplot as plt  # noqa
from matplotlib.patches import Wedge  # noqa
import numpy as np  # noqa
from numpy import pi  # noqa
import scipy.optimize as op  # noqa
from scipy.interpolate import interp1d, interp2d, griddata, RectBivariateSpline  # noqa
from aces.obsplan.config import ACESConfig  # noqa
import aces.beamset.beamfactory as bf  # noqa
import logging  # noqa

big = 1.0e+20


def arg_init():
    parser = ap.ArgumentParser(prog='fov', formatter_class=ap.RawDescriptionHelpFormatter,
                               description='',
                               epilog='See -x for more explanation')
    parser.add_argument('sbid', nargs="+", type=int, help="SBID")
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
    fp = fp_factory.make_footprint('ak:'+name, pitch * pi / 180, 0.0)
    return fp


class Grid(object):
    def __init__(self, grid_size, x0, x1, y0, y1):
        self.npnts = grid_size
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1
        self.extent = [self.x0, self.x1, self.y0, self.y1]
        self.x = np.linspace(self.x0, self.x1, self.npnts)
        self.y = np.linspace(self.y0, self.y1, self.npnts)
        self.xgrid, self.ygrid = np.meshgrid(self.x, self.y)


def assemble_data(obj, grid, f_limits=None):
    """

    :param obj:
    :param f_limits:
    """
    if f_limits is None:
        f_limits = []
    # sbid = obj.metadata['calSBID']
    #
    # fp_name = obj.metadata['fp_name']
    # fp_pitch = obj.metadata['fp_pitch'] * pi / 180.0
    freqs = obj.frequencies
    if len(f_limits) == 2:
        i1 = bsect(freqs, f_limits[0])
        i2 = bsect(freqs, f_limits[1])
        print('from bsect: ', i1, i2)
        fslice = slice(i1, i2)
        freqs = obj.frequencies[fslice]
    else:
        fslice = slice(0, None)

    antennas = obj.metadata['antennas']
    ipols = (0, 3)

    fp = obj.beams

    offsets = np.degrees(np.array(fp.offsetsRect))
    xo, yo = [], []
    for ib in obj.metadata['beams']:
        xo.append(offsets[ib][0] * -1)
        yo.append(offsets[ib][1])
    xo = np.array(xo)
    yo = np.array(yo)
    xyo = np.array((xo, yo)).transpose()

    # Corrected to display beams in the correct location, even if some are missing.
    # The offsets are used according to the beam index, not a running counter.

    nants = obj.get_container_shape()[1]
    nbeams = obj.get_container_shape()[2]

    msk = obj.flags[0, :, :, ipols[0], fslice].squeeze()
    arr = np.ma.masked_array(obj.data[0, :, :, ipols[0], fslice].squeeze(), mask=msk)
    zgrids = {}
    for iant in range(nants):
        ant = antennas[iant]

        msk = obj.flags[0, iant, :, ipols[0], fslice]
        arr = np.ma.masked_array(obj.data[0, iant, :, ipols[0], fslice], mask=msk)
        if nbeams > 1:
            sefdx = np.array([find_mode(d) for d in arr])
        else:
            sefdx = np.array([find_mode(arr)])
        sefdx = np.ma.array(sefdx, mask=(sefdx == -1.0))

        msk = obj.flags[0, iant, :, ipols[1], fslice]
        arr = np.ma.masked_array(obj.data[0, iant, :, ipols[1], fslice], mask=msk)
        if nbeams > 1:
            sefdy = np.array([find_mode(d) for d in arr])
        else:
            sefdy = np.array([find_mode(arr)])
        sefdy = np.ma.array(sefdy, mask=(sefdy == -1.0))

        pnts = xyo
        sefdxmin = sefdx.min()
        sensx = sefdxmin/sefdx
        sefdymin = sefdy.min()
        sensy = sefdymin/sefdy
        # sensx = sefdx
        zgrid = griddata(pnts, sensy, (grid.xgrid, grid.ygrid), method='cubic', fill_value=0.0)
        zgrids[ant] = np.ma.array(zgrid, mask=(zgrid==0.0))

    return zgrids


def make_plot(grid, zgrids):
    """

    :param grid:
    :param zgrids:
    """
    sbids = zgrids.keys()
    antennas = set()
    for sb in sbids:
        antennas.update(zgrids[sb].keys())
    ipols = (0, 3)
    # These values correspond to Tsys/eff = 60K and 120K
    sefd_scale_range = [1465., 2931.]
    ssl, ssu = sefd_scale_range

    # fp = obj.beams
    # fp = get_footprint_pa_zero(fp_name, fp_pitch)

    asizx, asizy = 44., 48.
    figsize = (8.27, 11.69)

    # Initialize the plotting
    plt.clf()
    fig = plt.gcf()
    fig.set_size_inches(figsize)

    laboff = [-3.0, 3.1]
    valoff = [2.0, -0.5, 0.5]
    # noinspection PyUnresolvedReferences
    cmap = mpl.cm.hot

    # This colour map puts a break 2/3 of the way up from the "hot" scale to blue.
    # r0 = 0.0416
    # br = 0.98
    # b1 = br * 0.365079
    # b2 = br * 0.746032
    # b3 = br * 1.01
    # revtup1 = ((0.0, r0, r0), (b1, 1.0, 1.0), (br, 1.0, 1.0), (b3, 0.8, 0.8), (1.0, 0.8, 0.8))
    # revtup2 = ((0.0, 0.0, 0.0), (b1, 0.0, 0.0), (b2, 0.9, 0.9), (br, 0.9, 0.9), (b3, 0.8, 0.8), (1.0, 0.8, 0.8))
    # revtup3 = ((0.0, 0.0, 0.0), (b2, 0.0, 0.0), (br, 0.9, 0.9), (b3, 1.0, 1.0), (1.0, 1.0, 1.0))
    #
    # cdict = {'red': revtup1, 'green': revtup2, 'blue': revtup3}
    # cmap = mpl.colors.LinearSegmentedColormap('my_colormap', cdict, N=256)
    # #
    # norm = mpl.colors.Normalize(vmin=ssl, vmax=ssu)
    #

    for ant in antennas:
        print ("ant = %d  %s" % (ant, sbids))
        row = 5 - (ant - 1)/6
        col = (ant - 1) % 6
        ip = row * 6 + col + 1

        z = zgrids[sbids[0]][ant]
        for sb in sbids[1:]:
            if ant in zgrids[sb]:
                z = np.ma.dstack((z, zgrids[sb][ant]))
        ax = fig.add_subplot(6, 6, ip)
        plt.imshow(z.mean(axis=2), origin='lower', extent=grid.extent, cmap=cmap)
        # plt.plot(z.mean(axis=2)[:,95])
        # plt.ylim(0.0, ssu)
        plt.grid()
        plt.title("AK%02d" % ant)
        if row < 5:
            ax.set_xticklabels([], visible=False)
        if col > 0:
            ax.set_yticklabels([], visible=False)
        # plt.plot(z[100,:,0])
        # plt.plot(z[100,:,1])
        # plt.plot(z[100,:,:].mean(axis=1))
        # CS = plt.contour(xr, yr, zgrid)

    ax = fig.add_subplot(18, 1, 1)
    # noinspection PyUnresolvedReferences
    cb1 = mpl.colorbar.ColorbarBase(ax, cmap=cmap,
                                    # norm=norm,
                                    orientation='horizontal')
    cb1.set_label('Normalised sensitivity')

    pfile = 'SEFD_%d_fov.png' % sbids[0]
    fig.suptitle('SBID = %d' % sbids[0], fontsize=24)
    plt.savefig(pfile, dpi=300)
    logging.info("written plot file : %s" % pfile)

    return pfile


def main():
    logging.info('started')
    args = arg_init().parse_args()
    if args.verbose:
        print ("ARGS = ", args)

    xomin = -4.0
    xomax = +4.0
    yomin = -4.0
    yomax = +4.0
    gridsize = 191
    the_grid = Grid(gridsize, xomin, xomax, yomin, yomax)

    all_zgrids = {}
    for sbid in args.sbid:
        obj = bf.load_beamset_class('SEFD_{}.hdf5'.format(sbid))
        gr = assemble_data(obj, the_grid)
        print (len(gr))
        all_zgrids[sbid] = gr

    plot_file = make_plot(the_grid, all_zgrids)

    # try:
    #     obj = bf.load_beamset_class('SEFD_{}.hdf5'.format(sbid))
    #     plot_file = make_summary_plot(obj)
    # except ValueError as ve:
    #     print "Footprint name or jira problem?", ve
    # finally:
    #     if args.jira:
    #         jira = Jira()
    #         jira.authenticate()
    #         if plot_file:
    #             jira.add_attachment('ACES-333', plot_file)
    #             jira.add_comment('ACES-333', 'SEFD results for *SB{}*:\n!{}|thumbnail!'.format(sbid, plot_file))
    #         else:
    #             jira.add_comment('ACES-333', 'Failed to produce SEFD summary for *SB{}*'.format(sbid))
    #         del jira

    logging.info('finished')


# ====END of process ================

if __name__ == "__main__":
    # Set up logging
    fmt = '%(asctime)s %(levelname)s  %(name)s %(message)s'
    logging.basicConfig(format=fmt, level=logging.INFO)
    sys.exit(main())
