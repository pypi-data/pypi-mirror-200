"""This contains prefect wrapped tasks that call existing functions
defined under the aces.operations module
"""

import logging
from pathlib import Path

from prefect import get_run_logger, task

from aces.operations.actions import copy_measurement_set

logger = logging.getLogger(__name__)


@task(name="Measurement set copy")
def task_copy_ms_to_dir(target_ms: Path, output_dir: Path, overwrite: bool=False) -> Path:
    """Copy a measurement set from a source location to the working directory where
    the holography pipeline is being executed. Although measurement sets are strictly
    directories, this function could be expanded for measurement specific tasks.

    Args:
        target_ms (Path): Full path to the measurement set to be copied
        output_dir (Path): Location to save the measurement set
        overwrite (bool, optional): Overwrite the measurement set if it exists. Defaults to False. 

    Returns:
        Path: The name of the copied measurement set in the target directory
    """
    logger = get_run_logger()

    logger.info(f"Copying {target_ms=} to {output_dir}")
    output_path = copy_measurement_set(target_ms, output_dir, overwrite=overwrite)

    return output_path
