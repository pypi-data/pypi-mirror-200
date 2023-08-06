#!/usr/bin/env python
"""
Compute array-wide mean beam shapes from holgraphy data

Copyright (C) CSIRO 2018
"""

import argparse as ap
import sys
import os

import numpy as np
from numpy import pi
from numpy.fft import ifft2, fft2, fftshift
import matplotlib.pylab as plt

import aces.beamset.beamfactory as bf


def shift(z, dx, dy):
    m, n = z.shape
    x, y = np.mgrid[0:m, 0:n] * 1.0
    x *= 1.0 / m
    y *= 1.0 / n
    t = fft2(z)
    ikx = 2j * np.pi * x
    iky = 2j * np.pi * y

    ph = fftshift(np.exp(-ikx * dx - iky * dy))
    return ifft2(t * ph)


def make_gen(shape):
    """Shape is always 5 long
    """
    for i in range(shape[0]):
        for j in range(shape[1]):
            for k in range(shape[2]):
                for l in range(shape[3]):
                    for m in range(shape[4]):
                        yield np.s_[i, j, k, l, m]


def fit_line(x, y):
    A = np.vstack([x, np.ones(len(x))]).T
    mc = np.linalg.lstsq(A, y)[0]
    return mc


def zero_phase(complex_image):
    z = complex_image.copy()
    x, y = np.real(z).flatten(), np.imag(z).flatten()
    if np.abs(x).max() > np.abs(y).max():
        mc = fit_line(x, y)
        ang = np.arctan(mc[0])
    else:
        mc = fit_line(-y, x)
        ang = np.arctan(mc[0]) - pi/2.
    ph = np.exp(-1.0j*ang)
    z -= mc[1]*1.j
    z *= ph
    if np.abs(np.real(z).min()) > np.abs(np.real(z).max()):
        z *= -1
    return z


def op_complex_mean(z):
    """Mean of complex data"""
    return z.mean(axis=0)


def op_func_mean(z_in):
    """Mean of squared magnitude"""
    z = np.ma.masked_invalid(np.abs(z_in) ** 2)
    for zi in z:
        zi /= zi.max()
    ret = z.mean(axis=0)
    return ret


def op_func_std(z_in):
    """Standard deviation of squared magnitude"""
    z = np.ma.masked_invalid(np.abs(z_in) ** 2)
    for zi in z:
        zi /= zi.max()
    ret = z.std(axis=0)
    return ret


def done_ant(err):
    err = np.array(err)
    err = np.reshape(err, [36, 2, 2])
    errx = err[:, 0, :].mean(axis=0)
    erry = err[:, 1, :].mean(axis=0)
    stdx = err[:, 0, :].std(axis=0)
    stdy = err[:, 1, :].std(axis=0)

    return [errx, erry], [stdx, stdy]


EXPLANATION = """TBD.
"""
HELPSTART = """Provide an SBID for which you have holography measurements and elliptical fits to
the beam half-power contours.
"""


def arg_init():
    """Provide essential data for interpreting command line arguments.
    """
    parser = ap.ArgumentParser(prog='array_mean',
                               formatter_class=ap.RawDescriptionHelpFormatter,
                               description=HELPSTART,
                               epilog='See -x for more explanation')
    parser.add_argument('sbid', nargs="?", type=int, help="SBID of holography measurement")
    parser.add_argument('-a', '--antennas', default=list(range(36)), action=intList,
                        help="Antennas to model [%(default)s]")
    parser.add_argument('-b', '--beams', default=list(range(37)), action=intList,
                        help="Beam numbers to model [%(default)s]")
    parser.add_argument('-p', '--polarizations', default=['XX', 'YY'], action=polList,
                        help="Polarizations to model [%(default)s]")
    parser.add_argument('-c', '--channel', type=int, default=150,
                        help="Channel number to use for centering [%(default)s]")
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-x', '--explain', action='store_true', help="Give an expanded explanation")
    return parser


class intList(ap.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        # print('ACTION : %r %r %r' % (namespace, values, option_string)
        safe_dict = {'range': range}
        rp = eval(values, safe_dict)
        if not isinstance(rp, list):
            rp = [rp]
        setattr(namespace, self.dest, rp)


class polList(ap.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        # print('ACTION : %r %r %r' % (namespace, values, option_string)
        pols = ['XX', 'YY', 'XY', 'YX', 'I', 'Q', 'U', 'V']
        rp = []
        for p in pols:
            if p in values:
                rp.append(p)
        setattr(namespace, self.dest, rp)


def main():

    # parse command line options
    print("\n     array_mean\n\n")

    args = arg_init().parse_args()
    if args.explain:
        print(EXPLANATION)
        sys.exit(0)
    if args.verbose:
        print("ARGS = ", args)

    sbid = args.sbid
    selants = args.antennas
    channel = args.channel
    # Load a MapSet file and print(its summary
    in_name = '{:d}_Holo.hdf5'.format(sbid)
    mod_name = '{:d}_ellipse.hdf5'.format(sbid)
    sub_name = '{:d}_Holo_ss.hdf5'.format(sbid)
    cen_name = '{:d}_Holo_ss_centred.hdf5'.format(sbid)

    mean_name = '{:d}_Holo_ss_mean.hdf5'.format(sbid)
    std_name = '{:d}_Holo_ss_std.hdf5'.format(sbid)

    if not os.path.exists(in_name):
        print("No holography file {} found.".format(in_name))
        sys.exit(0)
    if not os.path.exists(mod_name):
        print("No beam model file {} found.".format(mod_name))
        sys.exit(0)

    holo = bf.load_beamset_class(in_name)
    holo.print_summary()

    mod = bf.load_beamset_class(mod_name)

    # Selections:
    #   for models, a selector
    seli = {'times': 0, 'channels': [channel], 'beams': 'all'}
    selv = {'antennas': selants, 'polarizations': ['XX', 'YY']}
    sel_mod = mod.get_selector(seli, selv)

    # and for holography maps a selection (not selector !)
    seli = {'times': 0, 'frequencies': 'all', 'beams': 'all'}
    sel_holo = holo.get_selection(seli, selv)

    offsets = mod.get_beam_offsets()
    errs, err = [], []
    perant = []
    stdant = []
    iant = -1
    for s in sel_mod:
        i = s[1]
        if i != iant:
            if iant >= 0:
                er, st = done_ant(err)
                perant.append(er)
                stdant.append(st)
            err = []
            iant = i
        model = mod.get_model(s)
        err.append(model.get_centre() - offsets[s[2]])
    e, s = done_ant(err)
    perant.append(e)
    stdant.append(s)

    perant = np.degrees(np.array(perant))

    for i, p in enumerate(perant):
        print("{:d} {:^30} {:^30}".format(selants[i], p[0] * 60, p[1] * 60))

    # ## Procedure
    # 1. Prepare contour fits for a holography set
    # 2. Form per-antenna pointing errors
    # 3. Form subset of Holography data - to eliminate unwanted antennas
    #  - iterate through subset, shifting each map using the product of #2
    # 4. Use operation method to sum over antennas, leaving an image per beam, pol, channel.

    subset = holo.get_subset(sel_holo)
    subset.write_to_hdf5(sub_name.format(sbid))
    stage = np.zeros(subset.data.shape, dtype=complex)

    # shift all h maps in subset
    ssel = make_gen(subset.get_container_shape())
    print(subset.metadata['antennas'])
    xgrid = subset.metadata['xAxis']
    dgrid = np.degrees(xgrid[1] - xgrid[0])
    ia = -1
    for ss in ssel:
        err = perant[ss[1], ss[3]] / dgrid
        m = np.nan_to_num(subset.data[ss])
        mc = shift(m, err[0], err[1])
        stage[ss] = zero_phase(mc)

        if ss[1] != ia and args.verbose:
            print(ss[1])
            ia = ss[1]

    subset.data = stage
    subset.write_to_hdf5(cen_name.format(sbid))

    axis = 1
    qmean = subset.operation(axis, op_complex_mean, [0])
    qstd = subset.operation(axis, op_func_std, [0])

    qmean.write_to_hdf5(mean_name.format(sbid))
    qstd.write_to_hdf5(std_name.format(sbid))

    print("Subset of holography data written to {}".format(sub_name))
    print("  Centred holography data written to {}".format(cen_name))
    print("     Mean holography data written to {}".format(mean_name))
    print("      Std holography data written to {}".format(std_name))


if __name__ == "__main__":
    sys.exit(main())
