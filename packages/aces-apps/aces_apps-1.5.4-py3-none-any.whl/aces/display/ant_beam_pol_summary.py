#!/usr/bin/env python
from __future__ import print_function

"""
sefd_summary
Produces the one-page summary plot of the ASKAP SEFD values.

 $Author: mcc381 $


"""
import matplotlib as mpl
mpl.use('Agg')  # this line must precede pyplot import to suppress display

import matplotlib.pyplot as plt  # noqa
from matplotlib.patches import Wedge  # noqa
import matplotlib.patches as mpatches  # noqa
from matplotlib.colors import rgb2hex  # noqa
import numpy as np  # noqa
from numpy import pi  # noqa
from scipy.stats import gmean  # noqa
from aces.obsplan.config import ACESConfig  # noqa


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
    Uses the bisection method to find j such that x[j] <= z < x[j+1]

    :param x: array with values in increasing order
    :param z: value to locate
    :return: j such that x[j] <= z < x[j+1]
  """
    n = len(x)
    if n == 0:
        return 0
    j1 = 0
    j2 = n
    j = j1
    while (j2 - j1) > 1:
        j = (j1 + j2) // 2
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


def get_stats_strings(data_in):
    data = np.ma.masked_invalid(data_in)
    if data.count() == 0:
        return '--', '--', '--'
    try:
        logm = int(round(np.log10(data.mean())))
    except:
        logm = 0
    try:
        logs = int(round(np.log10(data.std())))
    except:
        logs = 0
    nfigm = max(0, (2 - logm))
    nfigs = max(0, (1 - logs))
    minmax_fmt = "$%%.%df$" % nfigm
    meansd_fmt = "${{:.{:d}f}} \pm {{:.{:d}f}} $".format(nfigm, nfigs)

    valmin = minmax_fmt % (data.min())
    if data.mean() < 99999.:
        valmsd = meansd_fmt.format(data.mean(), data.std())
    else:
        valmsd = "> 99999"
    if data.max() < 99999.:
        valmax = minmax_fmt % (data.max())
    else:
        valmax = "> 99999"
    return valmin, valmsd, valmax


def make_summary_plot(obj, r_method, r_parameters, frq_select=None, **kwargs):
    """
    Makes a graphical summary of some beam-specific quantity across the whole array. The routine needs to
    use a single scalar quantity for each of two polarisations (XX, YY) for each beam, for each antenna.
    The input object must be of a subclass of BeamSet, and may hold a spectrum of quantities.  This spectrum is
    reduced to a single scalar by the passed method 'r_method' with parameters 'r_parameters'.

    :param obj:     Object derived from BeamSet
    :param r_method: method to reduce a spectrum of values to a single scalarL r_method(spectrum, r_parameters)
    :param r_parameters: parameters of r_method
    :param frq_select: lower and upper limits of scalar values to be colour-coded
    :param kwargs:

    :return:

    """
    if frq_select is None:
        frq_select = []

    # set defaults
    class Par(object):
        pass

    par = Par()
    par.label = 'label'
    par.cmap = 'hsv'
    par.cnorm = mpl.colors.Normalize()
    par.minmax = None
    par.annotations = []

    # par = {'label':'label',
    #         'cmap':'hsv',
    #         'norm': mpl.colors.Normalize()}
    for key, val in kwargs.items():
        if hasattr(par, key):
            setattr(par, key, val)
        else:
            print('unknown arg %s' % key)

    cm = plt.get_cmap(par.cmap)

    sbid = obj.metadata['calSBID']

    fp_name = obj.metadata['fp_name']
    fp_pitch = obj.metadata['fp_pitch'] * pi / 180.0
    freqs = obj.frequencies
    if len(frq_select) == 2:
        i1 = bsect(freqs, frq_select[0])
        i2 = bsect(freqs, frq_select[1])
        print ('from bsect: ', i1, i2)
        fslice = slice(i1, i2)
        freqs = obj.frequencies[fslice]
    else:
        fslice = slice(0, None)

    antennas = obj.metadata['antennas']
    if 'beam_weights' in obj.metadata:
        bw_lab = "Beam weights {}".format(obj.metadata['beam_weights'])
    else:
        bw_lab = 'Beamforming SBID {:d}'.format(obj.metadata['beamformingSBID'])

    ipols = (0, obj.Np - 1)

    # fp = obj.beams
    fp = get_footprint_pa_zero(fp_name, fp_pitch)

    offsets = np.degrees(np.array(fp.offsetsRect))
    xo, yo = [], []
    for ib in obj.metadata['beams']:
        xo.append(offsets[ib][0] * -1)
        yo.append(offsets[ib][1])
    xo = np.array(xo) * 180. / pi
    yo = np.array(yo) * 180. / pi
    # Corrected to display beams in the correct location, even if some are missing.
    # The offsets are used according to the beam index, not a running counter.

    nants = obj.get_container_shape()[1]
    nbeams = obj.get_container_shape()[2]

    # force finite radius to deal wtih boresight footprint pitch == 0
    if nbeams > 1:
        rad = fp_pitch / 2. * 180.0 / pi
    else:
        rad = 1.

    scalars_all = np.ma.array(np.zeros((nants, nbeams, 2)), shrink=False)

    msk = obj.flags[0, :, :, ipols[0], fslice].squeeze()
    arr = np.ma.masked_array(obj.data[0, :, :, ipols[0], fslice].squeeze(), mask=msk)
    if nbeams > 1:
        arrmin = arr.min(axis=0).min(axis=0)
        arrmedian = np.percentile(arr, 50, axis=[0, 1])
    else:
        # single beam case
        arrmin = np.abs(arr).min(axis=0)
        arrmedian = np.percentile(arr, 50, axis=0)

    for iant in range(nants):
        for ip in [0, 1]:
            msk = obj.flags[0, iant, :, ipols[ip], fslice]
            arr = np.ma.masked_array(obj.data[0, iant, :, ipols[ip], fslice], mask=msk)
            if nbeams > 1:

                scalars = []
                for i, d in enumerate(arr):
                    r_parameters['label'] = "_{:d}_{:d}_{:d}".format(iant, ip, i)
                    scalars.append(r_method(d, r_parameters))
                scalars = np.array(scalars)
                # scalars = np.array([r_method(d, r_parameters) for d in arr])
            else:
                scalars = np.array([r_method(arr, r_parameters)])
            scalars = np.ma.array(scalars, mask=(scalars == -1.0))
            scalars_all[iant, :, ip] = scalars.copy()

    # Initialize the plotting
    figsize = (8.27, 11.69)
    fig = plt.figure(figsize=figsize)

    asizx, asizy = 44., 48.
    margin_l = 0.05
    margin_b = 0.05
    margin_l4 = 0.05
    margin_b4 = 0.03
    gutter = 0.03
    wid = 0.9
    height1 = wid * figsize[0] / figsize[1]
    height2 = 0.02
    height3 = 0.95 - height1 - height2 - margin_b
    height4 = height3 - margin_b4
    wid1 = wid
    wid2 = wid
    wid3 = wid / 2 - gutter / 2
    wid4 = wid3 - margin_l4

    ax1 = fig.add_axes([margin_l, margin_b + height2, wid1, height1])
    ax2 = fig.add_axes([margin_l, margin_b, wid2, height2])
    ax3 = fig.add_axes([margin_l, margin_b + height1 + height2, wid3, height3])
    ax4 = fig.add_axes([margin_l + wid3 + gutter + margin_l4, margin_b + height1 + height2 + margin_b4, wid4, height4])

    laboff = [-3.0, 3.1]
    valoff = [2.0, -0.5, 0.5]

    for iant, ant in enumerate(antennas):
        n = (ant - 1) // 6
        m = ant - 1 - 6 * n
        x0 = (m + 0.5) * asizx / 6
        y0 = (n + 0.5) * asizy / 6
        scalars_listed = []
        scalars_x = scalars_all[iant, :, 0]
        scalars_y = scalars_all[iant, :, 1]
        for xi, yi, sx, sxm, sy, sym in zip(xo, yo, scalars_x, scalars_x.mask, scalars_y, scalars_y.mask):
            if not (sxm and sym):
                colx = rgb2hex(cm(par.cnorm(sx)))
                coly = rgb2hex(cm(par.cnorm(sy)))

                xj = xi + x0
                yj = yi + y0 - 0.5
                dual_half_circle((xj, yj), rad, ax=ax1, angle=45, colors=(colx, coly))
                scalars_listed.append((sx, sy))

        scalars_all_beams = np.array(scalars_listed)
        ax1.set_xlim(0, asizx)
        ax1.set_ylim(0, asizy)
        labx, laby = x0 + laboff[0], y0 + laboff[1]
        lab = "AK%02d" % ant
        valmin, valmsd, valmax = get_stats_strings(scalars_all_beams)
        ax1.text(labx, laby, lab, fontsize=9)
        ax1.text(labx + valoff[0], laby + valoff[1], valmin, fontsize=6)
        ax1.text(labx + valoff[0], laby, valmsd, fontsize=6)
        ax1.text(labx + valoff[0], laby + valoff[2], valmax, fontsize=6)

    ax1.axis('off')

    # Plot key

    x0 = 0.12
    y0 = 0.1
    radk = 0.01
    fac = 1.0 / asizx
    ib = 0
    for xi, yi in zip(xo, yo):
        xj = xi * fac + x0
        yj = yi * fac + y0
        circle = mpatches.Circle((xj, yj), radk, ec='k', fc="none", lw=0.1)
        ax3.add_artist(circle)

        jb = obj.metadata['beams'][ib]
        ax3.text(xj, yj, '%d' % jb, fontsize=6, va='center', ha='center')
        ib += 1

    # Plot array-wide quantity
    scalars_listed = []
    array_wide_x = gmean(scalars_all[:, :, 0], axis=0)
    array_wide_y = gmean(scalars_all[:, :, 1], axis=0)

    x0 = 0.33
    y0 = 0.1

    for xi, yi, sx, sy in zip(xo, yo, array_wide_x, array_wide_y):
        colx = rgb2hex(cm(par.cnorm(sx)))
        coly = rgb2hex(cm(par.cnorm(sy)))

        xj = xi * fac + x0
        yj = yi * fac + y0
        dual_half_circle((xj, yj), radk, ax=ax3, angle=45, colors=(colx, coly))
        scalars_listed.append((sx, sy))

    scalars_all_beams = np.array(scalars_listed)
    labx, laby = x0 + laboff[0] * fac, y0 + laboff[1] * fac
    lab = "ALL"
    valmin, valmsd, valmax = get_stats_strings(scalars_all_beams)

    ax3.text(labx, laby, lab, fontsize=9)
    ax3.text(labx + valoff[0] * fac, laby + valoff[1] * fac, valmin, fontsize=6)
    ax3.text(labx + valoff[0] * fac, laby, valmsd, fontsize=6)
    ax3.text(labx + valoff[0] * fac, laby + valoff[2] * fac, valmax, fontsize=6)

    # noinspection PyUnresolvedReferences
    cb1 = mpl.colorbar.ColorbarBase(ax2, cmap=cm,
                                    norm=par.cnorm,
                                    orientation='horizontal')
    cb1.set_label(par.label)

    ax3.set_xlim(0.0, wid3)
    ax3.set_ylim(0.0, height3 * figsize[1] / figsize[0])

    lx, ly = 0.02, 0.32
    ax3.text(lx, ly, fp_name)
    ax3.text(lx, ly - 0.025, bw_lab, fontsize=8)
    ly -= 0.025*2
    dy = 0.02
    for i, ann in enumerate(par.annotations):
        ax3.text(lx, ly - i * dy, ann, fontsize=8)

    kx, ky = 0.35, 0.25
    dual_half_circle((kx, ky), 0.01, ax=ax3, angle=45, colors=('k', 'r'))
    ax3.text(kx - 0.03, ky + 0.01, 'XX', ha='center', va='center', fontsize=8)
    ax3.text(kx + 0.03, ky - 0.01, 'YY', ha='center', va='center', fontsize=8)
    ax3.tick_params(
        axis='x',  # changes apply to the x-axis
        which='both',  # both major and minor ticks are affected
        bottom='off',  # ticks along the bottom edge are off
        top='off',  # ticks along the top edge are off
        labelbottom='off')  # labels along the bottom edge are off
    ax3.tick_params(
        axis='y',  # changes apply to the y-axis
        which='both',  # both major and minor ticks are affected
        left='off',  # ticks along the bottom edge are off
        right='off',  # ticks along the top edge are off
        labelleft='off')  # labels along the bottom edge are off

    plt.sca(ax4)
    ax4.tick_params(axis='both', which='major', labelsize=8)
    plt.plot(freqs, arrmin, c='k', label='minimum')
    plt.plot(freqs, arrmedian, c='r', label='median')

    if par.minmax is None:
        use_min = min(arrmedian.min(), min(arrmin.min(), 0.0))
        use_max = max(arrmedian.max(), arrmedian.max())
    else:
        use_min, use_max = par.minmax
    plt.ylim(use_min, use_max)
    plt.xlabel('Frequency (MHz)')
    plt.ylabel(par.label)
    plt.legend()
    plt.grid()

    fig.suptitle('SBID = %d' % sbid, fontsize=24)
    return fig
