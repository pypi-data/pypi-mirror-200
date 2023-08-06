"""Holds bespoke operations related to directories
"""
import logging
import os
from pathlib import Path
from typing import Optional, Union

logger = logging.getLogger(__name__)


def setup_chdir_workdir(workdir: Optional[Union[Path, str]] = None) -> Path:
    """Perform checks on the target working directory. If it does not exist
    it will be created, and execution will be switched to take placce in the
    target

    Args:
        workdir (Optional[Union[Path,str]], optional): Location where work will be carried out. If None the current working directory is used. Defaults to None.

    Returns:
        Path: The resolved working directory
    """

    if workdir is None:
        logger.warn("No directory specified, seeting to current working directory. ")
        workdir = Path(os.getcwd())

    # Incase a string is passed in
    workdir = Path(workdir).absolute()

    if not workdir.exists():
        logger.warn(f"{workdir} does not exist. Creating, ")
        workdir.mkdir(parents=True)

    logger.info(f"Switching to {workdir}")
    os.chdir(workdir)

    return workdir


def check_create_dir(target_dir: Path) -> Path:
    """Check and if necessary create a directory

    Args:
        target_dir (Path): Path to ensure if it is a directory, and create it if it does not exist

    Returns:
        Path: Path to directory
    """
    if target_dir.exists():
        if not target_dir.is_dir():
            raise FileExistsError(f"{target_dir} exists and is not a directory")
    
    else:
        logger.debug(f"Creating {target_dir}")
        target_dir.mkdir(parents=True)

    return target_dir
