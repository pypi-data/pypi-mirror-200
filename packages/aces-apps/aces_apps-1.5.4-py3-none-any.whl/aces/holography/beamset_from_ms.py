"""
Get holography data from a measurement set and pack into a beamset object
"""
import argparse
import logging
import string
import sys

import askap.time as at
import casacore.tables as pt
import numpy as np
import pytz
from tqdm import tqdm

import aces.beamset.mapset as ms
from aces.askapdata.schedblock import SchedulingBlock
from aces.holography import holo_filenames as hf

log = logging.getLogger(__name__)

def cli():
    descStr = """
    Get holography data from a measurement set and pack into a beamset object
    """
    # Parse the command line options
    parser = argparse.ArgumentParser(
        description=descStr, formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        'mySBID',
        metavar='mySBID',
        type=int,
        help='Holography SBID to process.'
    )
    parser.add_argument(
        'mslist',
        metavar='mslist',
        type=str,
        help='Input holography measurement sets.',
        nargs='+'
    )
    parser.add_argument(
        'workdir',
        metavar='workdir',
        type=str,
        help='Working directory.'
    )

    parser.add_argument(
        '-c',
        '--correct',
        action='store_false',
        help="Read from CORRECTED_DATA column (default True). If set, will read from DATA column"
    )

    args = parser.parse_args()
    main(
        mySBID=args.mySBID,
        mslist=args.mslist,
        workdir=args.workdir,
        correct=args.correct
    )

# TODO: Revert this code back to being functional. OOP style is not required.
# This is a mess caused by me trying to parallelise in a dumb way in the past.
# TODO: This is also the slowest part of the code. We can use Dask for parallelisation
class BeamSetter:
    def __init__(self, mySBID, mslist, workdir, correct):
        
        sb = SchedulingBlock(mySBID)

        myRA = int(''.join(filter(lambda char: char in string.digits,
                                  sb.get_parameters()['holography.ref_antenna'])))
        myWeights = sb.get_weights_prefix()
        if myWeights[0:2] == "SB":
            myWeights = int(''.join(filter(
                lambda char: char in string.digits, sb.get_weights_prefix().split('_')[0])))
        elif myWeights == 'auto':
            myWeights = int(sb.get_variables()[
                                'schedblock.scan000.weights.id'])
        myFootprint = sb.get_footprint_name()
        myPitch = float(sb.get_footprint_pitch())
        myRotation = float(sb.get_footprint_rotation())
        myGridSize = int(sb.get_parameters()['holography.grid_size'])
        myGridStep = float(sb.get_parameters()['holography.grid_step'])

        # bsb = SchedulingBlock(myWeights)

        # dt = at.isoUTC2datetime(bsb.get_variables()['executive.start_time'])
        # dta = dt.replace(tzinfo=pytz.UTC)
        # bfTime = at.utcDt2mjd(dta)

        bfAngle = float(''.join(filter(lambda char: char in string.digits +
                                                    '.', sb.get_parameters()['common.target.src%d.pol_axis'])))

        log.info(f"Reference Antenna = {myRA}")
        log.info(f"Holography SBID = {mySBID}")
        log.info(f"Weights ID = {myWeights}")

        # Need to set the beams to process manually for now
        beams = [i for i in range(1, len(mslist)+1)]
        beam_arr = np.array(beams)

        log.info(f"The beams that are loaded {beams=}")

        assert len(mslist) == len(
            beams), "Unexpected number of measurement sets"

        myMS = mslist[0]  # beam 0

        with pt.table(myMS + "/ANTENNA") as tba:
            antNames = tba.getcol("NAME")
            ants = []
            for ant in antNames:
                ants.append(int(ant.replace('ak', '')))

        with pt.table(myMS + "/SPECTRAL_WINDOW") as tbs:
            freqNames = tbs.getcol("CHAN_FREQ")
            freqs = []
            for freq in freqNames[0]:
                freqs.append(float(freq / 1000000.0))

        dt = at.isoUTC2datetime(sb.get_variables()['executive.start_time'])
        dta = dt.replace(tzinfo=pytz.UTC)

        holoTime = at.utcDt2mjd(dta)

        offsets = []

        # Reproduced the logic from the observing procedure, without bulk offset support
        for x in range(myGridSize):
            offInDeg = ((x - (myGridSize - 1) / 2.) * myGridStep)
            offsets.append((np.pi / 180.0) * offInDeg)

        try:
            cast_myWeights = int(myWeights)
        except:
            cast_myWeights = str(myWeights)
            
        log.info(f"Casted {type(cast_myWeights)=} from {type(myWeights)=}")

            
        # 'beamformingEpoch': bfTime,
        metadata = {'times': [holoTime],
                    'antennas': ants,
                    'beams': beams,
                    'frequencies': freqs,
                    'polarizations': ['XX', 'XY', 'YX', 'YY'],
                    'fp_name': myFootprint, 'fp_pitch': myPitch, 'fp_angle': myRotation,
                    'beamformingPA': bfAngle,
                    'beamformingSBID': cast_myWeights,
                    'holographyEpoch': holoTime,
                    'holographySBID': mySBID,
                    'payloadshape': [myGridSize, myGridSize],
                    'xAxis': offsets,
                    'yAxis': offsets}

        bm = ms.MapSet(metadata=metadata)
        mds = bm.get_container_shape()
        bm.flags = np.zeros(mds, np.bool_)

        self.mslist = mslist
        self.mds = mds
        self.metadata = metadata
        self.myRA = myRA
        self.beams = beams
        self.ants = ants
        self.freqs = freqs
        self.myGridSize = myGridSize
        self.beam_arr = beam_arr
        self.bm = bm
        self.correct = correct
        self.workdir = workdir
        self.mySBID = mySBID

    def get_mslist(self):
        return self.mslist

    def read_data(self, myMS):
        # Extract the needed data from the measurement set
        with pt.table(myMS) as tb:
            iRA = self.myRA - 1
            # Get the ID of the antenna under test and reject auto-correlations
            with pt.taql(
                    'select from $tb where ANTENNA1 = $iRA or ANTENNA2 = $iRA'
            ) as tbs:
                ANTENNA1 = tbs.getcol("ANTENNA1")
                ANTENNA2 = tbs.getcol("ANTENNA2")
                FEED1 = tbs.getcol("FEED1")
                SCAN = tbs.getcol("SCAN_NUMBER")
                if self.correct:
                    DATA = tbs.getcol("CORRECTED_DATA")
                else:
                    DATA = tbs.getcol("DATA")
                FLAG = tbs.getcol("FLAG")
            # Conjugate if ANTENNA2 is reference -- ACES-584
            DATA[ANTENNA2 == iRA] = np.conjugate(DATA[ANTENNA2 == iRA])
        return iRA, ANTENNA1, ANTENNA2, FEED1, SCAN, DATA, FLAG

    @staticmethod
    def update(iRA, ANTENNA1, ANTENNA2, FEED1, SCAN, DATA, FLAG, temp, ints, flgs, beam_arr):
        ant_1_idx = np.logical_and(iRA == ANTENNA1, iRA != ANTENNA2)
        ant_2_idx = np.logical_and(iRA == ANTENNA2, iRA != ANTENNA1)
        TANT = np.ones_like(ANTENNA1) * np.nan
        TANT[ant_1_idx] = ANTENNA2[ant_1_idx]
        TANT[ant_2_idx] = ANTENNA1[ant_2_idx]
        TANT = TANT.astype(np.int16)
        BEAM = beam_arr[FEED1] - 1

        # CASA docs: Data are flagged bad if the FLAG array element is True.
        flags = np.array([False in flag for flag in FLAG])
        TANT, BEAM, SCAN, DATA, FLAG = TANT[flags], BEAM[flags], SCAN[flags], DATA[flags], FLAG[flags]

        for a, b, s, data, flag in zip(TANT, BEAM, SCAN, DATA, FLAG):
            if a < 0:
                continue
            else:
                temp[0, a, b, :, :, s] += data.T
                ints[0, a, b, :, :, s] += 1
                flgs[0, a, b, :, :, s] += flag.T
        return temp, ints, flgs

    def ms_to_arr(self, mslist):
        temp = np.zeros(self.mds + [len(self.metadata['xAxis']) *
                                    len(self.metadata['yAxis'])], np.complex64)
        ints = np.zeros(self.mds + [len(self.metadata['xAxis']) *
                                    len(self.metadata['yAxis'])], np.complex64)
        flgs = np.zeros(self.mds + [len(self.metadata['xAxis']) *
                                    len(self.metadata['yAxis'])], bool)

        # Open the measurement set
        for c, myMS in tqdm(enumerate(mslist), desc='Processing MS'):
            log.info(f"Processing {c+1} of {len(mslist)} - {myMS}")
            iRA, ANTENNA1, ANTENNA2, FEED1, SCAN, DATA, FLAG = self.read_data(
                myMS
            )
            temp, ints, flgs = self.update(
                iRA,
                ANTENNA1,
                ANTENNA2,
                FEED1,
                SCAN,
                DATA,
                FLAG,
                temp,
                ints,
                flgs,
                self.beam_arr
            )
            del ANTENNA1, ANTENNA2, FEED1, SCAN, DATA, FLAG

        # Regrids to same final shape as data
        # This is different to old scheme!
        # -- Gives a flag per pixel (not per image)
        shape = [i for i in flgs.shape[:-1]] + [self.myGridSize, self.myGridSize]
        flgs = flgs.reshape(shape)

        self.temp = temp
        self.ints = ints
        self.bm.flags = flgs

    def normalise(self):
        # Normalise by integration count and write to HDF5 structure
        print('Normalising by count')
        new_shape = list(self.temp.shape[:-1]) + [self.myGridSize, self.myGridSize]
        self.bm.data = (self.temp / self.ints).reshape(new_shape)

    def write_bm(self):
        # Write to disk
        outname = hf.make_file_name(self.bm, kind='hdf5')
        self.bm.write_to_hdf5(f'{self.workdir}/{outname}')


def main(mySBID, mslist, workdir, correct=True):
    """Main script

    Args:
        mySBID (int): SBID of holography
        mslist (list):
        workdir (str): Working directory
        correct (bool): Whether to use the raw data or the column that has been corrected for source structure
    """

    setter = BeamSetter(mySBID, mslist, workdir, correct)

    mslist = setter.get_mslist()

    setter.ms_to_arr(mslist)

    setter.normalise()

    setter.write_bm()

    del setter


if __name__ == "__main__":
    sys.exit(cli())
