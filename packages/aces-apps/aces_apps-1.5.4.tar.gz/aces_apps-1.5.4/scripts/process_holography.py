#!/usr/bin/env python3

"""A prefect2 based pipeline to process holography data taken by ASKAP. It will use components of the aces module,
which will be parallelised in a beam-wise manner where possible. The output data products are FITS files that 
are compatible with the linmos package of yandasoft. 
"""
import argparse
import logging
import os
import shutil
import sys
from glob import glob
from pathlib import Path
from typing import Optional, Union

import pkg_resources
from casacore.tables import table
from prefect import flow, get_run_logger, task

from aces.clink.tasks import task_create_emit_clink_event
from aces.cluster_configs.clusters import get_dask_runner
from aces.cluster_configs.environment import log_environment
from aces.holography import (
    beamset_from_ms,
    clean_holography,
    divmodel,
    dump_point,
    grid_holography,
    merge_holography,
    plot_summary,
)
from aces.operations.actions import find_ms_in_dir
from aces.operations.directory import setup_chdir_workdir
from aces.operations.flows import flow_find_copy_measurement_sets

# Known objects with a model available to correct the holography data with
KNOWN_HOLO_MODELS: tuple[str] = ("virgo",)

logger = logging.getLogger(__name__)


def get_model_resource(holo_src: str) -> str:
    """Look up and return a path to a model file that corresponds to a known bright source that
    holography was performed against.

    Args:
        holo_src (str): Name of the target source, as retreived from the field table of a measurement set

    Raises:
        ValueError: Raised when a model file is expected but not found through package resources.

    Returns:
        str: Path to a model file to use for a known source.
    """

    model = None
    if holo_src == "virgo":
        model = pkg_resources.resource_filename("aces.holography", "VirgoA.mod")

    if model is None:
        raise ValueError(
            f"Unable to resolve {holo_src} to known model. Known sources are {KNOWN_HOLO_MODELS}. "
        )

    return model


def get_holography_src(ms: Union[str, Path]) -> str:
    """Identifies the source that holography was carried out against by examining a measurement set. This intended to
    be used fo any additional processing/corrections (such as the case of virgo)

    Args:
        ms (Union[str,Path]): A measurement set to inspect to identify the target source holography was carried out against

    Returns:
        str: Name of the target source
    """
    # table() does not play well with Paths
    with table(f"{str(ms)}/FIELD") as field:
        fields = list(set(field.getcol("NAME")))

    assert (
        len(fields) == 1
    ), f"Expected a single field to be present, instead found {fields=}"

    return fields[0]


@task(name="Generate beamset")
def task_beamset_from_ms(*args, **kwargs) -> None:
    """A wrapper around the beamset_from_ms main entrypoint that converts MSs to a
    beamset. All args and kwargs are passed into  aces.holography.beamset_from_ms.main.

    """
    logger = get_run_logger()

    logger.info("Converting measurement set to beamset")
    beamset_from_ms.main(*args, **kwargs)


@task(name="Normalising MS based on model")
def task_divmodel(*args, **kwargs) -> None:
    """A wrapper around the divmodel main entry point that corrects holography
    data. All args and kwargs are passed into aces.holography.divmodel.main.

    """
    logger = get_run_logger()

    logger.info("Inserting expected source model")
    divmodel.main(*args, **kwargs)


@task(name="Get pointing data")
def task_dump_point(*args, **kwargs) -> None:
    """A wrapper around the dump_point main entry point that extracts pointing information
    from an MS. All args and kwargs are passed into aces.holography.dump_point.main.

    """
    logger = get_run_logger()

    logger.info("Extracting the point model")
    dump_point.main(*args, **kwargs)


@task(name="Regrid holography")
def task_grid_holography(beam: int, sbid: int, holo_dir: str, ant: int) -> None:
    """A wrapper around the grid_holography main entrypoint, which will grid and interpolate holography data.

    Args:
        beam (int): The beam number that will be processed from the beamset
        sbid (int): The SBID number of the holography data to process
        holo_dir (str): The path of the data that will be processed
        ant (int): Reference antenna used throughout the processing

    """
    logger = get_run_logger()

    logger.info(f"Gridding the holography data for {sbid=} {beam=}")
    grid_holography.main(beam=beam, sbid=sbid, holo_dir=holo_dir, refant=ant)


@task(name="Merge beamsets")
def task_merge_holography(*args, **kwargs) -> None:
    """A wrapper around the merge_holography main entry point that collates holgraphy results together.
    All args and kwargs are passed into aces.holography.merge_holography.main.

    """
    logger = get_run_logger()

    logger.info("Mering the holography data together")
    merge_holography.main(*args, **kwargs)


@task(name="Clean holography")
def task_clean_holography(*args, **kwargs) -> None:
    """A wrapper around the cleaan_holography main entry point that corrects holography
    data from RFI. All args and kwargs are passed into aces.holography.clean_holography.main.

    """
    logger = get_run_logger()

    logger.info("Cleaning the merged holography data")
    clean_holography.main(*args, **kwargs)


@task(name="Plot holography")
def task_plot_summary(*args, **kwargs) -> None:
    """A wrapper around the plot_summary main entry point to create visualisations of the holograhy data.
    data. All args and kwargs are passed into aces.holography.plot_summmary.main.

    """
    logger = get_run_logger()

    logger.info("Creating summary plots")
    plot_summary.main(*args, **kwargs)


@task(name="Get calibrated holography measurement sets")
def get_cal_holo_mslist(sbid: int, workdir: str) -> list[str]:
    """Get list of calibrated MSs from holography dir

    Args:
        sbid (int): Holography SBID
        workdir (str): Working directory

    Returns:
        list[str]: Calibrated holography MSs
    """
    mslist = sorted(
        glob(f"{workdir}/{sbid}/*[0-9].cal.ms"),
        key=lambda x: int(x[-x[::-1].find("_") : x.find(".cal.ms")]),
    )
    return mslist


@task(name="Copying final data products")
def task_copy_final_beams(final_path: Path, sbid: int, dry_run: bool = False) -> None:
    """Copy the constructed beams from the working directory to a final location

    Args:
        final_path (Path): Path to install the constructed beams into. This must exists and be a directory.
        sbid (int): The SBID of the holography observation, which is used when constructing the files to copy.
        dry_run (bool, optional): If True, the copying process is only reported, and no actual copying is performed. Defaults to False.
    """

    logger = get_run_logger()

    beams = glob(f"akpb.iquv.*.SB{sbid}.*.fits")

    assert (
        len(beams) == 2
    ), f"Expected to copy two beam fits, instead found {len(beams)=}"
    assert (
        final_path.exists() and final_path.is_dir()
    ), f"The {final_path=} directory does not exist. It should be created before attempting to run the pipeline. "

    final_path = final_path.absolute()
    logger.info(f"The beams will be installed into {final_path=}")

    if dry_run:
        logger.info(
            "The final beam data products will not be copied into place as the dry-run option has been specified. "
        )

    for beam in beams:
        beam_file = Path(beam).absolute()
        dest_name = final_path / beam_file.name

        if dest_name.exists():
            logger.warn(f"{dest_name} already exists. Skipping the copy. ")
            continue

        logger.info(f"Copying {beam_file} to {final_path}")
        if not dry_run:
            shutil.copy(beam_file, final_path)


# Define flow
@flow()
def flow_holography(
    workdir: str,
    sbid: int,
    grid_ant: Optional[int] = None,
    beam_path: Path = None,
) -> None:
    """The prefect workflow to execute the holography processing and analysis pipeline.

    This flow brings together the main stages that are implemented in other scripts,
    and wraps them up with the prefect logic to allow them to be called.

    The workflow expects that in the current working directory there to be a folder
    whose name is the sbid to be processed, and the measurement sets to be processed
    have been copied there already

    Args:
        workdir (str): Where the data processing will be carried out, including creation of products
        sbid (int): SBID number of the target holography observation to be procesed
        grid_ant (Optional[int], optional): Reference antenna used in observation. If None, attempts are made to dderive it from the data. Defaults to None.
        beam_path (Path, optional): The final location to copy the output beams to. If None, no copying is performed. Defaults to None.
    """
    logger = get_run_logger()

    # Make this a Path. Some of the aces code _really_ expects strings and does its own
    # path wranggling that I do not waant to fix
    workdir_path = Path(workdir)

    # Get MS list from holography. Submit is ommitted to block for result
    # The majority of the holography code expects strings to be passed, and
    # not Path objects
    mslist_holo = [
        str(ms) for ms in find_ms_in_dir(workdir_path / str(sbid), expected_no=36)
    ]

    # Dump pointing data to disk
    task_dump_point.submit(sbid=sbid, mslist=mslist_holo, workdir=workdir)

    holo_src = get_holography_src(mslist_holo[0])
    logger.info(f"The holography target source is {holo_src=}")

    if holo_src in KNOWN_HOLO_MODELS:
        logger.info(
            f"Will be normalising visibility data specific to {holo_src} processing. "
        )

        model = get_model_resource(holo_src)
        future_divmodel = task_divmodel.map(sbid, mslist_holo, model)

    else:
        logger.info(
            f"The extracted {holo_src=} is not in {KNOWN_HOLO_MODELS=}, so no models will be inserted. "
        )
        future_divmodel = None

    # Produce beams in HDF5
    future_beamset = task_beamset_from_ms.submit(
        sbid, mslist_holo, workdir, correct=False, wait_for=future_divmodel
    )

    logger.info(f"{sbid=}")
    logger.info(f"{workdir=}")
    logger.info(f"{grid_ant=}")
    logger.info(f"{mslist_holo=}")

    future_grid = task_grid_holography.map(
        [beam_no for beam_no, _ in enumerate(mslist_holo)],
        sbid,
        workdir,
        grid_ant,
        wait_for=future_beamset,
    )  # type: ignore

    future_merge = task_merge_holography.submit(
        sbid=sbid, holo_dir=workdir, wait_for=future_grid
    )  # type: ignore

    # post-process to FITS
    future_clean = task_clean_holography.submit(
        sbid=sbid,
        holo_dir=workdir,
        remake_stokes=True,
        max_order=5,
        param="BIC",
        snr_limit=3,
        wait_for=future_merge,
    )

    # Plot
    future_summary = task_plot_summary.submit(
        sbid=sbid, holo_dir=workdir, wait_for=future_clean
    )

    if beam_path is not None:
        task_copy_final_beams.submit(beam_path, sbid, wait_for=future_summary)  # type: ignore

    logger.info("Finished. Wrapping up. ")


@flow(name="Holography Main Flow")
def main(
    sbid: int,
    workdir: Optional[Path] = None,
    grid_ant: Optional[int] = None,
    cluster: str = "galaxy_small",
    beam_path: Path = None,
    schedule_block_path: Path = None,
    emit_clink: bool = False,
):
    """The main driver of the holography pipeline procedure. This entrypoint is responsible for

    - creating a dask task runner for use between subflows
    - run the sub-flow to find and copy measurement sets, if requested
    - run the sub-flow to perform the actual holography processing
    - emit a clink even if requested on completion of the two sub-flows

    Args:
        sbid (int): SBID of the observation used to collect the holography data
        workdir (Optional[Path], optional): The directory that the holography data will be processed in. There is an attempt to change to this directory. Defaults to None.
        grid_ant (Optional[int], optional): Antenna number that was the 'reference' antenna during the holography observation. Defaults to None.
        cluster (str, optional): The name of the cluster configuration file to load. Defaults to "galaxy_small".
        beam_path (Path, optional): Path to install the constructed holography beams into. If None, the beams are not copied. Defaults to None.
        schedule_block_path (Path, optional): Path to the space on disk where the Measurement sets are stored (inside a SBID folder). If not None and the SBID
        folder exists with the 36 measurementsets, these are copied over and delete the measurments in the workdir, if they exists. Defaults to None.
        emit_clink (bool, optional): Whether a clink event message will be raised to process manager
    """

    logger = get_run_logger()
    logger.info("The main flow of the ASKAP holography processing pipeline")

    # Directory changed here in case agent deployment is used
    workdir = setup_chdir_workdir(workdir=workdir)

    if beam_path is not None:
        assert (
            beam_path.exists() and beam_path.is_dir()
        ), f"The {beam_path=} directory does not exist. It should be created before attempting to run the pipeline. "

    log_environment()

    # This is a common dask backed runner that will be used for separate flows
    logger.info("Acquiring dask worker")
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
        )(src_path, out_path, expected_no=36)

    # Do the holography magix. Same dask runner used.
    # Sub-flows likst the one above are blocking
    flow_holography.with_options(
        name=f"Processing holography -- {sbid}",
        task_runner=task_runner,
    )(
        str(workdir),
        sbid,
        grid_ant=grid_ant,
        beam_path=beam_path,
    )

    # Sub-flows, including flow_holography, are blocking. No need
    # to wait_for= here
    if emit_clink:
        task_create_emit_clink_event.submit(
            "clink-holo", sbid, workdir, "holography", state="completed"
        )  # type: ignore


def cli():
    descStr = """
Process holography data from a measurement set, pack into a beamset HDF5
and Stokes FITS cube.

In your working directory have a directory containing the holography
measurement sets (and optionally the 1934 bandpass MSs) under the name
of its SBID.
    """
    # Parse the command line options
    parser = argparse.ArgumentParser(
        description=descStr, formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("workdir", type=Path, help="Working directory.")

    parser.add_argument("sbid", type=int, help="SBID of holography.")

    parser.add_argument(
        "-a",
        "--ant",
        type=int,
        default=None,
        help="Antenna to use for regrid reference - specify to override [ref. ant. + 1].",
    )

    parser.add_argument(
        "-v", "--verbosity", action="count", help="Increase output verbosity", default=0
    )
    parser.add_argument(
        "-c",
        "--cluster",
        type=str,
        default="galaxy_small",
        help="Name of the cluster specification file to use for interacting with a compute cluster. Inputs may be a resolved path to a yaml file, or a name of a known cluster file packaged with the aces repository (without the trailing .yaml extension)",
    )

    parser.add_argument(
        "-b",
        "--beam-path",
        type=Path,
        default=None,
        help="Path that the final beam data products will be copied to. If None, beams are not copied. ",
    )

    parser.add_argument(
        "-s",
        "--schedule-block-path",
        type=Path,
        default=None,
        help="The directory to the location of SBID folders with raw measurement sets. If this is not None and is valid, the data will be copied fresh, clobbering the existing SBID folder in the desired work directory, should it exist. ",
    )

    parser.add_argument(
        "-e",
        "--emit-clink",
        default=False,
        action="store_true",
        help="Issue a CLINK event to inform process manager of completion. ",
    )

    args = parser.parse_args()

    main(
        args.sbid,
        workdir=args.workdir,
        grid_ant=args.ant,
        cluster=args.cluster,
        beam_path=args.beam_path,
        schedule_block_path=args.schedule_block_path,
        emit_clink=args.emit_clink,
    )


if __name__ == "__main__":
    sys.exit(cli())
