#!/usr/bin/env python

import sys
import argparse as ap

from astropy.coordinates import Angle
from astropy.coordinates import SkyCoord
from astropy import units as au
from astropy.io import ascii
import numpy as np
from askap.footprint import Skypos
from askap.coordinates import parse_direction


EXPLANATION = """
complete this ...
"""
HELPSTART = """This helps find the RACS field containing a given source.
v 2019Jul15
"""


def arg_init():
    """Provide essential data for interpreting command line arguments.
    """
    parser = ap.ArgumentParser(prog='racs_find',
                               formatter_class=ap.ArgumentDefaultsHelpFormatter,
                               description=HELPSTART,
                               epilog='See -x for more explanation')
    parser.add_argument('in_file', nargs="?", help="survey status csv file")
    parser.add_argument('-c', '--centre', metavar="'RA,Dec'", help="J2000 position to find",
                        default=[0.0, 0.0], action=Celpos)
    parser.add_argument('-r', '--radius', type=float, default=10.0, help="Tile search radius (degrees)")
    # parser.add_argument('-o', '--output', default="swarp_mosaic", help="Name of output fits file")
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-x', '--explain', action='store_true',
                        help="Give an expanded explanation including module load instructions")
    return parser


class Celpos(ap.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not allowed")
        super(Celpos, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        # logger.debug('ACTION : %r %r %r' % (namespace, values, option_string))
        a, b = parse_direction(values)
        rp = [np.radians(a), np.radians(b)]
        # noinspection PyUnresolvedReferences
        setattr(namespace, self.dest, rp)


class Fields:
    def __init__(self, fname):
        self.fields = ascii.read(fname, format='csv')
        # noinspection PyUnresolvedReferences
        self.direction = SkyCoord(Angle(self.fields["RA_HMS"], unit=au.hourangle),
                                  Angle(self.fields["DEC_DMS"], unit=au.deg))
        self.num_fields = len(self.direction)

    def find(self, src_dir, src_sep=1.0):
        seps = self.direction.separation(src_dir).deg
        within_beam = np.where(seps < src_sep)
        return self.fields[within_beam[0]]

    def find_closest(self, src_dir):
        seps = self.direction.separation(src_dir).deg
        closest = seps.min()
        j = np.where(seps == closest)
        return self.fields[j]


def main():
    # parse command line options
    print("\n     racs_find\n\n")
    args = arg_init().parse_args()
    verbose = args.verbose

    if args.explain:
        print(EXPLANATION)
        sys.exit(0)
    if verbose:
        print("ARGS = ", args)

    ra, dec = args.centre
    src_dir = Skypos(ra, dec)        # ASKAP package, inputs are RA and DEC
    ra_str, dec_str = src_dir.get_ras(), src_dir.get_decs()

    # noinspection PyUnresolvedReferences
    src_dir = SkyCoord(Angle(ra_str, unit=au.hourangle), Angle(dec_str, unit=au.deg))

    # max_sep = 1.0
    fields = Fields(args.in_file)
    print ("Found {:d} fields.".format(fields.num_fields))

    src_fields = fields.find_closest(src_dir)
    print("Closest field:")
    print(src_fields[0]['FIELD_NAME'], src_fields[0]['SBID'], src_fields[0]['CAL_SBID'], src_fields[0]['STATE'])

    src_fields = fields.find(src_dir, src_sep=12.0)
    print ("\nOther nearby fields:")
    for s in src_fields:
        print(s['FIELD_NAME'], s['SBID'], s['CAL_SBID'], s['STATE'])


if __name__ == "__main__":
    sys.exit(main())

# ra_str = sys.argv[1]
# dec_str = sys.argv[2]
# src_dir = SkyCoord(Angle(ra_str, unit=au.hourangle), Angle(dec_str, unit=au.deg))
#
# max_sep = 1.0
# fields = Fields("racs_test4.csv")
# src_fields = fields.find(src_dir, max_sep)
# print(src_fields)
