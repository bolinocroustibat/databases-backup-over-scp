from paramiko import SSHClient
from scp import SCPClient

from helpers.paths import TODAY_LOCAL_PATH, TODAY_REMOTE_PATH
from settings import REMOTE_HOST


def remote_copy(ssh_client: SSHClient, db_filename: str, logger) -> None:
    """
    Initiate distant file transfer.
    SCPClient takes a paramiko transport as its only argument
    """
    transport = ssh_client.get_transport()
    if transport:
        scp = SCPClient(transport)
        # Copy on remote
        try:
            scp.put(
                f"{TODAY_LOCAL_PATH}/{db_filename}",
                f"{TODAY_REMOTE_PATH}/{db_filename}",
            )  # noqa E501
            logger.success(
                f"Backup file '{db_filename}' has been copied on '{REMOTE_HOST}'"  # noqa E501
            )
        except Exception as e:
            logger.error(
                f"Error while copying '{db_filename}' on '{REMOTE_HOST}': {str(e)}"  # noqa E501
            )
        scp.close()
