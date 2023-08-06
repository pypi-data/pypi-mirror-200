#!/usr/bin/env python
from __future__ import print_function

"""
sefd_merge
Takes the individual hdf5 files written by sefdProcessing on Galaxy, and merges to
a single hdf5 file in the beamset format.

 $Author: mcc381 $


"""
import argparse as ap
import glob

import sys
import numpy as np

import aces.beamset.beamfactory as bf
from aces.beamset.sefdset import SEFDSet
import logging

"""
sefd_merge reads from a set of files 
    /SEFD_A-<sbid>-beamBB.pkl

<sbid> is the scheduling block ident, and BB is the beam
number

sefd_merge writes a single file (hdf5) to the working directory:
    SEFD_<sbid>.hdf5
    
"""


def arg_init():
    parser = ap.ArgumentParser(prog='sefd_merge', formatter_class=ap.RawDescriptionHelpFormatter,
                               description='SEFD merge',
                               epilog='See -x for more explanation')
    # noinspection PyTypeChecker
    parser.add_argument('sbid', type=int, help="SBID")
    parser.add_argument('-d', '--dir', default='.', help="Input directory")
    parser.add_argument('-o', '--out_file', default=None, help="Output file name")
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-x', '--explain', action='store_true', help="Give an expanded explanation")
    return parser


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


pols = ['XX', 'XY', 'YX', 'YY']
ipols = [0, 1, 2, 3]
pols_par = ["XX", "YY"]
ipols_par = [0, 3]
root2 = np.sqrt(2.0)


def meta_legacy(m):
    """
    A temporary function to deal with tests on old-style outputs from sefdProcessing. It replaces single element
    lists with scalars, and in one case changes the key name of one entry.
    :param m: The meta directory, whose details structure was changed recently (2018-FEB-24)
    :return: The meta directory in the form that conforms to current expectations.
    """
    if isinstance(m['footprint.pitch'], list):
        m_out = {}
        for k, v in m.items():
            print("k, v : ", k, v)
            if len(v) == 0:
                logging.warning("No value found for %s" % k)
                m_out[k] = 0.0
            else:
                m_out[k] = v[0]
        if 'footprint.PA' in m:
            m_out['footprint.rotation'] = m_out['footprint.PA']
            del m_out['footprint.PA']
    else:
        m_out = m.copy()
    return m_out


def main():
    # Set up logging
    logging.info('started')
    args = arg_init().parse_args()
    if args.verbose:
        print ("ARGS = ", args)

    sbid = args.sbid
    out_file = args.out_file
    gq = 'SEFD_A-{:d}_beam_???.hdf5'.format(sbid)
    files = glob.glob(gq)
    f_ranges = []
    beams = []
    antennas = []
    inputs = []
    for f in files:
        obj = bf.load_beamset_class(f)
        inputs.append(obj)
        antennas += list(obj.metadata['antennas'])
        beams.append(obj.metadata['beams'][0])
        f_ranges.append(obj.metadata['freq_range'])

    antennas = sorted(list(set(antennas)))
    beams = sorted(list(set(beams)))

    f_ranges = np.array(f_ranges)
    f1 = f_ranges[:, 0]
    f2 = f_ranges[:, 1]
    nf = f_ranges[:, 2]
    f1s = sorted(list(set(f1)))
    f2s = sorted(list(set(f2)))
    nb = len(f1s)
    ns = list(set(nf))
    df1 = (f2s[0] - f1s[0]) / (ns[0] - 1)
    grand_df = (f2s[-1] - f1s[0]) / (nb * ns[0] - 1)
    if len(ns) == 1 and abs(grand_df - df1) < 1.0e-9:
        new_freq_range = [f1s[0], f2s[-1], nb * ns[0]]
    else:
        print ("Discontigous window?")
        print ("This had better be fixed to handle this case.")
        print ("Aborting!")
        sys.exit()

    new_md = inputs[0].get_metadata()
    new_md['antennas'] = antennas
    new_md['beams'] = beams
    new_md['freq_range'] = new_freq_range

    merged = SEFDSet(metadata=new_md)
    freqs = merged.frequencies
    n_t, n_a, n_b, n_p, n_f = merged.containerShape
    for inp in inputs:
        this_ants = inp.metadata['antennas']
        this_bm = inp.metadata['beams'][0]
        this_frange = inp.metadata['freq_range']
        wh = np.where(beams == this_bm)
        ib = wh[0][0]
        wh = np.where(abs(freqs - this_frange[0]) < 1.0e-4)
        ich1 = wh[0][0]
        ich2 = ich1 + int(this_frange[2])
        for a in this_ants:
            ia = antennas.index(a)
            ja = this_ants.tolist().index(a)
            masked = np.ma.masked_invalid(inp.data[:, ja:ja+1, 0, :, :])
            merged.data[:, ia, ib:ib+1, 0:n_p, ich1:ich2] = masked.data
            merged.flags[:, ia, ib:ib+1, 0:n_p, ich1:ich2] = masked.mask[:, :, :, :, 0]

    if out_file is None:
        fname = "SEFD_{:d}.hdf5".format(sbid)
    else:
        fname = out_file
    merged.add_to_history("Creating merged file")
    logging.info('Writing to file {}'.format(fname))
    merged.write_to_hdf5(fname)
    logging.info('finished')

# ====END of process ================


if __name__ == "__main__":
    fmt = '%(asctime)s %(levelname)s  %(name)s %(message)s'
    logging.basicConfig(format=fmt, level=logging.DEBUG)
    sys.exit(main())
