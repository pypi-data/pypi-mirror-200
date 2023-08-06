"""This contains some bespoke operations related to the general orchastration 
of a workflow, including:

- copying measurement sets
"""

import logging
import shutil
from glob import glob
from pathlib import Path
from typing import Optional

from aces.exceptions import MissingMSError

logger = logging.getLogger(__name__)

# TODO: Should these find tasks be consolidated into one and 
#       instead as an option have the glob string?

def find_sbid_ms_in_dir(
    sbid: int, target_dir: Path, expected_no: Optional[int] = None
) -> list[Path]:
    """Searches for measurement sets of a particular SBID in a target directory

    Args:
        sbid (int): The SBID of interest
        target_dir (Path): The directory expected to contain the MS
        expected_no (Optional[int], optional): Number of expected MSs to find. Defaults to None.

    Raises:
        MissingMSError: Raised when expected_no is not None and that many MSs are not found

    Returns:
        list[Path]: Location to the MSs that were found in the target_dir
    """
    mslist = sorted(
        glob(f"{str(target_dir)}/*{sbid}*[0-9].ms"),
        key=lambda x: int(x[-x[::-1].find("_") : x.find(".ms")]),
    )

    # Useful if calling code can only deal with a expected number, which
    # is currently the case for the holography and SEFD code -- one MS for
    # each beam
    if expected_no is not None and len(mslist) != expected_no:
        raise MissingMSError(
            f"Expected {expected_no} MSs, found {len(mslist)} for {target_dir=} and {sbid=}"
        )

    return [Path(ms) for ms in mslist]


def find_ms_in_dir(
    target_dir: Path, expected_no: Optional[int] = None
) -> list[Path]:
    """Searches for measurement sets of a particular SBID in a target directory

    Args:
        target_dir (Path): The directory expected to contain the MS
        expected_no (Optional[int], optional): Number of expected MSs to find. Defaults to None.

    Raises:
        MissingMSError: Raised when expected_no is not None and that many MSs are not found

    Returns:
        list[Path]: Location to the MSs that were found in the target_dir
    """
    mslist = sorted(
        glob(f"{str(target_dir)}/*[0-9].ms"),
        key=lambda x: int(x[-x[::-1].find("_") : x.find(".ms")]),
    )

    # Useful if calling code can only deal with a expected number, which
    # is currently the case for the holography and SEFD code -- one MS for
    # each beam
    if expected_no is not None and len(mslist) != expected_no:
        raise MissingMSError(
            f"Expected {expected_no} MSs, found {len(mslist)} for {target_dir=}."
        )

    return [Path(ms) for ms in mslist]


def copy_measurement_set(
    target_ms: Path, output_dir: Path, overwrite: bool = False
) -> Path:
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

    # This function can be called in parallel. It is therefore unsafe to trust it
    # to create the output directory should it not exist
    assert (
        output_dir.exists() and output_dir.is_dir()
    ), f"Output location {output_dir} is not a directory or does not exist. "

    target_ms = Path(target_ms)

    assert (
        target_ms.exists() and target_ms.is_dir()
    ), f"Target measurment set {target_ms=} is not available. "

    copy_path = output_dir / target_ms.name
    logger.info(f"Copying {target_ms=} to {copy_path=}")

    if copy_path.exists():
        if not overwrite:
            logger.warn(f"File {copy_path} exists. Not copying. ")

            return copy_path
        
        logger.warn(f"Output MS {str(copy_path)} exista and {overwrite=}. Removing.")
        shutil.rmtree(copy_path)
            
    shutil.copytree(target_ms, copy_path)
    logger.info(f"Copying {target_ms=} finished")

    return copy_path
