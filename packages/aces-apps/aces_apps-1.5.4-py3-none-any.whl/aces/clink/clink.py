"""Utilities and helper functions to work with creating
events by clink for consumption.
"""
import logging
import os
from collections import namedtuple
from pathlib import Path
from typing import Any, Optional

from clink import clink
from clink import settings as clink_settings
from prefect.context import get_run_context

logger = logging.getLogger(__name__)

ClinkEvent = namedtuple(
    "ClinkEvent",
    (
        "sbid",
        "workdir",
        "flow_run_id",
        "flow_run_start",
        "clink_subject",
        "clink_participant",
        "clink_type",
    ),
)

def create_clink_event(
    sbid: int, operation: str, state: str = "completed", workdir: Optional[Path] = None
) -> ClinkEvent:
    """Constructs a ClinkEvent based on inputs, registering inputs against known fields
    compatible with :aces.clink.clink.emmit_clink_event:

    Args:
        sbid (int): SBID of the observation being processed
        operation (str): Type of processing or operation that has been applied to the SBID
        state (str, optional): What state should be emitted for the operation. Defaults to "completed".
        workdir (Optional[Path], optional): Location where work was carried out. Defaults to None.
    
    Returns:
        ClinkEvent: Details that will be emmited by clink to cpmanager
    """

    logger.debug(f"Creating clink event for {sbid=} {operation=}")
    if workdir is None:
        workdir = Path(os.getcwd())

    flow_run_dict = get_run_context().dict()
    flow_run_id = str(flow_run_dict["task_run"]["flow_run_id"])
    flow_run_start = str(flow_run_dict["task_run"]["start_time"])

    clink_subject = f"urn:askap:{operation}:pawsey:askapops:flow-run/{flow_run_id}"
    clink_participant = f"au.csiro.atnf.askap.{operation}"
    clink_type = f"au.csiro.atnf.askap.{operation}.{state}"

    clink_event = ClinkEvent(
        sbid,
        str(workdir),
        flow_run_id,
        flow_run_start,
        clink_subject,
        clink_participant,
        clink_type,
    )
    logger.debug(f"Returning: {clink_event}")

    return clink_event


def format_clink_data(clink_event: ClinkEvent) -> dict[str, Any]:
    """Create an expect data payload to interact with clink / cpmanager. For the moment this
    merely creates a straight forward dict, but if logic grows this can be expanded to encompass
    a larger rule-set

    Args:
        clink_event (ClinkEvent): The data that will be packed to send to cpmanager

    Returns:
        dict[str, Any]: Formatted structure to be presented to clink
    """
    return dict(
        flowRun=dict(
            id=clink_event.flow_run_id,
            path=str(clink_event.workdir),
            processedAt=clink_event.flow_run_start,
            schedulingBlock=dict(id=str(clink_event.sbid)),
        )
    )


def emit_clink_event(clink_event: ClinkEvent) -> None:
    """Send a ClinkEvent through to cpmanager to report progress on
    some type of processing

    Args:
        clink_event (ClinkEvent): Formatted data and clink configurables
    """
    
    clink_data = format_clink_data(clink_event)

    # Define the message queue event will be tagged to
    participant = clink.Participant(clink_event.clink_participant)

    # Log the event that will be issued
    logger.info(f"Emitting clink subject: {clink_event.clink_subject=}")
    logger.info(f"Emiting clink data: {clink_data=}")

    # Register event with the message queue
    participant.emit_event(
        type=clink_event.clink_type,
        subject=clink_event.clink_subject,
        data=clink_data,
    )

def create_emit_clink_event(
    transport_url: str, sbid: int, workdir: Path, operation: str, state: str = "completed"
) -> None:
    """A prefect task that will emit a clink based event to inform other systems that data-processing has gone through a state change

    Args:
        secret_block (str): Name of registered Prefect Secret block corresponding to the desired clink url (which includes authentication)
        sbid (int): SBID being processed
        workdir (Path): The location of the work that has been carried out
        operation (str): Specifies the type of work that has been carried out. For example, holography of sefd
        state (str, optional): The state of the processing that should be advertised. Defaults to 'completed'.
    """
    # This TRANSPORT_URL is the default url that is used if a transport_url has
    # not been used when creating a clink Dispatcher / Backend object
    clink_settings.TRANSPORT_URL = transport_url
    
    logger.info(f"Creating clink data payload")
    clink_event = create_clink_event(sbid, operation, state=state, workdir=workdir)

    logger.info(f"Submitting {clink_event=}")
    emit_clink_event(clink_event)



