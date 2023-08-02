from typing import Optional

from paramiko import SSHClient

from helpers.paths import TODAY_REMOTE_PATH
from settings import REMOTE_HOST, REMOTE_USER


def remote_connect(logger) -> Optional[SSHClient]:
    """
    Returns ssh connection to remote server if creation of remote folder was successful
    """
    try:
        # Connect to backup server
        ssh_client: SSHClient = SSHClient()
        ssh_client.load_system_host_keys()
        ssh_client.connect(REMOTE_HOST, username=REMOTE_USER)

    except Exception as e:
        logger.error(f"Error while connecting to remote '{REMOTE_HOST}': {str(e)}")

    else:
        # Create remote backup folder
        try:
            ssh_client.exec_command(f"mkdir -p {TODAY_REMOTE_PATH}")
            ssh_client.close
            logger.success(
                f"Remote backup folder {TODAY_REMOTE_PATH} created on '{REMOTE_HOST}'"
            )
        except Exception as e:
            logger.error(
                f"Error while creating remote backup folder '{TODAY_REMOTE_PATH}' on '{REMOTE_HOST}': {str(e)}"  # noqa E501
            )
        else:
            return ssh_client
