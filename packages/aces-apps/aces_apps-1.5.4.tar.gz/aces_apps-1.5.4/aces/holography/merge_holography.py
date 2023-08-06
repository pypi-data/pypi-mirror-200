#!/usr/bin/env python3
""" Merge holography data """
import sys
import numpy as np
import copy
from aces.beamset.mapset import MapSet
import aces.beamset.beamfactory as bf
from aces.holography import holo_filenames as hf
import logging 

log = logging.getLogger(__name__)

# Catch annoying warnings
np.seterr(divide="ignore", invalid="ignore")


def main(sbid,
         holo_dir='.'):
    """Main script

    :param sbid: SBID
    :type sbid: int
    :param holo_dir: directory holding holograophy data
    :type holo_dir: str
    """

    # Clean up dir
    if holo_dir[-1] == '/':
        holo_dir = holo_dir[:-1]

    # Note this. Could need improved determination in future.
    nbeams = 36
    beam_data = []
    beam_meta = []
    for b in range(nbeams):
        # in_name = f'{holo_dir}/{sbid:d}_Holo_grid_{b:02d}.hdf5'
        kind = f'grid.beam{b:02d}.hdf5'
        try:
            in_name = hf.find_holo_file(holo_dir, pol='xxyy', sbid=sbid, kind=kind)
            ob = bf.load_beamset_class(in_name)
            # print(b, ob.data.shape, ob.flags.shape)
            beam_data.append(ob)
        except FileNotFoundError:
            log.warning(f"HDF5 file for beam {b} not found. Skipping. ")

    assert len(beam_data) > 0, 'No HDF5 beam files have been located. '

    # print(" A ", beam_data[0].flags.ndim, beam_data[0].flags.shape)
    md = copy.deepcopy(beam_data[0].metadata)
    sh1 = list(beam_data[0].data.shape)
    shn = tuple(sh1[:2] + [nbeams] + sh1[3:])

    merged_data = np.zeros(shn, dtype=complex)
    merged_flags = np.zeros(shn[:-2], dtype=bool)
    # print("merged flags shape ", merged_flags.shape, shn[:-2])
    truncate = beam_data[0].flags.ndim == 7
    for b, obj in enumerate(beam_data):
        merged_data[:, :, b:b + 1] = obj.data
        if truncate:
            merged_flags[:, :, b:b + 1] = obj.flags.all(axis=(-2, -1))
        else:
            # print(merged_flags[:, :, b:b + 1].shape)
            # print(obj.flags.shape)
            merged_flags[:, :, b:b + 1] = obj.flags
        beam_meta.append(obj.metadata['beams'][0])

    md['beams'] = np.array(beam_meta)
    merged_obj = MapSet(metadata=md,
                        data=merged_data,
                        flags=merged_flags,
                        filename=None
                        )
    merged_obj.add_to_history('Resampled beam files merged')

    out_name = f'{holo_dir}/{hf.make_file_name(merged_obj, kind="grid.hdf5")}'
    # out_name = f'{holo_dir}/{sbid:d}_Holo_grid.hdf5'
    merged_obj.write_to_hdf5(out_name)

    log.info("All finished")


def cli():
    import argparse
    """
    Command line interface
    """

    # Help string to be shown using the -h option
    descStr = """
    Clean holography data
    """

    epilog_text = """

    """

    # Parse the command line options
    parser = argparse.ArgumentParser(description=descStr,
                                     epilog=epilog_text,
                                     formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument(
        'sbid',
        metavar='sbid',
        type=int,
        help='SBID of processed holography (stored in HDF5) [no default].')

    parser.add_argument(
        '-d',
        dest='holo_dir',
        type=str,
        default='.',
        help='Directory containing holography data [./].')

    parser.add_argument(
        "-v",
        "--verbosity",
        action="count",
        help="Increase output verbosity",
        default=0
    )

    args = parser.parse_args()
    if args.verbosity == 1:
        log.basicConfig(
            level=log.INFO,
            format="%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    elif args.verbosity >= 2:
        log.basicConfig(
            level=log.DEBUG,
            format="%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    main(sbid=args.sbid,
         holo_dir=args.holo_dir
         )


if __name__ == "__main__":
    sys.exit(cli())
