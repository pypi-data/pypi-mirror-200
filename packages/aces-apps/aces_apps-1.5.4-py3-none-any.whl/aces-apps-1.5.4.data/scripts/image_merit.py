#!/usr/bin/env python
from __future__ import print_function

"""
Tool for quick image assessment.

Copyright (C) CSIRO 2017
"""
import argparse as ap
import sys
from pathlib import Path

import aces.misc.image_stats as ims

EXPLANATION = """TBD.
"""
HELPSTART = """This produces simple figures of merit.
v 2019Nov29

"""


def arg_init():
    """Provide essential data for interpreting command line arguments.
    """
    parser = ap.ArgumentParser(prog='image_merit',
                               formatter_class=ap.ArgumentDefaultsHelpFormatter,
                               description=HELPSTART,
                               epilog='See -x for more explanation')
    parser.add_argument('in_file', nargs="+", help="Image file")
    parser.add_argument('-c', '--cellsize', type=int, default=100, help='Cell size in pixels')
    parser.add_argument('-n', '--nomask', action='store_true', help='Select to disable edge masking in statistics '
                                                                    'determination')
    parser.add_argument('-r', '--replace', action='store_true', help='Replace existing statistics file')
    parser.add_argument('-s', '--statistic', choices=['rms', 'min', 'rat', 'iqr'], default='rms', help="Statistic to compute")
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-x', '--explain', action='store_true', help="Give an expanded explanation")
    return parser


def main():
    # parse command line options
    print ("\n     image_merit\n\n")
    args = arg_init().parse_args()
    verbose = args.verbose
    statistic = args.statistic

    if args.explain:
        print (EXPLANATION)
        sys.exit(0)
    if verbose:
        print ("ARGS = ", args)

    if args.in_file:
        in_files = args.in_file
        if in_files[0].startswith('@'):
            files = open(in_files[0][1:], 'rU').readlines()
            in_files = [f.strip() for f in files]
    else:
        print ("Try -h for help")
        sys.exit(0)
    mask_it = not args.nomask
    out_dir = Path('.')
    for in_file in in_files:
        input = Path(in_file)
        mos_stats, stats, fname = ims.image_cell_statistic(input, out_dir, cellsize=args.cellsize, statistic=statistic,
                                                do_mask=mask_it, replace_old=args.replace)
        print ("Statistics file is {}".format(fname))

        things = sorted(stats.keys())
        for thing in things:
            if thing != "speed":
                lab = 'rms'
                unit = 'microJy'
                fmt = "   {} {:.1f} {}"
                label = "{:3s} {:12s}".format(lab, thing)
                print(fmt.format(label, stats[thing], unit))
        if 'speed' in things:
            lab = ""
            unit = 'microJy^2  sq_deg'
            fmt = "   {} {:.6f} {}"
            label = "{:3s} {:12s}".format(lab, 'speed')
            print(fmt.format(label, stats['speed'], unit))

    return 0


if __name__ == "__main__":
    sys.exit(main())
