#!/usr/bin/env python
from __future__ import print_function

"""
sefd_convert
Takes the pickle files written by sefdProcessing on Galaxy, and converts to
an hdf5 file in the beamset format.

 $Author: mcc381 $


"""
import argparse as ap
import glob
import os
import pickle
import sys
import time
import re

import numpy as np

from aces.beamset.sefdset import SEFDSet
import logging

"""
sefd_convert reads from a set of files 
    /SEFD_A-<sbid>-beamBB.pkl

<sbid> is the scheduling block ident, and BB is the beam
number

sefd_convert writes a single file (hdf5) to the working directory:
    SEFD_<sbid>.hdf5
    
"""


def arg_init():
    parser = ap.ArgumentParser(prog='sefd_convert', formatter_class=ap.RawDescriptionHelpFormatter,
                               description='SEFD convert',
                               epilog='See -x for more explanation')
    # noinspection PyTypeChecker
    parser.add_argument('sbid', type=int, help="SBID")
    parser.add_argument('-d', '--dir', default='.', help="Input directory")
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-x', '--explain', action='store_true', help="Give an expanded explanation")
    return parser


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


SEFD_params = {1925: {'fpname': 'square_6x6', 'pitch': 0.9, 'angle': 0.0},
               1932: {'fpname': 'square_6x6', 'pitch': 0.9, 'angle': 0.0},
               1947: {'fpname': 'closepack30', 'pitch': 0.9, 'angle': 0.0},
               1948: {'fpname': 'closepack30', 'pitch': 0.9, 'angle': 0.0}}

pols = ['XX', 'XY', 'YX', 'YY']
ipols = [0, 1, 2, 3]
pols_par = ["XX", "YY"]
ipols_par = [0, 3]
root2 = np.sqrt(2.0)


class SEFDPlot(object):
    _directory = "%s/askap/ASKAP/sensitivity" % (os.environ['HOME'])

    # _directory = "/Volumes/BACKUP-02/askap"

    def __init__(self, sbid):
        self.flags = None
        self.autos = None
        self.autom = None
        self.raw = None
        self.sefd = None
        self.scale = None
        stub1 = "SEFD_A-%d_beam%d.pkl"
        stub2 = "SEFD_A-%d_beam%02d.pkl"
        gstub = "SEFD_A-%d_beam*.pkl"

        self.sbid = sbid
        cwd = os.path.basename(os.getcwd())
        self.prefix = None
        if '_' in cwd:
            self.prefix = cwd.split('_')[0]
        gquery = gstub % sbid
        pfiles = glob.glob(gquery)
        ants = set()
        q = None
        if not pfiles:
            print(gquery)
            raise IOError('Pickle files not found at {}'.format(gquery))
        else:
            for fname in pfiles:
                q = pickle.load(open(fname, 'rb'))
                ants = ants.union(q['SEFD'][0].keys())

        self.ants = sorted(list(ants))

        # The latest pickle loaded should have valid data; get its shape.
        dim_ft = q['SEFD'][0][self.ants[0]].shape
        if len(dim_ft) == 1:
            self.dim_ft = (dim_ft[0], 1)
        else:
            self.dim_ft = dim_ft

        if 'FLAGS' in q:
            self.baselines = q['FLAGS'][0].keys()
        else:
            self.baselines = []
        if 'META' in q:
            self.meta = q['META']
        else:
            self.meta = {}
        self._set_fp_params(sbid)

        self.frq = q['FREQ']
        self._make_data_struct('sefd', pols, self.ants)
        self._make_data_struct('poly', pols, self.ants)
        self._make_data_struct('scale', pols, self.ants)
        self._make_data_struct('raw', pols, self.ants)
        self._make_data_struct('autom', pols, self.ants)
        self._make_data_struct('autos', pols, self.ants)
        self._make_data_struct('flags', pols, self.baselines)

        if 'TIME' in q.keys():
            self.time = np.array(q['TIME'])
        else:
            self.time = np.array(range(self.dim_ft[1]))

        for b in range(36):
            q = None
            for st in [stub1, stub2]:
                fname = st % (sbid, b)
                if os.path.exists(fname):
                    q = pickle.load(open(fname, 'rb'))
                    break
            if q:
                for i, po in zip(ipols, pols):
                    for k in self.ants:
                        if k in q['SEFD'][i].keys():
                            qs = q['SEFD'][i][k]
                            qs = np.ma.masked_array(qs, qs < 10.0)
                            qs.mask = np.ma.mask_or(qs.mask, qs > 40000.0)
                            self.sefd[po][k][b] = qs
                            if i in ipols_par:
                                if 'SCALE' in q:
                                    self.scale[po][k][b] = q['SCALE'][i][k]
                                if 'RAWAMPL' in q:
                                    self.raw[po][k][b] = q['RAWAMPL'][i][k]
                                if 'AUTOM' in q:
                                    self.autom[po][k][b] = q['AUTOM'][i][k]
                                if 'AUTOS' in q:
                                    self.autos[po][k][b] = q['AUTOS'][i][k]
                    for k in self.baselines:
                        self.flags[po][k][b] = q['FLAGS'][i][k]

        self.beams = self.sefd[pols[0]][self.ants[0]].keys()

    def _make_data_struct(self, name, pol, ants):
        setattr(self, name, {})
        r = getattr(self, name)
        for p in pol:
            r[p] = {}
            for a in ants:
                r[p][a] = {}

    def summary(self):
        print ("SEFD for SBID%d  (%s)" % (self.sbid, self.prefix))
        pol = self.sefd.keys()
        ants = self.ants
        print ("Beams %s" % self.beams)
        print ("Ants  %s" % ants)
        print ("Pols  %s" % pol)
        sh = self.dim_ft
        print ("%d x %d  F x T cells" % (sh[0], sh[1]))
        print ("Frequency range %6.1f - %6.1f MHz" % (self.frq[0], self.frq[-1]))
        print ("Time range      %6.1f - %6.1f s" % (self.time[0], self.time[-1]))

    def _set_fp_params(self, sbid):
        if sbid in SEFD_params.keys():
            p = SEFD_params[sbid]
            self.fpname = p['fpname']
            self.pitch = p['pitch']
            self.angle = p['angle']
        else:
            if 'footprint.name' in self.meta:
                self.meta = meta_legacy(self.meta)
                self.fpname = self.meta['footprint.name']
                self.pitch = float(self.meta['footprint.pitch'])
                self.angle = self.meta['footprint.rotation']
            else:
                print ("ERROR: no known FP params for sbid %d" % sbid)

    def save_hdf5(self, filename=None):
        # Save the SEFD data as an hdf5 file in the "beamset" format.
        # This defines an array with five dimensions: time, ant, beam, pol, frq
        # and in this case assigns a payload of one float to each point in the grid.
        # It will unpack into an object of class SEFDset, based on class beamset.
        # 2017 Oct 23
        sbid = self.sbid
        times = self.time
        ants = self.ants
        beams = self.beams
        frqs = self.frq
        meta = self.meta
        md = {'class': 'SEFDSet',
              'times': times,
              'antennas': ants,
              'beams': beams, 'frequencies': [],
              'freq_range': [frqs[0], frqs[-1], len(frqs)],
              'polarizations': pols,
              'payloadshape': (1,),
              'fp_name': self.fpname,
              'fp_pitch': 0.9,
              'fp_angle': 0.0,
              'beamformingSBID': -1,
              'beamformingPA': 0.0,
              'beamformingEpoch': 0.0,
              'holographySBID': -1, 'holographyEpoch': 0.0,
              'calSBID': sbid,
              'beamType': 'formed',
              'history': [time.asctime() + ": First Created"]}

        pitch = self.pitch
        angle = self.angle
        md['fp_pitch'] = pitch
        md['fp_angle'] = angle
        md['beamformingSBID'] = -1
        if 'beam_weights' in meta:
            print ('beam forming : ', meta['beam_weights'])
            beam_wts = meta['beam_weights']
            md['beam_weights'] = beam_wts
            # next if block temporary
            if len(beam_wts) > 0:
                try:
                    tmp = beam_wts.split('_')[0]
                    digits = re.findall('[0-9]+', tmp)[0]
                    md['beamformingSBID'] = int(digits)
                except ValueError as ve:
                    print (ve)
                    print ('no beam weights found')
        obj = SEFDSet(metadata=md)
        obj.print_summary()

        # Now copy the SEFD data themselves
        # nti = len(self.time)
        nti = self.sefd[pols[0]][ants[0]][beams[0]].shape[1]
        nch = len(self.frq)
        seli = {'times': range(nti), 'channels': 0}
        selv = {}
        for thing in ['antennas', 'beams', 'polarizations']:
            selv[thing] = obj.metadata[thing]
        selector = obj.get_selector(seli, selv)
        for s in selector:
            t, ant, beam, pol, freq = obj.get_vector(s)
            i, j, k, l, m = s
            try:
                obj.data[i, j, k, l, :, 0] = self.sefd[pol][ant][beam][:nch, i]
                obj.flags[i, j, k, l, :] = self.sefd[pol][ant][beam][:nch, i].mask
            except KeyError:
                obj.data[i, j, k, l, :, 0] = 0.0
                obj.flags[i, j, k, l, :] = True
                logging.debug('Missing item pol,ant,beam  :[{}][{}][{}]'.format(pol, ant, beam))

        # Write to a file with default name, unless overridden
        if filename is None:
            fname = "SEFD_{:d}.hdf5".format(self.sbid)
        else:
            fname = filename
        logging.info('Writing to file {}'.format(fname))
        obj.write_to_hdf5(fname)


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
            print ("k, v : ", k, v)
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
        # sys.exit()

    sep = SEFDPlot(args.sbid)
    sep.summary()
    sep.save_hdf5()
    logging.info('finished')

# ====END of process ================


if __name__ == "__main__":
    fmt = '%(asctime)s %(levelname)s  %(name)s %(message)s'
    logging.basicConfig(format=fmt, level=logging.DEBUG)
    sys.exit(main())
