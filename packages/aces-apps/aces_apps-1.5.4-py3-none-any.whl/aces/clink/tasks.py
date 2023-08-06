from pathlib import Path

from prefect import task, get_run_logger 
from prefect.blocks.system import Secret

from aces.clink.clink import create_emit_clink_event

@task
def task_create_emit_clink_event(
    secret_block: str, sbid: int, workdir: Path, operation: str, state: str = "completed"
) -> None:
    """A prefect task that will emit a clink based event to inform other systems that data-processing has gone through a state change

    Args:
        secret_block (str): Name of registered Prefect Secret block corresponding to the desired clink url (which includes authentication)
        sbid (int): SBID being processed
        workdir (Path): The location of the work that has been carried out
        operation (str): Specifies the type of work that has been carried out. For example, holography of sefd
        state (str, optional): The state of the processing that should be advertised. Defaults to 'completed'.
    """
    logger = get_run_logger()
    
    # Acquire the clink endpoint url, which contains the authentication details, from prefect orion
    logger.info(f"Obtaining the {secret_block} block")
    try:
        clink_transport_url = Secret.load(secret_block).get()
    except:
        logger.warning(f"Unable to load the {secret_block} block, not emitting clink event. ")
        return
    
    create_emit_clink_event(
        clink_transport_url,
        sbid,
        workdir,
        operation=operation,
        state=state
    )