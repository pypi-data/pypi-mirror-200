#!/usr/bin/env python3
"""
Script to populate a measurementset with a visibility model.

Copyright (C) CSIRO 2018
"""
from casacore.tables import *
import numpy as np
import sys
import os
import string
from aces.holography import cmpmod
import argparse as ap
from tqdm import tqdm
from aces.askapdata.schedblock import SchedulingBlock
import logging

log = logging.getLogger(__name__)

def cli():
    explanation = """This script divides visibilities in a measurementset with a visibility model.
    """
    help_start = """Generates model visibilities for a given component model for
    a given measurementset and divides the observed visibilities with the
    generated visibilities. The resultant visibilities are stored in the
    "CORRECTED_DATA" column of the measurementset.
    """
    explanation += "/n%s" % help_start
    parser = ap.ArgumentParser(prog='divmod.py',
                               formatter_class=ap.RawDescriptionHelpFormatter,
                               description=help_start,
                               epilog='See -h for help')
    parser.add_argument("mySBID", type=int, help="SBID of observation")
    parser.add_argument("msFile", type=str, help="Measurementset (ms format)")
    parser.add_argument('modelFile', type=str,
                        help="Component model file (difmap format)")
    args = parser.parse_args()
    main(
        args.mySBID,
        args.msFile,
        modelFile=args.modelFile
    )


def main(mySBID, msFile, modelFile):
    log.info(
        f"{msFile} - Adding {modelFile}"
    )
    
    # Get Schedblock info
    sb = SchedulingBlock(mySBID)
    # Get reference antenna number
    myRA = int(''.join(filter(lambda char: char in string.digits,
                              sb.get_parameters()['holography.ref_antenna'])))
    iRA = myRA - 1  # Antenna index
    # Read the component model
    model = cmpmod.ComponentModel()
    model.read(modelFile)

    # Make the MODEL_DATA and CORRECTED_DATA columns if they don't already exist
    addImagingColumns(msFile)

    # Open the measurementset data
    tb = table(msFile, readonly=False)
    t = taql(
        'select from $tb where ANTENNA1 = $iRA or ANTENNA2 = $iRA'
    )
    # Open the SPECTRAL_WINDOW table to access the channel frequencies
    t_spec_window = table("%s/SPECTRAL_WINDOW" % (msFile))

    # Extract the array of channel frequencies
    freqs = t_spec_window[0]["CHAN_FREQ"]

    uvw_values = t.getcol("UVW")
    mod_vis = np.array([
        model.getmodvis(
            uvw_values,
            freq
        )
        for freq in tqdm(
            freqs,
            desc='Getting model visibilities'
        )
    ]
    )
    del uvw_values
    new_uv_data_values = t.getcol("DATA")
    new_uv_data_values /= mod_vis.T[:, :, np.newaxis]
    t.putcol("MODEL_DATA", mod_vis.T[:, :, np.newaxis])
    del mod_vis

    t.putcol("CORRECTED_DATA", new_uv_data_values)

    del new_uv_data_values
    t.close()
    t_spec_window.close()


if __name__ == "__main__":
    sys.exit(cli())
