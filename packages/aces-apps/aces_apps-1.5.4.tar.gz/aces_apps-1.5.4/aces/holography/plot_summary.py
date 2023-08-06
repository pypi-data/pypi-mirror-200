#!/usr/bin/env python3

import numpy as np
import os
import sys
import time
import argparse as ap
import pkg_resources

import matplotlib as mpl

from aces.obsplan.config import ACESConfig
from aces.askapdata.schedblock import SchedulingBlock

from aces import holography
from aces.holography import clean_holography as clh

from aces.beamset.mapset import MapSet

import scipy.interpolate as sp
import aces.beamset.beamfactory as bf
from aces.holography import holo_filenames as hf
from astropy.io import fits
import logging

log = logging.getLogger(__name__)

mpl.use('Agg')  # this line must precede pylab import to suppress display

import matplotlib.pylab as plt
from matplotlib.ticker import MultipleLocator

aces_cfg = ACESConfig()
fp_factory = aces_cfg.footprint_factory

explanation = """ Fill this"""


def arg_init():
    code_path = os.path.dirname(os.path.abspath(holography.__file__))
    log.debug(f'Code path = {code_path}')
    parser = ap.ArgumentParser(prog='plot_summary', formatter_class=ap.RawDescriptionHelpFormatter,
                               description='Plot summary of processed holography data',
                               epilog='See -x for more explanation',
                               fromfile_prefix_chars='@')
    parser.add_argument('sbid', metavar='sbid', type=int,
                        help='SBID of processed holography (stored in HDF5) [no default].')
    parser.add_argument('-d', dest='holo_dir', type=str, default='.', help='Directory containing holography data [.].')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-x', '--explain', action='store_true', help="give an expanded explanation")
    return parser


def linmos(beams, beams_i, cutoff=0.1):
    # Expect beams in array shape (nb,nx,ny)
    weight = beams_i ** 2
    mask = beams_i < cutoff
    beams[mask] = np.nan
    weight[mask] = np.nan
    mos = np.nansum(beams * weight, axis=0) / np.nansum(weight, axis=0)
    return mos


def beam_mosaic(beams):
    # Expect beams in array shape (nb,nx,ny)
    inv = beams ** 2
    g = np.nansum(inv, axis=0)
    sen = np.sqrt(g)
    return sen


def key_axis(fig, dx, dy, wd, ht):
    """
    Returns a new axis whose position is given relative to the plotted area as recorded in fig.subplotpars.
    This is used after a call to plt.subplots or equivalent. The returned axis is convenient for placing keys
    or explanations related to the plotted data.
    :param fig: Parent figure
    :param dx: Left position  of new axis relative to that of plotted area
    :param dy: Bottom position  of new axis relative to the TOP of plotted area
    :param wd: Width of new axis
    :param ht: Height of new axis
    :return: new axis
    """
    x0, y0 = fig.subplotpars.left, fig.subplotpars.top
    kb = mpl.transforms.Bbox.from_bounds(x0 + dx, y0 + dy, wd, ht)

    k_ax = fig.add_axes(kb)
    k_ax.set_xlim(0.0, 1.0)
    k_ax.set_ylim(0.0, 1.0)
    k_ax.axis('off')
    return k_ax


def get_target(sbid):
    try:
        sb = SchedulingBlock(sbid)
        target = sb.get_parameters()['common.target.src1.field_name']
    except:
        target = "unknown"
    return target


def get_ms_size(fig, ax, size):
    """
    Returns a marker size corresponding to the current axis scale and requested size.
    It is assumed that the axis aspect ratio is 1.0, and the scaling is computed using the x world and
    display coordinates.  If the aspect ratio is not 1.0, the marker will be scaled correctly in the horizontal
    direction only.
    :param fig: Current matplotlib figure
    :param ax: Current matplotlib axis
    :param size: Required size of marker in "world" coordinates
    :return: Marker size
    """
    ax_pos = ax.get_position()
    x1, x2 = ax.get_xlim()
    xpix = fig.dpi * fig.get_size_inches()[0]
    xscale = np.abs(x2 - x1) / (ax_pos.x1 - ax_pos.x0) / xpix
    return size / xscale


def plot_beampos_errors(mapset, remove_mean, channel, tt=False, plot_file_name=None):
    """

    :param mapset: Mapset object holding beam position offsets
    :param remove_mean: If True, subtract vector mean of beam errors before plotting
    :param channel:
    :param tt:
    :param plot_file_name: Output file name
    """

    chan = channel
    sbid = mapset.metadata['holographySBID']

    beam_pos = mapset.get_beam_offsets()
    beam_pos_errs = mapset.data[0, :, :, 0, chan, :2]
    n_ants, n_beams = beam_pos_errs.shape[:2]
    nx, ny = 0, 0
    if n_ants == 36:
        nx, ny = 6, 6
    elif n_ants == 1:
        nx, ny = 1, 1
    else:
        log.info("Case of {:d} antennas not handled".format(n_ants))

    poss = beam_pos
    shiftsd = np.degrees(beam_pos_errs)

    fig, ax = plt.subplots(nx, ny, figsize=(15.5, 16.), squeeze=False, sharex='col', sharey='row')
    plt.subplots_adjust(wspace=0.04, hspace=0.04)
    if n_ants == 36:
        qu_kw = {'width': 0.008, 'headwidth': 4, 'headlength': 5, 'headaxislength': 4.0, 'color': 'k', 'zorder': 10}
        qu_kwb = {'width': 0.02, 'headwidth': 3, 'headlength': 3, 'headaxislength': 2.0, 'color': 'b', 'zorder': 20}
        scale1 = 0.2
        scale2 = 0.075
        fs = 10
        beam_col = '0.9'

    elif n_ants == 1:
        qu_kw = {'width': 0.004, 'headwidth': 4, 'headlength': 5, 'headaxislength': 4.0, 'color': 'k', 'zorder': 10}
        qu_kwb = {'width': 0.01, 'headwidth': 3, 'headlength': 3, 'headaxislength': 2.0, 'color': 'b', 'zorder': 20}
        scale1 = 0.15
        scale2 = 0.075
        fs = 16
        beam_col = '0.9'

    for ant, axf in zip(range(n_ants), ax.flat):
        axf.set_aspect(1.0)
        shifts_mean = np.array([np.nan, np.nan])
        shifts_corr_mag_mean = np.nan
        shifts_corr_mag_std = np.nan

        valid = len(np.where(np.isnan(shiftsd[ant]))[0]) < (2 * n_beams)
        if valid:
            shifts_mean = np.nanmean(shiftsd[ant], axis=0)

        shifts_mean_mag = (shifts_mean ** 2).sum() ** 0.5
        shifts_mean_ang = np.degrees(np.arctan2(shifts_mean[0], shifts_mean[1]))
        shiftsdm = shiftsd[ant] - shifts_mean
        shifts_corr_mag = np.sqrt(shiftsdm[:, 0] ** 2 + shiftsdm[:, 1] ** 2)

        if valid:
            shifts_corr_mag_mean = np.nanmean(shifts_corr_mag)
            shifts_corr_mag_std = np.nanstd(shifts_corr_mag)

        if remove_mean:
            axf.quiver(poss[:, 0], poss[:, 1], shiftsdm[:, 0], shiftsdm[:, 1], angles='xy', scale_units='xy',
                       scale=scale1, **qu_kw)
            axf.quiver(0.0, 0.0, shifts_mean[0], shifts_mean[1], angles='xy', scale_units='xy', scale=scale2, **qu_kwb)
            if not np.isnan(shifts_corr_mag_std):
                axf.text(0.0, 2.9, "[{:.1f}±{:.1f}']".format(shifts_corr_mag_mean * 60., shifts_corr_mag_std * 60.),
                         ha='center', va='center', fontsize=fs)
                mag = shifts_mean_mag * 60.
                ang = shifts_mean_ang
                axf.text(0.0, -2.9, "[{:.1f}' {:+4.0f}]".format(mag, ang), ha='center', va='center', color='b',
                         fontsize=fs)
        else:
            axf.quiver(poss[:, 0], poss[:, 1], shiftsd[ant, :, 0], shiftsd[ant, :, 1], angles='xy', scale_units='xy',
                       scale=scale1, **qu_kw)
            if not np.isnan(shifts_corr_mag_std):
                axf.text(0.0, 2.9, "[{:.1f}±{:.1f}']".format(shifts_corr_mag_mean * 60., shifts_corr_mag_std * 60.),
                         ha='center', va='center', fontsize=fs)
        # Plot nominal beam positions
        beam_siz = get_ms_size(fig, axf, 3. / 60) / scale1
        axf.plot(poss[:, 0], poss[:, 1], 'o', c=beam_col, ms=beam_siz, zorder=1)
        axf.plot(poss[0, 0], poss[0, 1], 'or', ms=beam_siz)
        axf.plot(poss[0, 0], poss[0, 1], 'ok', ms=beam_siz * 1.4, mfc='none')
        if n_ants == 1:
            axf.text(3.0, 2.9, "Mean over antennas", va='center', fontsize=fs)
        else:
            axf.text(3.0, 2.9, "AK{:02d}".format(ant + 1), va='center', fontsize=fs)
        axf.set_xlim(3.3, -3.3)
        axf.set_ylim(-3.3, 3.3)

    slen = 6
    sup = "Beam position errors : "
    sup += " SBID {:d}".format(sbid)
    if tt:
        sup += "  TT0, {:.0f} MHz".format(mapset.frequencies[mapset.Nf // 2])
    else:
        sup += "  Chan {:d}, {:.0f} MHz".format(chan, mapset.frequencies[chan])
    if remove_mean:
        sup += "\nVector mean subtracted"
    fig.suptitle(sup, fontsize=18)

    bigax = fig.add_subplot(111, frameon=False)
    # hide tick and tick label of the big axis
    bigax.tick_params(labelcolor='none', which='both', top=False, bottom=False, left=False, right=False)
    bigax.set_xlabel("Beam offset (deg)", fontsize=16)
    bigax.set_ylabel("Beam offset (deg)", fontsize=16)

    y1, y2, y3 = 0.05, 0.2, 0.35
    k_fs = 12

    wd, ht = ax[0, 0].get_position().size[0], 0.125
    dx, dy = 0.25, 0.005

    x1 = 3.0
    x2 = x1 - 0.2
    k_ax = key_axis(fig, dx, dy, wd, ht)
    k_ax.set_xlim(ax[0, 0].get_xlim())
    k_ax.plot([x2, x2 - slen / 60. / scale1], [y2, y2], 'k', lw=2)
    k_ax.text(x1, y2, "{:d}'".format(slen), ha='right', va='center', fontsize=k_fs)
    if remove_mean:
        k_ax.plot([x2, x2 - slen / 60. / scale2], [y1, y1], 'b', lw=3)
        k_ax.text(x1, y1, "{:d}'".format(slen), ha='right', va='center', color='b', fontsize=k_fs)

    wd, ht = 0.125, 0.125
    dx, dy = 0.03, 0.005
    t_ax = key_axis(fig, dx, dy, wd, ht)

    t_ax.text(0.1, y2, 'Beam error [mean(mag),±sd(mag)]', va='center', fontsize=k_fs)
    if remove_mean:
        t_ax.text(0.1, y1, 'Vector mean [magnitude, PA]', color='b', va='center', fontsize=k_fs)

    dx, dy = 0.66, 0.005
    r_ax = key_axis(fig, dx, dy, wd, ht)
    r_ax.text(0.5, y3, "{}".format(mapset.metadata['fp_name']), va='center', ha='right', fontsize=k_fs)
    r_ax.text(0.5, y2, "Pitch {:.2f}".format(mapset.metadata['fp_pitch']), va='center', ha='right', fontsize=k_fs)
    r_ax.text(0.5, y1, 'Beam zero', va='center', ha='right', fontsize=k_fs)
    r_ax.plot(0.6, y1 + 0.01, 'or', ms=6)
    r_ax.plot(0.6, y1 + 0.01, 'ok', ms=12, mfc='none')

    tt = time.localtime(time.time())
    plot_date = time.strftime("%Y-%m-%d %H:%M:%S", tt)

    bbb = bigax.get_position()
    fig.text(bbb.x0, bbb.y0 - 0.04, 'Plot date {}'.format(plot_date), va='top')
    if plot_file_name:
        plt.savefig(plot_file_name, dpi=300, bbox_inches='tight')


def plot_valid_summary(mapset, plot_file_name=None):
    target = get_target(mapset.metadata['holographySBID'])

    flgs = np.array(mapset.flags)
    data = mapset.data
    sbid = mapset.metadata['holographySBID']
    frqs = mapset.frequencies

    flg_con = flgs[0, :, :, 0, :]

    disp = np.ma.masked_array(np.abs(data[0, :, :, 0, :].max(axis=(3, 4))), mask=flg_con) * 0.5
    npix = np.product(disp[0].shape)
    ext = [frqs[0], frqs[-1], 0, 35]

    fig, axes = plt.subplots(6, 6, figsize=(16., 15.), sharex='col', sharey='row')
    fig.subplots_adjust(wspace=0.04, hspace=0.04)
    bigax = fig.add_subplot(111, frameon=False)
    # Magic numbers to make the colorbar fit
    cbar_ax = fig.add_axes([0.91, 0.15, 0.02, 0.7])
    cm = plt.cm.get_cmap('YlOrRd')

    for a, ax in enumerate(axes.flat):
        ax.set_ylim(-1.0, 40.0)
        ax.xaxis.set_major_locator(MultipleLocator(100))
        ax.xaxis.set_minor_locator(MultipleLocator(25))

        ax.yaxis.set_major_locator(MultipleLocator(9))
        ax.yaxis.set_minor_locator(MultipleLocator(3))
        im = ax.imshow(disp[a], origin='lower', aspect='auto', cmap=cm, extent=ext, vmin=0.75, vmax=1.25)
        vfrac = int(disp[a].count() / npix * 100.0 + 0.5)
        ax.text(frqs[5], 36.5, 'AK{:02d}    {:d}%'.format(a + 1, vfrac), ha='left')
        ax.grid()

    cb = fig.colorbar(im, cax=cbar_ax, orientation='vertical')
    cb.ax.yaxis.set_ticks_position('right')
    cb.ax.yaxis.set_label_position('right')
    cbar_ax.set_ylabel('Beam maximum pixel')

    # hide tick and tick label of the big axis
    bigax.tick_params(labelcolor='none', which='both', top=False, bottom=False, left=False, right=False)
    bigax.set_xlabel("Frequency (MHz)", fontsize=14)
    bigax.set_ylabel("Beam", fontsize=14)

    y2, y3, y4 = np.linspace(1.05, 1.1, 3)
    xt = 0.9
    k_fs = 12

    r_ax = bigax
    r_ax.text(xt, y4, f"Target {target}", va='center', fontsize=k_fs)
    r_ax.text(xt, y3, "{}".format(mapset.metadata['fp_name']), va='center', fontsize=k_fs)
    r_ax.text(xt, y2, "Pitch {:.2f}".format(mapset.metadata['fp_pitch']), va='center', fontsize=k_fs)

    fig.suptitle('Valid data SBID {:d}'.format(sbid), fontsize=16)

    tt = time.localtime(time.time())
    plot_date = time.strftime("%Y-%m-%d %H:%M:%S", tt)

    bbb = bigax.get_position()
    fig.text(bbb.x0, bbb.y0 - 0.04, 'Plot date {}'.format(plot_date), va='top')

    if plot_file_name:
        fig.savefig(plot_file_name, dpi=300, bbox_inches='tight')


def plot_footprint_sensitivity(mapset, plot_file_name=None):
    sbid = mapset.metadata['holographySBID']
    target = get_target(sbid)

    frqs = mapset.frequencies
    data = MapSet.sky_transform_hyper(mapset.data)
    inx = np.degrees(mapset.xsi)
    outx = np.linspace(inx[0], inx[-1], 100)
    # da = (outx[1] - outx[0]) ** 2
    ext = [outx[-1], outx[0], outx[0], outx[-1]]
    cui = np.zeros([36, 100, 100])
    chans = range(3, 288, 18)

    fig, axes = plt.subplots(4, 4, figsize=(12., 12.), sharex='col', sharey='row')
    plt.subplots_adjust(hspace=0.02, wspace=0.02)
    bigax = fig.add_subplot(111, frameon=False)
    # Magic numbers to make the colorbar fit
    cbar_ax = fig.add_axes([0.91, 0.15, 0.02, 0.7])

    cm = plt.cm.get_cmap('YlOrRd')
    mos = []
    for ch in chans:
        cu = data[0, 0, :, 0, ch - 2:ch + 3].mean(axis=1)
        for b in range(36):
            fn = sp.RectBivariateSpline(inx, inx, cu[b], kx=2, ky=2)
            cui[b] = fn(outx, outx)
        mos.append(beam_mosaic(cui))
    mos = np.array(mos)

    global_max = mos.max()
    for i, ax in enumerate(axes.flat):
        im = ax.imshow(mos[i], origin='lower', cmap=cm, extent=ext, vmax=global_max)
        # lev = global_max / 2.0
        lev = 0.5
        ax.contour(-outx, outx, mos[i], levels=[lev], linewidths=1, colors='0.7')
        tx = outx[-1] * 0.95
        ch = chans[i]
        ax.text(tx, tx, "Ch{:d}".format(ch), va='top')
        ax.text(-tx, tx, "{:.0f} MHz".format(frqs[ch]), va='top', ha='right')

    # hide tick and tick label of the big axis
    bigax.tick_params(labelcolor='none', which='both', top=False, bottom=False, left=False, right=False)
    bigax.set_xlabel("Offset (deg)", fontsize=14)
    bigax.set_ylabel("Offset (deg)", fontsize=14)

    cb = fig.colorbar(im, cax=cbar_ax, orientation='vertical')
    cb.ax.yaxis.set_ticks_position('right')
    cb.ax.yaxis.set_label_position('right')
    cbar_ax.set_ylabel('Normalised sensitivity')

    # edge = outx[-1]
    y2, y3, y4 = np.linspace(1.05, 1.1, 3)
    xt = 0.9
    k_fs = 12
    r_ax = bigax
    r_ax.text(xt, y4, f"Target {target}", va='center', fontsize=k_fs)
    r_ax.text(xt, y3, "{}".format(mapset.metadata['fp_name']), va='center', fontsize=k_fs)
    r_ax.text(xt, y2, "Pitch {:.2f}".format(mapset.metadata['fp_pitch']), va='center', fontsize=k_fs)

    plt.suptitle("Sensitivity\nSBID {:d}".format(sbid), fontsize=16)

    tt = time.localtime(time.time())
    plot_date = time.strftime("%Y-%m-%d %H:%M:%S", tt)

    bbb = bigax.get_position()
    fig.text(bbb.x0, bbb.y0 - 0.04, 'Plot date {}'.format(plot_date), va='top')

    if plot_file_name:
        plt.savefig(plot_file_name, dpi=300, bbox_inches='tight')


def plot_footprint_leakage(mapset, plot_file_name=None):
    sbid = mapset.metadata['holographySBID']
    target = get_target(sbid)

    frqs = mapset.frequencies
    data = MapSet.sky_transform_hyper(mapset.data)
    inx = np.degrees(mapset.xsi)
    outx = np.linspace(inx[0], inx[-1], 100)
    # da = (outx[1] - outx[0]) ** 2
    ext = [outx[-1], outx[0], outx[0], outx[-1]]
    chans = range(3, 288, 18)
    mos_i = []

    for s, stoke in enumerate(["I", "Q", "U", "V"]):
        cui = np.zeros([36, 100, 100])
        cui_i = np.zeros([36, 100, 100])
        fig, axes = plt.subplots(4, 4, figsize=(12., 12.), sharex='col', sharey='row')
        plt.subplots_adjust(hspace=0.02, wspace=0.02)
        bigax = fig.add_subplot(111, frameon=False)
        # Magic numbers to make the colorbar fit
        cbar_ax = fig.add_axes([0.91, 0.15, 0.02, 0.7])
        if s == 0:
            cm = plt.cm.get_cmap('YlOrRd')
        else:
            cm = plt.cm.RdBu_r
        mos = []
        # sen = []
        for ch in chans:
            cu = data[0, 0, :, s, ch - 2:ch + 3].mean(axis=1)
            cu_i = data[0, 0, :, 0, ch - 2:ch + 3].mean(axis=1)
            for b in range(36):
                fn = sp.RectBivariateSpline(inx, inx, cu[b], kx=2, ky=2)
                fn_i = sp.RectBivariateSpline(inx, inx, cu_i[b], kx=2, ky=2)
                cui[b] = fn(outx, outx)
                cui_i[b] = fn_i(outx, outx)
            # Convert response to leakage - divide by I
            if not stoke == "I":
                cui /= cui_i
            mos.append(linmos(cui, cui_i))
        mos = np.array(mos)

        if stoke == "I":
            mos_i = mos.copy()

        global_max = np.nanmax(mos)
        for i, ax in enumerate(axes.flat):
            if stoke == "I":
                # norm = plt.cm.colors.TwoSlopeNorm(vmax=global_max, vcenter=global_max/2)
                norm = None
            else:
                # Hard-coded to 5% leakage threshold
                norm = plt.cm.colors.TwoSlopeNorm(vmin=-0.05, vcenter=0, vmax=0.05)
                # norm = MidpointNormalize(midpoint=0)
            im = ax.imshow(mos[i], origin='lower', cmap=cm, extent=ext, norm=norm)
            # lev = global_max / 2.0
            lev = 0.5
            if stoke == "I":
                ax.contour(-outx, outx, mos[i], levels=[lev], linewidths=1, colors='k')
            else:
                ax.contour(-outx, outx, mos_i[i], levels=[lev], linewidths=1, colors='k')
            tx = outx[-1] * 0.95
            ch = chans[i]
            ax.text(tx, tx, "Ch{:d}".format(ch), va='top')
            ax.text(-tx, tx, "{:.0f} MHz".format(frqs[ch]), va='top', ha='right')

        # hide tick and tick label of the big axis
        bigax.tick_params(labelcolor='none', which='both', top=False, bottom=False, left=False, right=False)
        bigax.set_xlabel("Offset (deg)", fontsize=14)
        bigax.set_ylabel("Offset (deg)", fontsize=14)

        cb = fig.colorbar(im, cax=cbar_ax, orientation='vertical')
        cb.ax.yaxis.set_ticks_position('right')
        cb.ax.yaxis.set_label_position('right')
        if stoke == "I":
            cbar_ax.set_ylabel('Normalised mosaic')
        else:
            cbar_ax.set_ylabel('Normalised leakage')

        y2, y3, y4 = np.linspace(1.05, 1.1, 3)
        xt = 0.9
        k_fs = 12
        r_ax = bigax
        r_ax.text(xt, y4, f"Target {target}", va='center', fontsize=k_fs)
        r_ax.text(xt, y3, "{}".format(mapset.metadata['fp_name']), va='center', fontsize=k_fs)
        r_ax.text(xt, y2, "Pitch {:.2f}".format(mapset.metadata['fp_pitch']), va='center', fontsize=k_fs)

        if stoke == "I":
            plt.suptitle(f"Stokes {stoke} mosaic\nSBID {sbid:d}", fontsize=16)
        else:
            plt.suptitle(f"Stokes {stoke} leakage\nSBID {sbid:d}", fontsize=16)

        tt = time.localtime(time.time())
        plot_date = time.strftime("%Y-%m-%d %H:%M:%S", tt)

        bbb = bigax.get_position()
        fig.text(bbb.x0, bbb.y0 - 0.04, 'Plot date {}'.format(plot_date), va='top')

        if plot_file_name:
            out_name = plot_file_name.replace("_X_", f"_{stoke}_")
            if stoke == "I":
                out_name = out_name.replace("leakage", "mosaic")
            plt.savefig(out_name, dpi=300, bbox_inches='tight')

def cli():
    """
    Plot three summary files from holography data:
    1. valid_data from <sbid>_Holo_stokes.hdf5
    2. beam position errors from <sbid>_Holo_beam_shifts.hdf5
    3. Sensitivity of footprint over array-wide mean from <sbid>_Holo_mean_interp.hdf5
    :return:
    """
    arg_parser = arg_init()
    args = arg_parser.parse_args()
    if args.explain:
        log.info(explanation)
        sys.exit()
    if args.verbose:
        log.info(args)

    sbid = args.sbid
    holo_dir = args.holo_dir
    main(
        sbid=sbid,
        holo_dir=holo_dir
    )


def main(sbid, holo_dir="."):
    in_name = [
        hf.find_holo_file(holo_dir, sbid=sbid, pol='iquv', kind='stokes.hdf5'),
        hf.find_holo_file(holo_dir, sbid=sbid, pol='i', kind='beam_shifts.hdf5'),
        hf.find_holo_file(holo_dir, sbid=sbid, pol='iquv', kind='mean_interp.hdf5'),
        hf.find_holo_file(holo_dir, sbid=sbid, pol='iquv', kind='taylor.fits')
    ]

    obj = bf.load_beamset_class(in_name[0])
    plot_valid_summary(obj, hf.make_file_name(obj, kind='valid_summary.png'))

    channel = obj.Nf // 2
    obj = bf.load_beamset_class(in_name[1])
    plot_beampos_errors(obj, True, channel, tt=False,
                        plot_file_name=hf.make_file_name(obj, kind='beam_shifts.png'))

    obj = bf.load_beamset_class(in_name[2])
    model_file = pkg_resources.resource_filename("aces.holography", "mean_beam_model.pkl")
    bmodel = clh.BeamModel(obj)

    log.info("Calculating mean beam position shifts")
    shift, resid, amp = clh.get_beampos_errs(obj, bmodel)
    errs_obj = clh.shifts_to_mapset(obj, shift, resid, amp)
    plot_beampos_errors(errs_obj, True, channel, tt=False,
                        plot_file_name=hf.make_file_name(obj, kind='mean_beam_shifts.png'))

    fits_file = fits.open(in_name[3])
    fits_header = fits_file[0].header
    fits_data = np.squeeze(fits_file[0].data)
    shift, resid, amp = clh.get_beampos_errs_from_fits(fits_header, fits_data)
    errs_obj = clh.shifts_to_mapset(obj, shift, resid, amp)
    plot_beampos_errors(errs_obj, True, channel, tt=True,
                        plot_file_name=hf.make_file_name(obj, kind='mean_beam_shifts_fits.png'))

    plot_footprint_sensitivity(obj, hf.make_file_name(obj, kind='stokes_I_sensitivity.png'))
    plot_footprint_leakage(obj, hf.make_file_name(obj, kind='stokes_X_leakage.png'))

if __name__ == "__main__":
    sys.exit(cli())
