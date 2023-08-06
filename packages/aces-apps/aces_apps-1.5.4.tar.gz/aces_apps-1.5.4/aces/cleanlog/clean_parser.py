import logging
import re
from datetime import datetime

import pandas as pd

LOGGER_REGEX = r"^(?P<level>\w+)\s+(?P<process>[\w\.]+)\s+\((?P<rank>\d+), (?P<node>\w+)\)\s+\[(?P<datetime>.+?)\] - (?P<message>.+)$"

logger = logging.getLogger(__name__)

def parse_clean_log(clean_log_file: (str)) -> pd.DataFrame:
    """Parse an ASKAPSoft imager log file and extract deconvolution data.

    Args:
        clean_log_file (str): filename of imager log file

    Returns:
        pd.DataFrame: devconulation data at different minor iterations
    """
    
    # regex for extracting deconvolution information
    logger_pattern = re.compile(LOGGER_REGEX)
    minor_cycle_message_pattern = re.compile(
        (
            r"^Iteration (?P<iteration>\d+), "
            r"Peak residual (?P<peak_resid>.+?), Objective function (?P<obj_func>.+?), Total flux "
            r"(?P<total_flux>.+?)$"
        )
    )

    # parse imager log file
    minor_cycles = []
    with open(clean_log_file) as f:
        for line in f:
            match = logger_pattern.match(line)
            if match:
                log = match.groupdict()
                if log["process"] == "deconvolution.monitor":
                    # extract the minor cycle info (iteration, peak_resid, obj_func, etc)
                    try:
                        minor_cycle_regex = minor_cycle_message_pattern.match(
                            log["message"]
                        )
                        
                        # Do nothing if the line did not match
                        if minor_cycle_regex is None:
                            continue
                        
                        minor_cycle_data = minor_cycle_regex.groupdict()
                        
                        log.update(minor_cycle_data)
                        minor_cycles.append(log)
                    except AttributeError:
                        logger.warning(
                            f"Log message regex match failed for line groupdict: {log}"
                        )
                
                elif log["process"] == "deconvolution.control":
                    minor_cycles[-1].update({"major_stop_reason": log["message"]})
                elif (
                    log["process"] == "deconvolution.multitermbasisfunction"
                    and "Exceeded" in log["message"]
                ):
                    minor_cycles[-1].update({"major_stop_reason": log["message"]})

    # format extracted data
    for d in minor_cycles:
        d["datetime"] = datetime.strptime(d["datetime"], "%Y-%m-%d %H:%M:%S,%f")
        d["peak_resid"] = float(d["peak_resid"])
        d["iteration"] = int(d["iteration"])
        d["obj_func"] = float(d["obj_func"])
        d["total_flux"] = float(d["total_flux"])

    minor_df = pd.DataFrame(data=minor_cycles).set_index("datetime")

    # determine major cycle numbers
    minor_df["major_cycle"] = -1
    minor_iter0_timestamps = minor_df.query("iteration == 0").index
    for i, date in enumerate(minor_iter0_timestamps):
        rows = minor_df.query("index >= @date").index
        minor_df.loc[rows, "major_cycle"] = i

    return minor_df
