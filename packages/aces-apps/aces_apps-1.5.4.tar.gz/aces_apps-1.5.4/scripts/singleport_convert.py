#!/usr/bin/env python
"""
Example use of BeamSet and subclasses BeamMeasure.

Copyright (C) CSIRO 2018
"""
import argparse as ap
import sys
import re

import aces.beamset.beamfactory as bf



EXPLANATION = """The singleport_convert process tkes an Holography file containing both single-port and formed-beam data
and splits it into two separate hdf5 files. It adapts the metadata of the single-port file to describe the data.
This maybe a temporary script: some of the functions here can be put directly into the script that writes the original
holography file.
"""
HELPSTART = """The singleport_convert process tkes an Holography file containing both single-port and formed-beam data
and splits it into two separate hdf5 files. 
"""

def arg_init():
    """Define the interprestation of command line arguments.
    """
    parser = ap.ArgumentParser(prog='singleport_convert.py',
                               formatter_class=ap.RawDescriptionHelpFormatter,
                               description=HELPSTART,
                               epilog='See -x for more explanation')
    parser.add_argument('inFile', nargs="?", help="Data file (hdf5 format)")
    parser.add_argument('-p', '--ports', default=None, help="Name of file holding ports list.")
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-x', '--explain', action='store_true', help="Give an expanded explanation")
    return parser


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

    if args.ports:
        ports_file = args.ports
    else:
        ports_file = "ports_list.txt"

    holo_pos = infile.find("holo")
    if holo_pos >= 0:
        p = holo_pos + 4
    else:
        p = infile.find(".hdf5")
    outfile_sp = infile[:p] + '_sp.hdf5'
    outfile_fb = infile[:p] + '_fb.hdf5'

    old = bf.load_beamset_class(infile)

    try:
        portlist = open(ports_file, 'rU').readlines()[0]

        # portlist = '[[6, 7], [8, 9], [10, 11], [14, 15], [16, 17], [18, 19], [20, 21], [24, 25], [26, 27], [28, 29],' \
        #        '[30, 31], [34, 35], [36, 37], [38, 39], [40, 41], [44, 45], [46, 47], [48, 49], [50, 51], [54, 55],' \
        #        '[56, 57], [58, 59], [60, 61], [64, 65], [66, 67], [68, 69], [70, 71], [74, 75], [76, 77], [78, 79],' \
        #        '[80, 81], [84, 85], [86, 87], [88, 89]]'
        p1 = re.findall('[0-9]+', portlist)
        p2 = list(map(int, p1))
        npo = len(p2)
        print("Found {:d} ports.".format(npo))
    except IOError:
        print("{} file not found".format(ports_file))
        sys.exit()

    # Create the new object and populate the metadata
    new_md = old.get_metadata()
    new_md['beamType'] = 'singleport'
    new_md['beams'] = p2
    new_md['polarizations'] = ['XX']
    # Skip the reference antenna
    # todo  Don't assume AK01 is reference
    new_md['antennas'] = old.get_metadata()['antennas'][1:]
    new_obj = old.__class__(new_md)

    for ia in range(1, old.Na):
        for ip in [0, 1]:
            for ib in range(npo/2):
                ob = ib*2 + ip
                new_obj.data[0, ia-1, ob, 0, :] = old.data[0, ia, ib+1, ip, :]
                new_obj.flags[0, ia-1, ob, 0, :] = old.flags[0, ia, ib+1, ip, :]

    new_obj.add_to_history("Translated to single port format")
    new_obj.write_to_hdf5(outfile_sp)

    # todo  Write out formed boresight beam, if present
    # todo  Handle Y ports, or a mixture of x and Y ports.

if __name__ == "__main__":
    sys.exit(main())
