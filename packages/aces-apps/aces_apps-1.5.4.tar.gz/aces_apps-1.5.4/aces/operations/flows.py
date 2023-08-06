"""This contains prefect based workflows that may be called and used in other larger workflows. Specifically
these particular flows are related to the tasks involing file interaction and similar oepraitons
"""

import logging
from typing import Collection, Optional
from pathlib import Path

from prefect import flow, get_run_logger

from aces.operations.tasks import task_copy_ms_to_dir
from aces.operations.actions import find_ms_in_dir

logger = logging.getLogger(__name__)


@flow(name="Measurement set copied")
def flow_find_copy_measurement_sets(
    src_dir: Path,
    output_dir: Path,
    expected_no: Optional[int] = None,
    overwrite: bool = False,
) -> Collection[Path]:
    """Given a target directory to search and a SBID, search for MSs to copy and copy.

    Since this uses a prefect Task and its map method, there is no non-flow alternative. 

    Args:
        src_dir (Path): Directory thought to contain the SBID MSs
        output_dir (Path): Where to copy the MSs to. If directory does not exist an error is raised. 
        expected_no (Optional[int], optional): Number of MSs that should be found. Defaults to None.
        overwrite (bool, optional): If True and a MS that will be copied is found to exist, it is overwriten. Defaults to False.

    Returns:
        Collection[Path]: Paths of MSs that are copied
    """

    logger = get_run_logger()

    logger.info("Copying measurement sets")
    logger.info(f"Searching for measurement sets in: {src_dir=}")

    ms_paths = find_ms_in_dir(src_dir, expected_no=expected_no)

    logger.info(f"Found {len(ms_paths)} measurement sets in {src_dir=}")

    if not (output_dir.exists() and output_dir.is_dir()):
        logger.warning(f" Attempting to create {output_dir=}. ")
        output_dir.mkdir(parents=True)

    output_paths = task_copy_ms_to_dir.map(
        ms_paths, output_dir, overwrite=overwrite
    ) # type: ignore

    logger.info(f"Finished copying {len(ms_paths)} MSs")

    return output_paths
