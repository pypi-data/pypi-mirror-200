#!/usr/bin/env python3
import sys
import os
import argparse
from casacore.tables import *
import numpy as np
import logging as log


def main(sbid, mslist, workdir="."):
    workdir = os.path.abspath(workdir)
    ms = mslist[0]
    t = table(ms, readonly=True)
    tp = table(f"{ms}/POINTING")
    p_phase = tp.getcol("DIRECTION")
    p_phase.dump(f"{workdir}/SB{sbid:d}_beam00.pointing")
    ti = tp.getcol("TIME")
    ti.dump(f"{workdir}/SB{sbid:d}_beam00.time")
    az = tp.getcol("AZIMUTH")
    az.dump(f"{workdir}/SB{sbid:d}_beam00.azimuth")
    el = tp.getcol("ELEVATION")
    el.dump(f"{workdir}/SB{sbid:d}_beam00.elevation")
    pa = tp.getcol("POLANGLE")
    pa.dump(f"{workdir}/SB{sbid:d}_beam00.polangle")

    t.close()
    tp.close()
    log.info("Dumped field table for beam 0")


def cli():
    descStr = """
    Get pointing data from holography
    """
    # Parse the command line options
    parser = argparse.ArgumentParser(
        description=descStr, formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "mySBID", metavar="mySBID", type=int, help="Holography SBID to process."
    )
    parser.add_argument(
        "mslist",
        metavar="mslist",
        type=str,
        help="Input holography measurement sets.",
        nargs="+",
    )
    parser.add_argument(
        "workdir", metavar="workdir", type=str, help="Working directory."
    )

    args = parser.parse_args()

    main(sbid=args.mySBID, mslist=args.mslist, workdir=args.workdir)


if __name__ == "__main__":
    sys.exit(cli())
