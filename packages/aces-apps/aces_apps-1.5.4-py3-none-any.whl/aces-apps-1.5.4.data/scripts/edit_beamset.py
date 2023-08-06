#!/usr/bin/env python
"""
Example use of BeamSet and subclasses BeamMeasure.

Copyright (C) CSIRO 2017
"""
import argparse as ap
import sys

import aces.beamset.beamfactory as bf
from aces.beamset.beamset import BeamSet
import numpy as np

HELPSTART = """This helps you edit header information (metadata) in a BeamSet file. A new file
is written with the altered metadata. The interface is simple:
-s Display all metadata items available for editting.
-i item will select metadata[item], display its value and, if -v is used, change it.
-v value, if given will set metadata[item] to value, with a data type the same as the original.

Note that editing metadata items that are lists or arrays is not implemented.
"""

"""
2018-May-19  Add function to check the metadata contents against defaults expected.

"""
EXPLANATION = HELPSTART


def arg_init():
    """Define the interprestation of command line arguments.
    """
    parser = ap.ArgumentParser(prog='edit_beamset.py',
                               formatter_class=ap.RawDescriptionHelpFormatter,
                               description=HELPSTART,
                               epilog='See -x for more explanation')
    parser.add_argument('infile', nargs="?", help="Data file (hdf5 format)")
    parser.add_argument('-o', '--output', default=None, help="Name of output file")
    parser.add_argument('-i', '--item', default=None, help="Item to edit")
    parser.add_argument('-n', '--new_value', default=None, help="New value to set")
    parser.add_argument('-k', '--keyword', default=None, help="Correct name of keyword for chosen item")
    parser.add_argument('-s', '--show', action='store_true', help="Show all metadata items")
    parser.add_argument('-r', '--remove', action='store_true', help="Remove this metadata item")
    parser.add_argument('-p', '--print_val', action='store_true', help="Print item value in full")
    parser.add_argument('-d', '--dryrun', action='store_true', help="Do not write new file")
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-x', '--explain', action='store_true', help="Give an expanded explanation")
    return parser


def boolify(s):
    if s == 'True':
        return True
    if s == 'False':
        return False
    raise ValueError("huh?")


def autoconvert(s):
    for fn in (boolify, int, float):
        try:
            return fn(s)
        except ValueError:
            pass
    return s


def show_items(md):
    print("\n  Items available for editing are: \n")
    for k, v in list(md.items()):
        if type(v) in [list, tuple, np.ndarray]:
            sv = '[]'
        else:
            sv = v
        print("%20s : %s" % (k, sv))

def check_metadata_items(obj):
    md = obj.metadata
    cl = obj.__class__
    dkeys = list(BeamSet.metadataDefaults.keys())
    subkeys = cl.metadataDefaults
    unrecog = []
    for k in list(md.keys()):
        if k in dkeys:
            print("{:20s} recognised ({})".format(k, 'BeamSet'))
        elif k in subkeys:
            print("{:20s} recognised ({})".format(k, cl))
        else:
            print("{:20s} NOT recognised".format(k))
            unrecog.append(k)
    print("end check")
    return unrecog

def main():
    # parse command line options
    print("\n     edit_beamset\n\n")

    args = arg_init().parse_args()
    if args.explain:
        print(EXPLANATION)
        sys.exit(0)
    if args.verbose:
        print("ARGS = ", args)

    if args.infile:
        infile = args.infile
    else:
        print("Try -h for help")
        sys.exit(0)

    if args.output:
        outfile = args.output.split('.')[0] + '.hdf5'
    else:
        outfile = args.infile.split('.')[0] + '_edit.hdf5'

    print("Reading {}.  ".format(infile))

    item = args.item
    value = args.new_value
    show = args.show
    print_val = args.print_val
    dryrun = args.dryrun

    in_obj = bf.load_beamset_class(infile)
    in_obj.print_summary()
    md = in_obj.metadata
    unrecog = check_metadata_items(in_obj)
    if len(unrecog) > 0:
        print("Some metadata keywords are not recognised. Consider correcting them with -k option.")
        print("Alternatively ensure they exist in the metadataDefaults for thei (sub)class.")
        for u in unrecog:
            print("{:20s} is not recognised".format(u))

    do_save = False
    if show:
        in_obj.print_summary()
        show_items(md)
    elif print_val:
        print("metadata['{}'] = {}".format(item, md[item]))
    else:
        if item in list(md.keys()):
            d = in_obj.data
            f = in_obj.flags
            cls = in_obj.__class__
            out_obj = cls(md, d, f)
            if args.new_value:
                old_val = md[item]
                typ_val = type(old_val)
                print("Current value metadata[{}] = {}".format(item, old_val))
                if value is not None:
                    if typ_val in [list, tuple, np.ndarray]:
                        print("Editing items of type {} is not implemented".format(typ_val))
                    else:
                        # new_val = autoconvert(value)
                        new_val = typ_val(value)
                        h_item = "metadata[{}] changed from {} to {}".format(item, old_val, new_val)
                        print(h_item)
                        out_obj.metadata[item] = autoconvert(value)
                        out_obj.add_to_history('metadata editted: ' + h_item)
                        do_save = True
            elif args.keyword:
                out_obj.metadata[args.keyword] = md[item]
                out_obj.add_to_history('metadata keyword changed: ' + args.keyword)
                do_save = True
            elif args.remove:
                del out_obj.metadata[item]
                out_obj.add_to_history('metadata item "{}" removed: '.format(item))
                do_save = True

            out_obj.print_summary()

            if dryrun:
                print("No output file written; '-d' selected.")
            elif do_save:
                out_obj.write_to_hdf5(outfile)
                print("Writing {}.  ".format(outfile))
        else:
            print("{} is not an item in metadata.".format(item))
            show_items(md)


if __name__ == "__main__":
    sys.exit(main())
