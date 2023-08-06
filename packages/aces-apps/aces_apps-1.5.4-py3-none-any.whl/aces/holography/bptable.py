#!/usr/bin/env python3
import sys
import os
import argparse
import numpy as np
from casacore.tables import *
import shutil
from aces.askapdata.schedblock import SchedulingBlock
import string


class BandpassTable:

    def getcol(self, inTable, colName, antNum, beamNum, nPol=4):
        """Get column of BP table

        :param inTable: Name of table on disk
        :type inTable: str
        :param colName: Name of column 'BANDPASS' or 'BPLEAKAGE'
        :type colName: str
        :param antNum: Antenna index
        :type antNum: int
        :param beamNum: Beam index
        :type beamNum: int
        :param nPol: Number of polarisations, defaults to 4
        :type nPol: int, optional
        """
        with table(inTable, readonly=True, ack=False) as t:
            self.bp = t.getcol(colName, startrow=0, nrow=-1, rowincr=1)
            # Read the flag table
            colName = colName + '_VALID'
            self.bpf = t.getcol(colName, startrow=0, nrow=-1, rowincr=1)

            # Get some properties handy:
            time = t.getcol('TIME', startrow=0, nrow=-1, rowincr=1)
            self.time = (time - time[0])*24.0*60.0  # In minutes from start

            self.nTime = self.bp.shape[0]
            self.nbeams = self.bp.shape[1]
            self.nante = self.bp.shape[2]
            self.nchan = self.bp.shape[3]//nPol
            self.chan_arr = np.linspace(0, self.nchan-1, self.nchan)
            self.ant_arr = np.linspace(0, self.nante-1, self.nante)

            # x-pol:
            self.fx = np.array(
                self.bpf[0, beamNum, antNum, 0:nPol*self.nchan:2].astype(
                    dtype="float32",
                    casting='same_kind'
                )
            )
            self.xr = np.multiply(
                self.bp[0, beamNum, antNum, 0:nPol*self.nchan:2].real, self.fx
            )
            self.xi = np.multiply(
                self.bp[0, beamNum, antNum, 0:nPol*self.nchan:2].imag, self.fx
            )
            self.xa = abs(
                np.array(
                    self.xr + 1j*self.xi
                )
            )
            self.xp = np.angle(
                np.array(
                    self.xr + 1j*self.xi
                )
            )*180.0/np.pi

            # Now for y-pol:'
            self.fy = np.array(
                self.bpf[0, beamNum, antNum, 1:nPol*self.nchan:2].astype(
                    dtype="float32", casting='same_kind'
                )
            )
            self.yr = np.multiply(
                self.bp[0, beamNum, antNum, 1:nPol*self.nchan:2].real, self.fy
            )
            self.yi = np.multiply(
                self.bp[0, beamNum, antNum, 1:nPol*self.nchan:2].imag, self.fy
            )
            self.ya = abs(
                np.array(
                    self.yr + 1j*self.yi
                )
            )
            self.yp = np.angle(
                np.array(
                    self.yr + 1j*self.yi
                )
            )*180.0/np.pi

    def putcol(self, outTable, colName, antNum, beamNum, nPol=4):
        """Write column to BPTable

        :param outTable: Output table
        :type outTable: str
        :param colName: Column to overwrite - 'BANDPASS' or 'BPLEAKAGE'
        :type colName: str
        :param antNum: Antenna index
        :type antNum: int
        :param beamNum: Beam index
        :type beamNum: int
        :param nPol: Number of polarisations, defaults to 4
        :type nPol: int, optional
        """
        with table(outTable, readonly=False, ack=False) as t:
            bp = t.getcol(colName, startrow=0, nrow=-1, rowincr=1)
            # Read the flag table
            colNameF = colName + '_VALID'
            bpf = t.getcol(colNameF, startrow=0, nrow=-1, rowincr=1)

            new_bp = np.copy(bp)
            # x-pol:
            x = self.xr + 1j*self.xi
            new_bp[0, beamNum, antNum, 0:nPol*self.nchan:2] = x

            # Now for y-pol:
            y = self.yr + 1j*self.yi
            new_bp[0, beamNum, antNum, 1:nPol*self.nchan:2] = y

            t.putcol(colName, new_bp, startrow=0, nrow=-1, rowincr=1)


def copy_and_overwrite(from_path, to_path):
    """Copy and overwrite directory

    Args:
        from_path (str): Source path
        to_path (str): Destination path
    """
    if os.path.exists(to_path):
        shutil.rmtree(to_path)
    shutil.copytree(from_path, to_path)


def main(bs_tab, hl_tab, beam, mySBID):
    """Main script

    :param bs_tab: Boresight bandpass table
    :type bs_tab: str
    :param hl_tab: Holography bandpass table
    :type hl_tab: str
    :param beam: Beam index
    :type beam: int
    :param mySBID: SBID of holography observation
    :type mySBID: int
    :return: Combined bandpass table
    :rtype: str
    """
    sb = SchedulingBlock(mySBID)
    myRA = int(''.join(filter(lambda char: char in string.digits,
                              sb.get_parameters()['holography.ref_antenna'])))
    iRA = myRA - 1

    ms_comb = bs_tab.replace('boresight', 'combined')
    copy_and_overwrite(hl_tab, ms_comb)

    bpTable = BandpassTable()

    for col in ['BANDPASS', 'BPLEAKAGE']:
        bpTable.getcol(bs_tab, col, iRA, beam, nPol=4)
        bpTable.putcol(ms_comb, col, iRA, beam, nPol=4)

    return ms_comb


def cli():
    descStr = """
Combine bandpass tables for holography processing.
    """
    # Parse the command line options
    parser = argparse.ArgumentParser(
        description=descStr,
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        'bs_tab',
        metavar='bs_tab',
        type=str,
        help='Boresight bandpass table.'
    )

    parser.add_argument(
        'hl_tab',
        metavar='hl_tab',
        type=str,
        help='Holography bandpass table.'
    )

    parser.add_argument(
        'beam',
        metavar='beam',
        type=int,
        help='Beam of bandpass table.'
    )

    parser.add_argument(
        'sbid',
        metavar='sbid',
        type=int,
        help='SBID of holography observation.'
    )

    args = parser.parse_args()

    main(
        args.bs_tab,
        args.hl_tab,
        args.beam,
        args.sbid,
    )


if __name__ == "__main__":
    sys.exit(cli())
