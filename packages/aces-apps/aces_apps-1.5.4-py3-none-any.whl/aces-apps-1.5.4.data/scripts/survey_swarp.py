#!/usr/bin/env python
from __future__ import print_function

"""
Tool to launch swarp for mosaicing survey tiles.

Copyright (C) CSIRO 2019
"""
import os
import argparse as ap
import sys
import numpy as np

from astropy.io import ascii
from askap.footprint import Skypos
from askap.coordinates import parse_direction

EXPLANATION = """
% You will need to get the correct environment (on Zeus?) as follows:
source /group/mwa/software/module-reset.sh
module use /group/mwa/software/modulefiles
module load mwapy
module load manta-ray-client
module load MWA_Tools
"""
HELPSTART = """This launches swarp.
v 2019Jun24
"""

def arg_init():
    """Provide essential data for interpreting command line arguments.
    """
    parser = ap.ArgumentParser(prog='racs_swarp',
                               formatter_class=ap.ArgumentDefaultsHelpFormatter,
                               description=HELPSTART,
                               epilog='See -x for more explanation')
    parser.add_argument('in_file', nargs="?", help="survey status csv file")
    parser.add_argument('-c', '--centre', metavar="'RA,Dec'", help="J2000 position mosaic centre",
                        default=[0.0, 0.0], action=Celpos)
    parser.add_argument('-r', '--radius', type=float, default=10.0, help="Tile search radius (degrees)")
    parser.add_argument('-o', '--output', default="swarp_mosaic", help="Name of output fits file")
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-x', '--explain', action='store_true', help="Give an expanded explanation including module load instructions")
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

def make_lists(infile, refpos, radius):
    """

    :param infile: racs_status_SkyScan_<id>.csv file
    :param refpos: [ra, dec] of centre (radians)
    :param radius: in degrees
    """

    if os.path.exists(infile):
        data = ascii.read(infile, format='csv')

    else:
        print("")
        print("ERROR: RACS status summary CSV file {} not found".format(infile))
        print("")
        sys.exit()

    ind_good = np.where(data['DEC_DEG'] <= 40)  # only grab the locations that are observable with ASKAP
    data = data[ind_good]                       # re-structure data to only have good locations

    # Generate coordinate transformation based on user's preference position: place it at the origin.
    ra, dec = refpos
    origin = Skypos(ra, dec)        # ASKAP package, inputs are RA and DEC

    ra_all = data['RA_DEG']                 # RA in degrees
    dec_all = data['DEC_DEG']               # DEC in degrees
    fld_all = data['FIELD_NAME']
    sbid_all = data['SBID']

    tc = []
    for rai, deci in zip(ra_all,dec_all):
        # noinspection PyTypeChecker
        tc.append(Skypos(np.radians(rai), np.radians(deci)))

    rad = np.radians(radius)
    fld_select = []
    sbid_select = []
    for i,t in enumerate(tc):
        if origin.d_pa(t)[0] < rad:
            fld_select.append(fld_all[i])
            sbid_select.append(sbid_all[i])
    print ("{:d} fields selected".format(len(fld_select)))
    pre0 = os.environ['RACS']
    pre_i = pre0+"FLD_IMAGES/stokesI/image.i.SB{:d}.cont."
    pre_w = pre0+"FLD_IMAGES/weights/weights.i.SB{:d}.cont."

    post_i = ".linmos.taylor.0.restored.fits"
    post_w = ".linmos.taylor.0.fits"
    list_i, list_w = [],[]
    for fld, sb in zip(fld_select, sbid_select):
        list_i.append((pre_i+fld+post_i).format(sb))
        list_w.append((pre_w+fld+post_w).format(sb))
    return list_i, list_w


def main():
    # parse command line options
    print("\n     racs_swarp\n\n")
    args = arg_init().parse_args()
    verbose = args.verbose

    if args.explain:
        print(EXPLANATION)
        sys.exit(0)
    if verbose:
        print("ARGS = ", args)

    fname = args.output
    racs_csv = args.in_file
    centre = args.centre
    radius = args.radius
    i_list, w_list = make_lists(racs_csv, centre, radius)
    fnames = {'im': 'tmp_image_list.txt', 'wt': 'tmp_weigh_list.txt'}
    fil = {}
    for k, v in fnames.items():
        if os.path.exists(v):
            print ("Deleting previous {}".format(v))
            os.remove(v)
        fil[k] = open(v, 'w')
    for ii, wi in zip(i_list, w_list):
        if os.path.exists(ii):
            fil['im'].write(ii + '\n')
            fil['wt'].write(wi + '\n')
            print ("{}  {}".format(ii, wi))
        else:
            print ("Not found : {}".format(ii))
    fil['im'].close()
    fil['wt'].close()

    cmd = "swarp -VMEM_MAX 4095 -MEM_MAX 2048 -COMBINE_BUFSIZE 2048"
    cmd += " -IMAGEOUT_NAME {}.fits".format(fname)
    cmd += " -WEIGHTOUT_NAME {}.weight.fits".format(fname)
    cmd += " -WEIGHT_TYPE MAP_WEIGHT -WEIGHT_IMAGE @{} -WEIGHT_SUFFIX .weight.fits".format(fnames['wt'])
    cmd += " -RESCALE_WEIGHTS Y -COMBINE Y -COMBINE_TYPE WEIGHTED -SUBTRACT_BACK N -WRITE_XML N"
    cmd += " -PROJECTION_TYPE ZEA"
    cmd += " @{}".format(fnames['im'])
    if verbose:
        print ("swarp command:")
        print (cmd)
    os.system(cmd)

if __name__ == "__main__":
    sys.exit(main())
