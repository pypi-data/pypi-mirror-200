#!/usr/bin/env python3

import logging
import os
from argparse import ArgumentParser
from pathlib import Path
from typing import Collection

from prefect import flow, get_run_logger, task, unmapped

from aces.clink.tasks import task_create_emit_clink_event
from aces.cluster_configs.clusters import get_dask_runner
from aces.cluster_configs.environment import log_environment
from aces.exceptions import MissingBeamError
from aces.operations.directory import setup_chdir_workdir
from aces.operations.flows import flow_find_copy_measurement_sets
from aces.sefd.stages import (
    create_parset,
    find_ms,
    merge_hdf5_sefd,
    processing_sefd,
    summary_plots_sefd,
    scan_ms_configs,
    move_sefd_files_into
)

logger = logging.getLogger(__name__)

task_summary_sefd = task(summary_plots_sefd)
task_merge_sefd = task(merge_hdf5_sefd)
task_processing_sefd = task(processing_sefd)
task_scan_ms_configs = task(scan_ms_configs)
task_create_parset = task(create_parset)
task_move_sefd_files_info = task(move_sefd_files_into)

        
@flow(log_prints=True)  # type: ignore
def process_sefd(sbid: int, sefd_path: Path = None) -> None:
    """Main prefect flow to perform the SEFD processing and analysis.

    Args:
        sbid (int): SBID of the observation data. A folder with these measurement sets should be in the current directory.
        sefd_path (Path, optional): If not None, the SEFD data products will be copied to this directory. An attempt will be made to created the directory if it does not exist. Defaults to None. 
        
    Raises:
        MissingBeamError: Raised when on of the 36 ASKAP beams is missing
    """
    workdir = Path(os.getcwd())
    logger.info(f"Processing SEFD {sbid=}")
    logger.info(f"Working directory: {workdir=}")

    sefd_ms = find_ms(sbid)

    # Some observing modes have high spectral resolution modes, and for efficiency
    # beams are split into multiple measurement sets covering different spectral windows.
    if len(sefd_ms) % 36 != 0:
        raise MissingBeamError(
            f"Located {len(sefd_ms)} measurement sets, expected a multiple of 36"
        )

    # mypy type error without the xplicit casting below
    sefd_ms_join = "\n".join([str(p) for p in sefd_ms])
    logger.info(f"Located {len(sefd_ms)} measurement sets: {sefd_ms_join}")

    parset_future = task_create_parset.submit(sbid, workdir)

    sorted_beam_freqs = task_scan_ms_configs.submit(sefd_ms, wait_for=[parset_future])  # type: ignore

    sefd_hdf5_set = task_processing_sefd.map(
        sbid,
        sefd_ms,
        unmapped(sorted_beam_freqs),
        wait_for=[
            parset_future,
        ],
    )  # type: ignore

    merge_hdf5 = task_merge_sefd.submit(sbid, sefd_hdf5_set)  # type: ignore

    plot_name = task_summary_sefd.submit(
        sbid,
        merge_hdf5,
    )  # type: ignore

    if sefd_path:
        task_move_sefd_files_info.submit(sbid, sefd_path, wait_for=[plot_name, ])


@flow
def setup_sefd_flow(
    sbid: int,
    cluster: str,
    workdir: Path = None,
    schedule_block_path: Path = None,
    emit_clink: bool = False,
    sefd_path: Path = None
) -> None:
    """Perform basic checks before starting the main SEFD processing workflow

    Args:
        sbid (int): SBID of observation to process
        cluster (str): Known cluster configuration file for the DaskTaskRunner packaged with aces-apps
        workdir (Path, optional): Where to carry out the computation. If None, the current working directory will be used. Defaults to None.
        schedule_block_path (Path, optional): Path to the space on disk where the Measurement sets are stored (inside a SBID folder). If not None and the SBID folder exists with the 36 measurementsets, these are copied over and delete the measurments in the workdir, if they exists. Defaults to None.
        emit_clink (bool, optional): If True, a clink event will be sent to advertise the processing completeion. Defaults to False.
        sefd_path (Path, optional): If not None, the SEFD data products will be copied to this directory. An attempt will be made to created the directory if it does not exist. Defaults to None. 
    """
    logger = get_run_logger()

    # Directory changed here in case agent deployment is used
    workdir = setup_chdir_workdir(workdir=workdir)

    logger.info(f"Setting up environment for SEFD processing")
    logger.info(f"SEFD SBID to process: {sbid}")
    logger.info(f"Using cluster environment: {cluster=}")
    logger.info(f"Working directory: {workdir=}")

    log_environment()

    task_runner = get_dask_runner(
        cluster, extra_cluster_kwargs=dict(local_directory=os.getcwd())
    )

    # Copy the measureement sets into place if requested
    if schedule_block_path is not None:
        src_path = schedule_block_path / str(sbid)
        out_path = Path(workdir) / str(sbid)
        logger.debug(f"Searching {src_path} to copy MS to {out_path}")

        flow_find_copy_measurement_sets.with_options(
            name=f"Copy measurement sets -- {sbid}", task_runner=task_runner
        )(src_path, out_path)

    process_sefd.with_options(
        name=f"SEFD Processing pipeline -- {sbid}", task_runner=task_runner
    )(sbid, sefd_path)

    if emit_clink:
        task_create_emit_clink_event.submit(
            "clink-sefd", sbid, workdir, "sefd", state="completed"
        )  # type: ignore


def cli() -> None:
    """CLI entry point for the SEFD processing pipeline"""
    parser = ArgumentParser(description="Launch SEFD processing")

    parser.add_argument("sbid", type=int, help="SBID")
    parser.add_argument(
        "-c",
        "--cluster",
        type=str,
        default="galaxy_small",
        help="Name of the cluster specification file to use for interacting with a compute cluster. Inputs may be a resolved path to a yaml file, or a name of a known cluster file packaged with the aces repository (without the trailing .yaml extension)",
    )
    parser.add_argument(
        "-d", "--workdir", type=Path, default=".", help="working directory"
    )
    parser.add_argument("-v", "--verbose", action="store_true")

    parser.add_argument(
        "-e",
        "--emit-clink",
        default=False,
        action="store_true",
        help="Issue a CLINK event to inform process manager of completion. ",
    )

    parser.add_argument(
        "-s",
        "--schedule-block-path",
        type=Path,
        default=None,
        help="The directory to the location of SBID folders with raw measurement sets. If this is not None and is valid, the data will be copied fresh, clobbering the existing SBID folder in the desired work directory, should it exist. ",
    )
    parser.add_argument(
        "-f",
        "--sefd-path",
        type=Path,
        default=None,
        help="The directory that the SEFD data products will be copied into, including the SBID folder. Defaults to None. "
    )

    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    setup_sefd_flow.with_options(name=f"SEFD -- {args.sbid}")(
        args.sbid,
        args.cluster,
        args.workdir,
        schedule_block_path=args.schedule_block_path,
        emit_clink=args.emit_clink,
        sefd_path=args.sefd_path
    )


if __name__ == "__main__":
    cli()
