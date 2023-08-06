#!/usr/bin/env python
"""
Analysis of holography beam maps to infer pointing errors, etc..

Copyright (C) CSIRO 2021
"""

import numpy as np
import sys
import argparse as ap
import pickle
import copy

from astropy.io import ascii
from astropy.table import Table, Column

import matplotlib.pylab as plt
from aces.obsplan.config import ACESConfig

from aces.beamset.mapset import MapSet
from aces.beamset.beamset import BeamSet
import numpy.fft as fft

import aces.beamset.beamfactory as bf

aces_cfg = ACESConfig()
fp_factory = aces_cfg.footprint_factory

EXPLANATION = """The beam_pointing process ....
"""
HELPSTART = """The ...
"""


def arg_init():
    """Define the interpretation of command line arguments.
    """
    parser = ap.ArgumentParser(prog='beam_pointing.py',
                               formatter_class=ap.RawDescriptionHelpFormatter,
                               description=HELPSTART,
                               epilog='See -x for more explanation')
    parser.add_argument('sbid', nargs="?", help="SBID of Stokes maps")
    parser.add_argument('-d', dest='holo_dir', type=str, default='.',
                        help='Directory containing holography data [./].')
    parser.add_argument('-c', '--chan', type=int, default=200, help='Channel number')

    parser.add_argument('-r', '--recompute', action='store_true')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-x', '--explain', action='store_true', help="Give an expanded explanation")
    return parser


# holo_dir = '/Users/mcc381/askap/ASKAP/beams'


def get_shift(obj, ref_im, target_im, frac=0.25):
    """
    Compute the shift of target_im relative to ref_im.
    Use Fourier shift theorem
    param: obj (MapSet)
    param: ref_im (ndarray) Reference image ndim=2
    param: target_im (ndarray) Target image
    param: frac (float) Mask transform values < ampMax * frac in phase fit.
    """
    n0 = ref_im.shape[0] // 2
    f = fft.fftshift(fft.fft2(ref_im))
    fa = fft.fftshift(fft.fft2(target_im))

    zf = np.angle(fa / f).flatten()
    amp = np.abs(fa)
    clip = amp.max() * frac
    zm = np.ma.masked_array(zf, amp < clip)
    x = np.arange(-1. * n0, n0 + 0.1, 1.)
    y = np.arange(-1. * n0, n0 + 0.1, 1.)
    xg, yg = np.meshgrid(x, y)
    xf = xg.flatten()
    yf = yg.flatten()
    zf = zm[~zm.mask]
    xf = xf[~zm.mask]
    yf = yf[~zm.mask]
    zf = np.expand_dims(zf, 1)

    A = np.c_[xf, yf]
    result = np.linalg.lstsq(A, zf, rcond=None)
    coeff, r, rank, s = result
    xs = obj.metadata['xAxis']
    span = xs[-1] - xs[0]
    shift = -1.0 * coeff / (2.0 * np.pi) * span
    if len(r) > 0:
        qual = np.ma.masked_array(np.abs(fa / f), amp < clip).mean()
    else:
        qual = np.nan
    return shift[:, 0], f, fa, result, qual


class BeamModel(object):
    delta_x = 0.6
    edge = 4.2
    centre = 7.

    def __init__(self, pickle_file):
        pkg = pickle.load(open(pickle_file, 'rb'))
        xk, ref_freq, model, fn = pkg
        self.xs = xk
        self.ref_freq = ref_freq
        self.model = model
        self.bv_func = fn

    def get(self, pixoff, freq):
        px, py = BeamModel.delta_x * (pixoff - BeamModel.centre) * freq / self.ref_freq
        end = BeamModel.edge * freq / self.ref_freq
        xm = np.linspace(-end - px, end - px, 15)
        ym = np.linspace(-end - py, end - py, 15)
        return self.bv_func(ym, xm)


def make_ref(obj, beam, chan):
    pixoff = obj.get_beam_positions()
    px, py = pixoff[beam]
    nx, ny = obj.metadata['payloadshape']
    dgrid = obj.xsi[1] - obj.xsi[0]
    freq = obj.frequencies[chan]
    aw = 300. / freq / 12.0 * 1.09 / 2. / np.sqrt(np.log(2)) / dgrid
    xh, yh = np.meshgrid(np.arange(nx), np.arange(ny))
    ref = np.exp(-(np.sqrt((xh - px) ** 2 + (yh - py) ** 2) / aw) ** 2)
    return ref


def get_beampos_errors(obj, bmodel, chan):
    na, nb = obj.Na, obj.Nb
    cube_s = MapSet._sky_transform_hyper(obj.data)[0]
    shifts = np.ones((na, nb, 2))
    pixoff = obj.get_beam_positions()
    for beam in range(nb):
        #         ref = make_ref(obj, beam, chan)
        ref = bmodel.get(pixoff[beam], obj.frequencies[chan])
        for ant in range(na):
            refa = np.abs(cube_s[ant, beam, 0, chan])
            shifts[ant, beam], f, fa, co, qu = get_shift(obj, ref, refa)
    return shifts


def get_beampos_errs(obj, bmodel):
    na, nb, nf = obj.Na, obj.Nb, obj.Nf
    shiftss = np.ones((na, nb, nf, 2))
    resid = np.zeros([na, nb, nf])
    amps = np.zeros([na, nb, nf])
    pixoff = obj.get_beam_positions()
    cube_s = MapSet._sky_transform_hyper(obj.data)[0]
    ants = list(range(na))
    for chan in range(nf):
        for beam in range(nb):
            ref = bmodel.get(pixoff[beam], obj.frequencies[chan])
            for ant in ants:
                refa = np.abs(cube_s[ant, beam, 0, chan])
                sh, f, fa, co, amps[ant, beam, chan] = get_shift(
                    obj, ref, refa, frac=0.25)
                shiftss[ant, beam, chan] = sh
                if len(co[1]) == 0:
                    resid[ant, beam, chan] = np.nan
                else:
                    resid[ant, beam, chan] = co[1][0]
    return shiftss, resid, amps


def save_shifts(obj, shifts, resids, amps, holo_dir, sbid):
    mds = copy.deepcopy(obj.metadata)
    mds['polarizations'] = ['I']
    mds['payloadshape'] = (4,)
    mds['xAxis'] = [0.0]
    mds['yAxis'] = [0.0]
    sdata = np.zeros([1, obj.Na, obj.Nb, 1, obj.Nf, 4])
    sdata[0, :, :, 0, :, :2] = shifts
    sdata[0, :, :, 0, :, 2] = resids
    sdata[0, :, :, 0, :, 3] = amps

    print(shifts.shape, resids.shape)
    sflags = np.array(obj.flags)
    print(sdata.shape)

    shift_obj = BeamSet(metadata=mds,
                        data=sdata,
                        flags=sflags,
                        filename=None
                        )
    shift_obj.add_to_history('Beam position errs, resid, amps')
    outnam = '{}/{:d}_Holo_beam_shifts.hdf5'.format(holo_dir, sbid)
    shift_obj.write_to_hdf5(outnam)


def plot_beampos_errors(beam_pos, beam_pos_errs, remove_mean, plot_file_name=None, **kw):
    poss = beam_pos
    shiftsd = np.degrees(beam_pos_errs)
    fig, ax = plt.subplots(6, 6, figsize=(16., 15.), sharex=True, sharey=True)
    plt.subplots_adjust(wspace=0.04, hspace=0.04)
    qu_kw = {'width': 0.008, 'headwidth': 4, 'headlength': 5, 'headaxislength': 4.0, 'color': 'k', 'zorder': 10}
    qu_kwb = {'width': 0.02, 'headwidth': 3, 'headlength': 3, 'headaxislength': 2.0, 'color': 'b', 'zorder': 20}
    scale1 = 0.2
    scale2 = 0.075
    for ant, axf in zip(list(range(36)), ax.flat):
        shifts_mean = np.nanmean(shiftsd[ant], axis=0)
        shifts_mean_mag = (shifts_mean ** 2).sum() ** 0.5
        shifts_mean_ang = np.degrees(np.arctan2(shifts_mean[0], shifts_mean[1]))
        shiftsdm = shiftsd[ant] - shifts_mean
        shifts_corr_mag = np.sqrt(shiftsdm[:, 0] ** 2 + shiftsdm[:, 1] ** 2)

        shifts_corr_mag_mean = np.nanmean(shifts_corr_mag)
        shifts_corr_mag_std = np.nanstd(shifts_corr_mag)

        if remove_mean:
            axf.quiver(poss[:, 0], poss[:, 1], shiftsdm[:, 0], shiftsdm[:, 1], angles='xy', scale_units='xy',
                       scale=scale1, **qu_kw)
            axf.quiver(0.0, 0.0, shifts_mean[0], shifts_mean[1], angles='xy', scale_units='xy', scale=scale2, **qu_kwb)
            if not np.isnan(shifts_corr_mag_std):
                axf.text(0.0, -3.0, "{:.1f}±{:.1f}'".format(shifts_corr_mag_mean * 60., shifts_corr_mag_std * 60.),
                         ha='center', va='center')
                mag = shifts_mean_mag * 60.
                ang = shifts_mean_ang
                axf.text(0.0, +3.0, "{:.1f}' {:+4.0f}".format(mag, ang), ha='center', va='center', color='b')
        else:
            axf.quiver(poss[:, 0], poss[:, 1], shiftsd[ant, :, 0], shiftsd[ant, :, 1], angles='xy', scale_units='xy',
                       scale=scale1, **qu_kw)
        axf.plot(poss[:, 0], poss[:, 1], 'o', c='0.9', ms=10, zorder=1)
        axf.plot(poss[0, 0], poss[0, 1], 'or')
        axf.text(3.0, 2.8, "AK{:02d}".format(ant + 1))
        axf.set_xlim(3.3, -3.3)
        axf.set_ylim(-3.3, 3.3)
    slen = 6
    ax[0, 0].plot([0.0, -slen / 60. / scale1], [1.0, 1.0], 'k', lw=2)
    ax[0, 0].text(0.2, 1.0, "{:d}'".format(slen), ha='right', va='center')
    if remove_mean:
        ax[0, 0].plot([0.0, -slen / 60. / scale2], [0.0, 0.0], 'b', lw=3)
        ax[0, 0].text(0.2, 0.0, "{:d}'".format(slen), ha='right', va='center', color='b')
    sup = "Beam pos errs - "
    if 'sbid' in kw:
        sup += " SBID {:d}".format(kw['sbid'])
    if "chan" in kw:
        sup += "  Chan {:d}".format(kw['chan'])
    if len(sup) > 0:
        fig.suptitle(sup)
    if plot_file_name:
        plt.savefig(plot_file_name, dpi=300, bbox_inches='tight')


def main():
    # parse command line options
    print("\n     beam_pointing\n\n")

    args = arg_init().parse_args()
    if args.explain:
        print(EXPLANATION)
        sys.exit(0)
    if args.verbose:
        print("ARGS = ", args)

    sbid = int(args.sbid)
    chan = int(args.chan)
    holo_dir = args.holo_dir

    recompute = args.recompute

    if recompute:
        in_name = '{}/{:d}_Holo_stokes.hdf5'.format(holo_dir, sbid)
        obj = bf.load_beamset_class(in_name)
        Na, Nb, Np, Nf = obj.Na, obj.Nb, obj.Np, obj.Nf

        bmodel = BeamModel('{}/mean_beam_model.pkl'.format(holo_dir))
        errors, resids, amps = get_beampos_errs(obj, bmodel)
        save_shifts(obj, errors, resids, amps, holo_dir, sbid)
        shifts = errors[:, :, chan]
    else:
        in_name = '{}/{:d}_Holo_beam_shifts.hdf5'.format(holo_dir, sbid)
        obj = bf.load_beamset_class(in_name)
        Na, Nb, Np, Nf = obj.Na, obj.Nb, obj.Np, obj.Nf
        shifts = obj.data[0, :, :, 0, chan, :2]

    pixoff = obj.get_beam_offsets()
    kw = {"sbid": sbid, "chan": chan}
    plot_file = "beam_pos_errs_SB{:d}".format(sbid)
    plot_beampos_errors(pixoff, shifts, True, plot_file_name=plot_file, **kw)

    shiftsd = np.degrees(shifts)
    shifts_mean = shiftsd.mean(axis=1)
    bp = Table()
    bp['antenna'] = list(range(1, Na + 1))
    bp['ew_error'] = shifts_mean[:, 0]
    bp['ns_error'] = shifts_mean[:, 1]
    tab_name = 'beam_pointing_SB{:d}.csv'.format(sbid)
    bp.write(tab_name, format='ascii.csv', overwrite=True)


if __name__ == "__main__":
    sys.exit(main())
