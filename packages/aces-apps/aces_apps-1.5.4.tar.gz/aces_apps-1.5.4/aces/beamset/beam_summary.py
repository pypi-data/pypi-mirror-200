#!/usr/bin/env python
"""
Example script to read and interpret BeamModel files.

Copyright (C) CSIRO 2017
"""

import argparse as ap
import sys

from aces.beamset import beamfactory

explanation = "You asked for an explanation but there is none.\n"


def arg_init():
    """
    Setup parser for command line arguments
    :return: initalised command line argument parser
    :rtype: :class:`argparse.ArgumentParser` object
    """
    parser = ap.ArgumentParser(prog='tilesky', formatter_class=ap.RawDescriptionHelpFormatter,
                               description='',
                               epilog='See -x for more explanation')
    parser.add_argument('inFile', nargs="?", help="Data file (hdf5 format)")
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-x', '--explain', action='store_true', help="Give an expanded explanation")
    return parser


def main():
    """
    
    """
    print("\n     beamSummary\n\n")

    # parse command line options
    args = arg_init().parse_args()
    if args.explain:
        print(explanation)
        sys.exit(0)
    if args.verbose:
        print("ARGS = ", args)

    if args.inFile:
        obj = beamfactory.load_beamset_class(args.inFile)
        obj.print_summary()


if __name__ == "__main__":
    sys.exit(main())
