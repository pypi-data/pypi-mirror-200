"""Base tasks used to construct the prefect based SEFD pipeline
"""
import glob
import logging
import os
import shutil
from pathlib import Path
from typing import Any, Collection

import numpy as np
import pkg_resources
from askap.parset.parset import ParameterSet
from casacore.tables import table

from aces.askapdata.schedblock import SchedulingBlock
from aces.beamset import beamfactory
from aces.beamset.sefdset import SEFDSet
from aces.display import ant_beam_pol_summary
from aces.obsplan.config import get_footprint
from aces.sefd.plotting import find_mode, make_sefd_cmap
from aces.sefd.sefd__cc import SEFD
from aces.operations.ms import extract_beam_min_freq

logger = logging.getLogger(__name__)


ARCHIVE = "/astro/askaprt/askapops/askap-scheduling-blocks/"


def scan_ms_configs(ms_set: Collection[Path]) -> list[tuple[int, int]]:
    """Obtain a sorted listed of (beam, minimum frequency) tuples, used for helping
    to sort measurement sets before merging their corresponding hdf5 files together
    while ensuring unique indicies

    Args:
        ms_set (Collection[Path]): Measurement sets that will be sorted

    Returns:
        list[tuple[int, int]]: Increasing beam and frequency tuples across all measurement sets
    """

    logger.info(f"Examinging {len(ms_set)} measurement sets")

    configs = sorted([extract_beam_min_freq(ms) for ms in ms_set])

    lines = "\n".join([f"{config}" for config in configs])
    logger.debug(f"Sorted configs: {lines}")
    
    configs_set = set(configs)
    assert len(configs_set) == len(ms_set), f"(Beam, Min.Freq) lookup produces repeating key. {len(ms_set)=} MSs with {len(configs_set)=} unique keys. "
    
    return configs


def find_ms(sbid: int) -> Collection[Path]:
    """Searches for measurement sets within a folder in the current directory. The folder
    name is the provided sbid.

    Args:
        sbid (int): The SBID of the observation, and the name of a folder containing the measurement sets

    Raises:
        FileNotFoundError: Raised when the SBID folder containing the measurement sets is not found

    Returns:
        Collection[Path]: Paths to each of the located measurement sets
    """
    search_dir: Path = Path(os.getcwd()) / Path(f"{sbid}")

    logger.info(f"Searching {search_dir=}")
    if not search_dir.exists():
        raise FileNotFoundError(f"Path {search_dir=} does not exist.")

    glob_ms = glob.glob(f"{search_dir}/*ms")

    logger.info(f"Located {len(glob_ms)} measurement sets")

    return tuple([Path(ms) for ms in glob_ms])


def summary_plots_sefd(
    sbid: int,
    merged_hdf5: Path,
    sefd_scale_range: tuple[float, float] = (1465.0, 2931.0),
) -> Path:
    """Create summary plots of the merged SEFD hdf5 file

    Args:
        sbid (int): The SBID of the observation the SEFD data are derived from
        merged_hdf5 (Path): Location of the merged HDF5 file
        sefd_scale_range (tuple[float, float], optional): SEFD limits used for plotting, and correspond to Tsys/eff of 60K and 120K. Defaults to (1465.0, 2931.0).

    Returns:
        Path: Path to output plot created
    """

    # These values correspond to Tsys/eff = 60K and 120K
    logger.info(f"Using SEFD scale of: {sefd_scale_range=}")
    cmap, norm = make_sefd_cmap(*sefd_scale_range)

    kwargs = dict(
        label="SEFD (Jy)", cmap=cmap, cnorm=norm, minmax=[0.0, 5000.0], annotations=[]
    )
    params = dict(lower=500.0, upper=2000.0)

    logger.info(f"Loading {merged_hdf5=}")
    sefd_beamset = beamfactory.load_beamset_class(merged_hdf5)

    if "difference" in sefd_beamset.metadata:
        kwargs["annotations"].append(
            f"Difference in {sefd_beamset.metadata['difference']}"
        )

    logger.info(f"Creating the antenna beam summary plot...")
    fig = ant_beam_pol_summary.make_summary_plot(
        sefd_beamset, find_mode, params, **kwargs
    )

    plot_file = Path(f"SEFD_{sbid}_summary.png")
    logger.info(f"... saving to {plot_file}")
    fig.savefig(plot_file, dpi=300)

    return plot_file


def verify_create_hdf5_hdr_sefd(
    sefd_hdf5: Collection[Path],
) -> tuple[dict[Any, Any], list[int], list[int]]:
    """Inspects the header of many SEFD hdf5 files, each corresponding to a separate ASKAP
    beam, to ensure compatible frequency ranges, correct number of beams, and antennas. If
    these checks pass, a new header is formed with correct properties for the merged HDF5
    file

    Args:
        sefd_hdf5 (Collection[Path]): A collection of Paths, each pointing to a SEFD beam HDF5 file

    Raises:
        ValueError: Raised when the spectrum is discontigous / split.

    Returns:
        tuple[dict[Any, Any], list[int], list[int]]: The new header, list of unique antenna and beams
    """

    logger.info(f"Loading the metadata for {len(sefd_hdf5)} HDF5 files")
    sefd_metadata: list[dict[Any, Any]] = [
        beamfactory.load_beamset_class(str(hdf5)).metadata for hdf5 in sorted(sefd_hdf5)
    ]

    beams = sorted(list(set([metadata["beams"][0] for metadata in sefd_metadata])))
    logger.info(f"Unique beams loaded: {beams=}")

    antennas = sorted(
        list(set([ant for metadata in sefd_metadata for ant in metadata["antennas"]]))
    )
    logger.info(f"Unique antennas loaded: {antennas=}")

    freq_ranges = np.array([metadata["freq_range"] for metadata in sefd_metadata])
    logger.info(f"Loaded frequency information:")
    logger.info(f"    - frequency range shape: {freq_ranges.shape}")
    logger.info(f"    - example range (1st): {freq_ranges[0]}")
    logger.info(f"    - example range (2nd): {freq_ranges[1]}")
    logger.info(f"    - example range (3rd): {freq_ranges[2]}")

    start_freq = np.sort(np.unique(freq_ranges[:, 0]))
    end_freq = np.sort(np.unique(freq_ranges[:, 1]))
    no_freqs = np.sort(np.unique(freq_ranges[:, 2]))

    delta_chan = (end_freq[0] - start_freq[0]) / (no_freqs[0] - 1)
    
    # I am not convinced that the brackets in the denominator is correctly
    # ordered, and the minus 1 should be subtracted from the number of channels
    # potentially for each sub-band. However, the 1e-9 check below fails.
    # This might be a magic numbed that needs to be reconsidered?
    delta_band = (end_freq[-1] - start_freq[0]) / (
        start_freq.shape[0] * no_freqs[0] - 1
    )

    if not (no_freqs.shape[0] == 1 and abs(delta_band - delta_chan) < 1e-9):
        raise ValueError(
            "Likely discontigous spectrum among the SEFD HDF5 found when merging"
        )

    new_freq_range = (start_freq[0], end_freq[-1], start_freq.shape[0] * no_freqs[0])

    new_metadata_hdr = sefd_metadata[0]
    new_metadata_hdr["antennas"] = antennas
    new_metadata_hdr["beams"] = beams
    new_metadata_hdr["freq_range"] = new_freq_range

    return new_metadata_hdr, antennas, beams


def merge_hdf5_sefd(sbid: int, sefd_hdf5s: Collection[Path]) -> Path:
    """Merge many SEFD beam HDF5 files into a single HDF5 file

    Args:
        sbid (int): The SBID of the observationt hat took the data being processed
        sefd_hdf5s (Collection[Path]): Collection of paths that point to t he SEFD HDF5 file of indibidual beams

    Returns:
        Path: Path to the merged SEFD HDF5 file
    """
    out_filename = Path(f"SEFD_{sbid}.hdf5")

    new_metadata_hdr, antennas, beams = verify_create_hdf5_hdr_sefd(sefd_hdf5s)
    merged_sefd = SEFDSet(metadata=new_metadata_hdr)

    logger.info(f"Merged SEFD data shape: {merged_sefd.data.shape}")

    freqs = merged_sefd.frequencies
    _, _, _, no_pol, _ = merged_sefd.containerShape

    for sefd_hdf5 in sefd_hdf5s:
        logger.info(f"Merging {sefd_hdf5}")

        sefd_container = beamfactory.load_beamset_class(str(sefd_hdf5))
        this_ants = sefd_container.metadata["antennas"]
        this_beam = sefd_container.metadata["beams"][0]
        this_freq_range = sefd_container.metadata["freq_range"]

        idx_beam = np.where(beams == this_beam)[0][0]
        idx_start_chan = np.where(np.abs(freqs - this_freq_range[0]) < 1e-4)[0][0]
        idx_end_chan = idx_start_chan + int(this_freq_range[2])

        for ant in this_ants:
            idx_ant = antennas.index(ant)
            idx_this_ant = list(this_ants).index(ant)

            this_masked = np.ma.masked_invalid(
                sefd_container.data[:, idx_this_ant : idx_this_ant + 1, 0, :, :]
            )
            logger.info(f"Data shape of subject antenna: {this_masked.shape}")

            merged_sefd.data[
                :,
                idx_ant,
                idx_beam : idx_beam + 1,
                0:no_pol,
                idx_start_chan:idx_end_chan,
                0,
            ] = this_masked.data[..., 0]

            merged_sefd.flags[
                :,
                idx_ant,
                idx_beam : idx_beam + 1,
                0:no_pol,
                idx_start_chan:idx_end_chan,
            ] = this_masked.mask[..., 0]

    merged_sefd.add_to_history("Creating merged file")
    logging.info(f"Writing to {out_filename}")
    merged_sefd.write_to_hdf5(str(out_filename))

    return out_filename


def processing_sefd(
    sbid: int,
    ms: Path,
    beam_min_freq_order: list[tuple[int, int]],
    default_parset_path: Path = Path("SEFD_defaults.parset"),
) -> Path:
    """Create a SEFD HDF5 file from a measurement set

    Args:
        sbid (int): SBID of the observation used to obtain data
        ms (Path): Path to a measurement set containing data from a single ASKAP beam
        beam_min_freq_order (list[tuple[min, float]]): Lookup used to derive the correct order of output hdf5 files, with increasing numbers corresponding to larger beams and higher frequencies.
        default_parset_path (Path, optional): Path to a parset with default processing options. Defaults to Path("SEFD_defaults.parset").

    Raises:
        FileNotFoundError: Raised if the default SEFD processing parset can not be located
        FileNotFoundError: Raised id the SEFD paraset for this SBID does not exist

    Returns:
        Path: Output path of the SEFD HDF5 file
    """

    if not default_parset_path.exists():
        raise FileNotFoundError(f"Unable to locate {default_parset_path=}")

    sbid_parset_path = Path(f"SEFD_{sbid}.parset")
    if not sbid_parset_path.exists():
        raise FileNotFoundError(f"Unable to locate {sbid_parset_path}")

    parset = ParameterSet(str(default_parset_path)).to_dict()
    sbid_parset = ParameterSet(str(sbid_parset_path)).to_dict()

    parset.update(sbid_parset)
    logger.info(f"Loaded the default parset, and updated with {sbid} parset for {ms}")

    # During the merge stage the HDF5 files need to be sorted, and the
    # code expects filenames to contain an index where the index represents
    # an increasing beam and frequency. The order will be extracted
    # outside this function, and the sorted order will be used here to
    # derive a consistent order.
    beam_min_freq = extract_beam_min_freq(ms)
    
    logger.info(f"Extracted {beam_min_freq=}")
    logger.info(f"{beam_min_freq_order=}")
    pos_idx = beam_min_freq_order.index(beam_min_freq)

    outfile_base = parset["outfile_base"].format(sbid, pos_idx)
    hdf5_filename = Path(os.getcwd()) / f"{outfile_base}.hdf5"
    logger.info(f"Constructed HDF5 filename: {hdf5_filename}")

    logger.info(f"Parset keys: {parset.keys()}")

    ms_sefd = SEFD(
        sbid,
        file_name=str(ms),
        dch=parset["nChanAvg"],
        ch0=parset["chan0"],
        ncf=parset["nFrqCells"],
        scan=parset["scan"],
        dnt=parset["nTimAvg"],
        nstart=parset["start"],
        nct=parset["nTimCells"],
        uvmin=parset["uvmin"],
    )
    ms_sefd.summary()
    ms_sefd.calc_sefd()

    if parset["decompose"]:
        ms_sefd.decompose(what="SEFD")
        ms_sefd.decompose(what="SCALE")

    logger.info(f"Saving to hdf5 file")
    ms_sefd.save_hdf5(str(hdf5_filename), per_ant=parset["decompose"])

    return hdf5_filename


def create_parset(sbid: int, workdir: Path) -> None:
    """Copies and creates the necessary parsets to support the SEFD pipeline

    Args:
        sbid (int): The SBID of the SEFD observation to process
        workdir (Path): Location to copy the parsets into, which is intended to be where processing will be carried out

    Raises:
        FileNotFoundError: Raised if the SEFD parset distributed with aces-apps can not be found
    """

    # Copy the deafault config file into place
    default_parset = Path(
        pkg_resources.resource_filename("aces", "sefd/SEFD_defaults.parset")
    )
    if not default_parset.exists():
        raise FileNotFoundError(f"{default_parset=} does not exist. ")

    logger.info(f"Copying {default_parset=} to {workdir=}")
    shutil.copy(default_parset, workdir)

    # Now create a special parset unique for this sbid
    logger.info(f"Building parset for {sbid=}")
    parset = ParameterSet()

    sched_block = SchedulingBlock(sbid)
    footprint = get_footprint(sched_block)

    parset.sbid = sched_block.id
    parset.footprint = footprint.to_parset()
    parset.footprint.pitch = sched_block.get_footprint_pitch()
    parset.footprint.rotation = sched_block.get_footprint_rotation()

    parset_out = Path(os.getcwd()) / f"SEFD_{sbid}.parset"
    logger.info(f"Writing {parset_out}")
    parset.to_file(parset_out)


def move_sefd_files_into(sbid: int, out_dir: Path) -> None:
    """Move the SEFD created files into a specified output directory. 

    Args:
        sbid (int): The SBID of the observation being processed.
        out_dir (Path): Location to move files to. 
    """
    
    if not out_dir.exists():
        logger.info(f"Creating {out_dir}")
        out_dir.mkdir(parents=True)

    data_products = [Path(p) for p in (
        f"SEFD_{sbid}.hdf5",
        f"SEFD_{sbid}.parset",
        f"SEFD_{sbid}_summary.png",
        "SEFD_defaults.parset"
    )]

    for data_product in data_products:
        assert data_product.exists(), f"Expected {data_product} to be present. "

        new_file = out_dir / data_product.name
        if new_file.exists():
            logger.warn(f"File {new_file} already exists. Removing. ")
            new_file.unlink()
            
        logger.info(f"Moving {data_product} to {new_file}.")
        data_product.rename(new_file)
