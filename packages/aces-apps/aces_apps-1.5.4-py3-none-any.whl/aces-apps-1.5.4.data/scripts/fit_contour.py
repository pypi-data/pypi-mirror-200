#!/usr/bin/env python
"""
Example use of BeamSet and subclasses BeamMeasure.

Copyright (C) CSIRO 2017
"""
import argparse as ap
import sys

import aces.beamset.beamfactory as bf
import numpy as np

import aces.beamset.contourellipse as ce
from aces.beamset import modelset as modset

EXPLANATION = """The fit_contour process fits an ellipse to the half-power contour of the
selected beams. It provides an example of how a MapSet holding holography
beam maps can be accesed, and models for each map be written
to a ModelSet object and associated output file.
"""
HELPSTART = """The fit_contour process fits an ellipse to the half-power contour of the
selected beams. It provides an example of how a MapSet holding holography
beam maps can be accessed, and models for each map be written
to a ModelSet object and an associated output file.
"""


def arg_init():
    """Define the interprestation of command line arguments.
    """
    parser = ap.ArgumentParser(prog='fit_contour.py',
                               formatter_class=ap.RawDescriptionHelpFormatter,
                               description=HELPSTART,
                               epilog='See -x for more explanation')
    parser.add_argument('inFile', nargs="?", help="Data file (hdf5 format)")
    parser.add_argument('-o', '--output', default=None, help="Name of output file")
    parser.add_argument('-a', '--antennas', default=list(range(36)), action=IntList,
                        help="Antennas to model [%(default)s]")
    parser.add_argument('-b', '--beams', default=[], action=IntList,
                        help="Beam numbers to model [%(default)s]")
    parser.add_argument('-p', '--polarizations', default=['XX', 'YY'], action=polList,
                        help="Polarizations to model [%(default)s]")
    parser.add_argument('-c', '--channels', default=list(range(0, 300, 30)), action=IntList,
                        help="Channel numbers to model [%(default)s]")
    parser.add_argument('-i', '--interp', type=float, default=0.2,
                        help="Interpolation grid spacing [%(default).2f] (deg)")
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-x', '--explain', action='store_true', help="Give an expanded explanation")
    return parser


class IntList(ap.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        # print 'ACTION : %r %r %r' % (namespace, values, option_string)
        safe_dict = {'range': range}
        rp = eval(values, safe_dict)
        if not (isinstance(rp, tuple) or isinstance(rp, list)):
            rp = (rp,)
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
    print("\n     fit_contour\n\n")

    args = arg_init().parse_args()
    if args.explain:
        print(EXPLANATION)
        sys.exit(0)
    if args.verbose:
        print("ARGS = ", args)

    if args.inFile:
        infile = args.inFile
    else:
        print("Try -h for help")
        sys.exit(0)

    if args.output:
        outfile = args.output.split('.')[0] + '.hdf5'
    else:
        if "holo" in infile.lower():
            outfile = infile.lower().replace("holo", "ellipse")
        else:
            outfile = 'ellipse.hdf5'

    print("Reading %s.  Writing models to %s." % (infile, outfile))
    # Read the new hdf5 file, extract a particular map, interpolate and display.
    obj = bf.load_beamset_class(args.inFile)
    obj.print_summary()
    i_step = args.interp
    obj.set_interp(i_step)

    request = {}
    for k in ['antennas', 'beams', 'polarizations', 'channels']:
        if len(args.__getattribute__(k)) > 0:
            request[k] = args.__getattribute__(k)

    mod_metadata = obj.get_metadata(override=request)

    mod_metadata['model'] = "ContourEllipse"
    mod_metadata['modelParams'] = ce.ContourEllipse.PARAM_NAMES
    mod_metadata['payloadshape'] = (ce.ContourEllipse.NUM_PARAMS,)

    mod_metadata['fp_angle'] = 45.0
    mods = modset.ModelSet(mod_metadata)
    mods.print_summary()

    seli = {'times': 0}
    selv1, selv2 = {}, {}
    for thing in ['antennas', 'beams', 'polarizations', 'frequencies']:
        selv1[thing] = mods.metadata[thing]
        selv2[thing] = mods.metadata[thing]

    tmp = list(selv1['polarizations'])
    if 'I' in tmp:
        tmp[tmp.index('I')] = 'XX'
        selv1['polarizations'] = tmp

    sel_map = obj.get_selector(seli, selv1)
    sel_mod = mods.get_selector(seli, selv2)

    p_ant = -1
    for s1, s2 in zip(sel_map, sel_mod):
        it, ia, ib, ip, ichan = s1
        t, ant, beam, pol, freq = obj.get_vector(s1)
        ot, oant, obeam, opol, ofreq = mods.get_vector(s2)
        if ant != p_ant:
            p_ant = ant
            print('AK%02d' % ant)

        if not obj.flags[s1]:
            if opol == 'I':
                mp = obj.get_map_stokes_i(s1)
            else:
                mp = obj.get_map(s1, 'power')

            cont = mp.get_contour(0.5)
            if len(cont) == 1:
                xy = cont[0][0]
                area = ce.greens(xy) * (180.0 / np.pi) ** 2
            else:
                area = 0.0
            # Set area limit of 0.6 sq deg. Will FAIL for higher freuencies.
            if area > 0.6:
                ellipse = ce.ContourEllipse()
                ellipse.fit(xy[:, 0], xy[:, 1])
                if ellipse.valid:
                    mods.data[s2] = ellipse.get_params()
                else:
                    if args.verbose:
                        print('Flagged %2d %2d %s %3d  ellipse fit failed' % (ant, beam, pol, ichan))
                    mods.flags[s2] = True

            else:
                if args.verbose:
                    print('Flagged %2d %2d %s %3d  implausible contour' % (ant, beam, pol, ichan))
                mods.flags[s2] = True
        else:
            mods.flags[s2] = True

    nflagged = np.count_nonzero(mods.flags)
    ntotal = mods.flags.size

    print("Input  {:.2f}% flagged  ({:d})".format(nflagged * 100. / ntotal, nflagged))
    mods.add_to_history("Ellipse fitted to half-power contour")
    mods.write_to_hdf5(outfile)


if __name__ == "__main__":
    sys.exit(main())
