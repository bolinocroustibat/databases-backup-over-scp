from paramiko import SSHClient
from scp import SCPClient

from settings import REMOTE_HOST


def remote_copy(
    logger, ssh_client: SSHClient, local_path: str, remote_path: str, db_filename: str
) -> None:
    """
    Initiate distant file transfer.
    SCPClient takes a paramiko transport as its only argument
    """
    transport = ssh_client.get_transport()
    if transport:
        scp = SCPClient(transport)
        try:
            scp.put(
                f"{local_path}/{db_filename}",
                f"{remote_path}/{db_filename}",
            )
            logger.success(f"Backup file '{db_filename}' has been copied on '{REMOTE_HOST}'")
        except Exception as e:
            logger.error(f"Error while copying '{db_filename}' on '{REMOTE_HOST}': {str(e)}")
        scp.close()
