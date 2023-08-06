"""Utility functions to help inspect the environment a workflow is running on. 
"""

import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)


def log_environment(local_logger: Optional[logging.Logger]=None) -> None:
    """Logs details about the environment executing the function. Used
    primarily to record details to a logger for debugging and recording. Details
    captured are current working directory, and environment variables.

    If an Orion logging handler has been attached via PREFECT_LOGGING_EXTRAS and this function
    is called before a flow has started, an error would be raised. An alternate logging object
    may be passed though. 

    Args:
        local_logger (Optional[logging.Logger], optional): A logger that is desired for output. Useful for logging in functions outside of a prefect flow if an Orion handler has been attached. If None, the aces logger is used. Defaults to None. 
    """
    items = ["Recording environment configuration", f"Working directory: {os.getcwd()}"]
    items.extend([f"{key}: {os.environ[key]}" for key in sorted(os.environ.keys())])

    # If an Orion logging handler has been attached via PREFECT_LOGGING_EXTRAS and this function
    # is called before a flow has started, an error would be raised. An alternate logging object
    # may be passed though. 
    if local_logger is None:
        local_logger = logger 
    
    local_logger.info("\n".join(items))
