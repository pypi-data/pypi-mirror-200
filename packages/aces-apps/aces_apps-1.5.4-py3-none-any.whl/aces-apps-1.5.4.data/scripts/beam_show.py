#!/usr/bin/env python
"""
Example use of BeamSet and subclasses BeamMeasure.

Copyright (C) CSIRO 2017
"""
import sys
import argparse as ap
import matplotlib.pylab as plt

import aces.beamset.beamfactory as bf


EXPLANATION = """The beam_show process displays a holography beam map.
"""
HELPSTART = """The beam_show process displays a holography beam map.
"""


def arg_init():
    """Define the interpretation of command line arguments.
    """
    parser = ap.ArgumentParser(prog='beam_show.py',
                               formatter_class=ap.RawDescriptionHelpFormatter,
                               description=HELPSTART,
                               epilog='See -x for more explanation')
    parser.add_argument('inFile', nargs="?", help="Data file (hdf5 format)")
    parser.add_argument('-o', '--output', default=None, help="Name of output file")
    parser.add_argument('-a', '--antennas', default=list(range(36)), action=IntList,
                        help="Antennas to model [%(default)s]")
    parser.add_argument('-b', '--beams', default=list(range(37)), action=IntList,
                        help="Beam numbers to model [%(default)s]")
    parser.add_argument('-p', '--polarizations', default=['XX', 'YY'], action=PolList,
                        help="Polarizations to model [%(default)s]")
    parser.add_argument('-c', '--channels', default=list(range(0, 300, 30)), action=IntList, type=str,
                        help="Channel numbers to model [%(default)s]")
    parser.add_argument('-g', '--do_log', action='store_true', help="Logarithmic intensity coding")
    parser.add_argument('-s', '--save', action='store_true', help="Save plot file")
    parser.add_argument('-i', '--interp', type=float, default=0.2,
                        help="Interpolation grid spacing [%(default).2f] (deg)")
    parser.add_argument('-m', '--movie', action='store_true', help="Plot sequence for animation")
    parser.add_argument('-d', '--display', action='store_true', help="Make plots interactive")
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-x', '--explain', action='store_true', help="Give an expanded explanation")
    return parser


class IntList(ap.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        # print('ACTION : %r %r %r' % (namespace, values, option_string)
        safe_dict = {'range': range}
        rp = eval(values, safe_dict)
        if isinstance(rp, tuple):
            rp = list(rp)
        if not isinstance(rp, list):
            rp = [rp]
        setattr(namespace, self.dest, rp)


class PolList(ap.Action):
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
    print("\n     beam_show\n\n")

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

    for_animation = args.movie

    print("Reading %s. " % infile)
    # Read the new hdf5 file, extract a particular map, interpolate and display.
    obj = bf.load_beamset_class(args.inFile)
    obj.print_summary()

    i_step = args.interp
    obj.set_interp(i_step)

    channels = [a for a in args.channels if a < obj.Nf]
    request = {'antennas': args.antennas,
               'beams': args.beams,
               'polarizations': args.polarizations,
               'channels': channels}

    seli = {'times': 0, 'channels': request['channels']}
    selv = {}
    for thing in ['antennas', 'beams', 'polarizations']:
        # print(thing, request[thing]
        selv[thing] = request[thing]

    tmp = list(selv['polarizations'])
    if 'I' in tmp:
        stokes_i = True
        tmp[tmp.index('I')] = 'XX'
        selv['polarizations'] = tmp
    else:
        stokes_i = False

    # print(seli)
    # print(selv)
    sel_map = obj.get_selector(seli, selv)

    p_ant = -1
    schan = 0
    for s1 in sel_map:
        t, ant, beam, pol, freq = obj.get_vector(s1)
        print(ant, beam, pol, freq)

        offsets = beam, obj.get_beam_offset(s1[2])
        if ant != p_ant:
            p_ant = ant
            print('AK%02d' % ant)

        if not obj.flags[s1]:
            if for_animation:
                pname = "beammap_AK{:02d}_{:d}_{}_c-{:03d}.png".format(ant, beam, pol, schan)
                schan += 1
            else:
                pname = "beammap_AK{:02d}_{:d}_{}_{:04d}.png".format(ant, beam, pol, int(freq+0.5))
            if stokes_i:
                mp = obj.get_map_stokes_i(s1)
            else:
                mp = obj.get_map(s1, 'power')

            plt.clf()
            mp.plot(log=args.do_log, title=True, xlabels=True, ylabels=True, bar=False)
            if args.save:
                plt.savefig(pname, dpi=300, bbox_inches='tight')
            if args.display:
                plt.show()


if __name__ == "__main__":
    sys.exit(main())
