"""Simple tools and functions associated with measurement sets
"""
import logging
import os
from pathlib import Path
from typing import Optional

import numpy as np
from casacore.tables import table

from aces.operations.directory import check_create_dir

logger = logging.getLogger(__name__)

MSTABLES: tuple[str, ...] = (
    "ANTENNA",
    "DATA_DESCRIPTION",
    "FEED",
    "FIELD",
    "FLAG_CMD",
    "HISTORY",
    "OBSERVATION",
    "POINTING",
    "POLARIZATION",
    "PROCESSOR",
    "SPECTRAL_WINDOW",
    "STATE",
)
MSTABLEFILES: tuple[str, ...] = (
    "table.dat",
    "table.f0",
    "table.f0i",
    "table.f1",
    "table.info",
    "table.lock",
)


def generate_mock_ms(
    ms_name: str,
    out_dir: Optional[Path] = None,
    ms_tables: tuple[str, ...] = MSTABLES,
    ms_table_files: tuple[str, ...] = MSTABLEFILES,
) -> Path:
    """Generates a mock measurement folder and file structure, intended for
    testing and other trickery. Not yet intended for regular usage. A '.ms'
    suffix will be added if it does not already exist.

    Args:
        ms_name (str): Name of the measurement fodler to create
        out_dir (Optional[Path], optional): Location to create the measurement set folder structure. If None it is created in current working directory. Defaults to None.
        ms_tables (tuple[str, ...], optional): Set of table names that will be created. Defaults to MSTABLES.
        ms_table_files (tuple[str, ...], optional): Names of files in each table to create. Defaults to MSTABLEFILES.

    Returns:
        Path: Path to the measurement set
    """

    if out_dir is None:
        logger.debug(
            f"No output directory specified for {ms_name}. Creating in working directory."
        )
        out_dir = Path(os.getcwd())

    if not ms_name.endswith(".ms"):
        logger.debug("Adding .ms extension to ms_name str instance")
        ms_name = f"{ms_name}.ms"

    ms_dir = check_create_dir(out_dir / ms_name)

    for ms_table in ms_tables:
        logger.debug(f"Creating {ms_table=}")
        ms_table_path = check_create_dir(ms_dir / ms_table)

        for ms_table_file in ms_table_files:
            ms_file_path = ms_table_path / ms_table_file

            with open(ms_file_path, "w") as out_file:
                out_file.write("This is a fake measurement structure. \n")

    return ms_dir


def beam_from_ms(ms: Path) -> int:
    """Returns the ASKAP PAF beam number from an ASKAP measurement set

    Args:
        ms (Path): Path of the measurement set where the beam number will be obtained

    Returns:
        int: The beam number of the ASKAP measurement set
    """
    with table(str(ms), readonly=True, ack=False) as t:
        vis_feed = t.getcol("FEED1", 0, 1)
        beam = vis_feed[0]

    return beam


def min_freq_from_ms(ms: Path) -> float:
    """Returns the lowest frequency observed in an ASKAP measurement set

    This is useful when building up a unique combintaion

    Args:
        ms (Path): Path of the measurement set where the beam number will be obtained

    Returns:
        float: The lowest frequency in Hz across all channels
    """
    with table(f"{str(ms)}/SPECTRAL_WINDOW", readonly=True, ack=False) as t:
        chan_freq = t.getcol("CHAN_FREQ", 0, 1)

    return np.min(chan_freq)


def extract_beam_min_freq(ms: Path) -> tuple[int, int]:
    """Extracts the beam number and lowest frequency channel from an ASKAP measurement set.

    This is intended to help identify and sort measurement sets in a increasing beam and frequency order,
    and will be helpful when merging hdf5 based datasets together

    Args:
        ms (Path): Path to a valid measurement set.

    Returns:
        tuple[int, int]: The beam number and lowest frequency in MHz
    """

    logger.debug(f"Extracting beam and min freq from {ms}")
    assert (
        ms.exists() and ms.is_dir()
    ), f"The measurement set {ms} does not exist or is not a directory. "

    beam = beam_from_ms(ms)
    min_freq = int(min_freq_from_ms(ms) / 1000000.)

    logger.info(f"{ms} extracted {beam=} {min_freq}")

    return beam, min_freq
