#!/usr/bin/env python
"""
Example use of BeamSet and subclasses BeamModel.

Copyright (C) CSIRO 2017
"""
import argparse as ap
import sys

import aces.beamset.beamfactory as bf
from numpy import pi

import aces.beamset.surfacegaussian as sg
import aces.beamset.surfaceairy as sa
from aces.beamset import modelset as modset


# import gaussfitter as gf


def show_params(params):
    """ Foratted display of parameters.
    """
    p = params
    if p is None:
        st = "None"
    else:
        st = "{:6.5f} {:6.3f}  ({:6.3f},{:6.3f}) {:6.3f} {:6.3f}   {:6.3f}".format(p[0], p[1], p[2], p[3], p[4], p[5],
                                                                                   p[6])
    return st


EXPLANATION = """TBD.
"""
HELPSTART = """The fit_surface process fits a 2D gaussian to the man lobe of the
selected beams. It provides an example of how a MapSet holding holography
beam maps can be accessed, and models for each map be written
to a ModelSet object and an associated output file.
"""


def arg_init():
    """Provide essential data for interpreting command line arguments.
    """
    parser = ap.ArgumentParser(prog='fit_surface',
                               formatter_class=ap.RawDescriptionHelpFormatter,
                               description=HELPSTART,
                               epilog='See -x for more explanation')
    parser.add_argument('inFile', nargs="?", help="Data file (hdf5 format)")
    parser.add_argument('-o', '--output', default=None, help="Name of output file")
    parser.add_argument('-f', '--function', choices=['gaussian', 'airy'], default='gaussian',
                        help="Function to fit (gaussian, airy)")
    parser.add_argument('-a', '--antennas', default=list(range(36)), action=intList,
                        help="Antennas to model [%(default)s]")
    parser.add_argument('-b', '--beams', default=list(range(37)), action=intList,
                        help="Beam numbers to model [%(default)s]")
    parser.add_argument('-p', '--polarizations', default=['XX', 'YY'], action=polList,
                        help="Polarizations to model [%(default)s]")
    parser.add_argument('-c', '--channels', default=list(range(0, 300, 30)), action=intList,
                        help="Channel numbers to model [%(default)s]")
    parser.add_argument('-L', '--level', type=float, default=0.2,
                        help="Lower limit of beam to fit")
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-x', '--explain', action='store_true', help="Give an expanded explanation")
    return parser


class intList(ap.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        # print 'ACTION : %r %r %r' % (namespace, values, option_string)
        safe_dict = {'range': range}
        rp = eval(values, safe_dict)
        if not isinstance(rp, list):
            rp = [rp]
        setattr(namespace, self.dest, rp)


class polList(ap.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        # print 'ACTION : %r %r %r' % (namespace, values, option_string)
        pols = ['XX', 'YY', 'XY', 'YX', 'I', 'Q', 'U', 'V']
        rp = []
        for p in pols:
            if p in values:
                rp.append(p)
        setattr(namespace, self.dest, rp)


def main():
    # parse command line options
    print("\n     fit_surface\n\n")
    args = arg_init().parse_args()
    verbose = args.verbose
    level = args.level

    if args.explain:
        print(EXPLANATION)
        sys.exit(0)
    if verbose:
        print("ARGS = ", args)

    if args.inFile:
        infile = args.inFile
    else:
        print("Try -h for help")
        sys.exit(0)

    if args.function == "gaussian":
        fitter = sg.SurfaceGaussian
        guess_params = sg.guess_params
    elif args.function == "airy":
        fitter = sa.SurfaceAiry
        guess_params = sa.guess_params

    if args.output:
        outfile = args.output.split('.')[0] + '.hdf5'
    else:
        if "holo" in infile.lower():
            outfile = infile.lower().replace("holo", fitter.SHORT_NAME)
        else:
            outfile = 'model.hdf5'

    print("Reading %s.  Writing measurments to %s." % (infile, outfile))
    # Read the new hdf5 file, extract a particular map, interpolate and display.
    obj = bf.load_beamset_class(args.inFile)
    obj.print_summary()

    gridstep = 0.1
    obj.set_interp(gridstep)
    frequencies = obj.metadata['frequencies']

    request = {'antennas': args.antennas,
               'beams': args.beams,
               'polarizations': args.polarizations,
               'channels': args.channels}

    mod_metadata = obj.get_metadata(override=request)

    mod_metadata['model'] = "SurfaceGaussian"
    mod_metadata['modelParams'] = fitter.PARAM_NAMES
    mod_metadata['payloadshape'] = (fitter.NUM_PARAMS,)

    mod = modset.ModelSet(mod_metadata)
    mod.print_summary()

    itime = 0
    seli = {'times': itime}
    selv1, selv2 = {}, {}
    for thing in ['antennas', 'beams', 'polarizations', 'frequencies']:
        selv1[thing] = mod.metadata[thing]
        selv2[thing] = mod.metadata[thing]

    tmp = list(selv1['polarizations'])
    if 'I' in tmp:
        tmp[tmp.index('I')] = 'XX'
        selv1['polarizations'] = tmp

    sel_map = obj.get_selector(seli, selv1)
    sel_mod = mod.get_selector(seli, selv2)

    for smap, smod in zip(sel_map, sel_mod):
        time, ant, beam, pol, freq = obj.get_vector(smap)
        ich = list(frequencies).index(freq)
        if verbose:
            print("\n AK{:02d}  beam {:d}  {:s} {:d}".format(ant, beam, pol, ich))
        if not obj.flags[smap]:
            bmap = obj.get_map(smap, 'power')
            bmap.mask_below(level)

            par_ell = guess_params(bmap)
            if par_ell:
                gfit = fitter(par_ell)
                gfit.fit(bmap)
                fitted_params = gfit.get_params()
                if verbose:
                    print('guess ', show_params(par_ell))
                    print('fit   ', show_params(fitted_params))
                if fitted_params[4] < fitted_params[5]:
                    tmp = fitted_params[4]
                    fitted_params[4] = fitted_params[5]
                    fitted_params[5] = tmp
                    fitted_params[6] = (fitted_params[6] + pi / 2) % pi
                    if verbose:
                        print('final ', show_params(fitted_params))
                mod.data[smod] = fitted_params
            else:
                mod.flags[smod] = True
        else:
            mod.flags[smod] = True

    history_entry = "{} fit".format(fitter.FUNCTION_NAME)
    mod.add_to_history(history_entry)
    mod.print_summary()
    mod.write_to_hdf5(outfile)


if __name__ == "__main__":
    sys.exit(main())
