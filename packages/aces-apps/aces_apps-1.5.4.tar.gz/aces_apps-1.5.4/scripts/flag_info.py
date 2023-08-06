#!/usr/bin/env python
import argparse
import sys
from casacore.tables import table, tablecommand


"""
Example code for compute flagging percentage in a ms:
    python flag_info.py
* Read msdata
* Compute Flagged data, Unflagged data
* Print useful flagging onformation

                                     --wr, 20Apr2018
"""


def parse_args():
    """
    Parse input arguments
    """
    parser = argparse.ArgumentParser(description='Prints flagging statistics for measurement set')

    parser.add_argument('-i', '--msfile', dest='ms_data', required='true', help='Input measurement set (with path)',
                        type=str)

    if len(sys.argv) < 2:
        parser.print_usage()
        sys.exit(1)

    _args = parser.parse_args()
    return _args


if __name__ == "__main__":
    args = parse_args()

    inTable = args.ms_data
    t = table(inTable, readonly=True)
    visTot = tablecommand('calc sum([select nelements(FLAG) from $t])')
    visFlagged = tablecommand('calc sum([select ntrue(FLAG) from $t])')

    print("Flagging Information for Input msfile: " + inTable)
    print("           Total Visibilities: ", visTot)
    print("         Flagged Visibilities: ", visFlagged)
    print("           Flagged percentage: ", 100.0 * visFlagged / visTot, "%")
    print(" ")
    t.close()
