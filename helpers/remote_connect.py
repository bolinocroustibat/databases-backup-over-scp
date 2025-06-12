from datetime import UTC, datetime
from pathlib import Path
from typing import Tuple

from paramiko import SSHClient

from settings import REMOTE_HOST, REMOTE_PATH, REMOTE_USER


def remote_connect(logger) -> Tuple[SSHClient, Path] | None:
    """
    Returns SSH connection and path of created folder on remote server
    if creation of remote folder was successful
    """
    now: str = datetime.now(UTC).strftime("%Y-%m-%d_%H-%M")
    remote_path = Path(REMOTE_PATH) / now
    logger.debug(f"Connecting to remote host: {REMOTE_HOST}")
    try:
        # Connect to backup server
        ssh_client: SSHClient = SSHClient()
        ssh_client.load_system_host_keys()
        logger.debug(f"Establishing SSH connection to {REMOTE_HOST} as {REMOTE_USER}")
        ssh_client.connect(REMOTE_HOST, username=REMOTE_USER)

    except Exception as e:
        logger.error(f"Error while connecting to remote '{REMOTE_HOST}': {str(e)}")

    else:
        # Create remote backup folder
        try:
            logger.debug(f"Creating remote backup folder: {remote_path}")
            ssh_client.exec_command(f"mkdir -p {remote_path}")
            ssh_client.close
            logger.success(f"Remote backup folder {remote_path} created on '{REMOTE_HOST}'")
        except Exception as e:
            logger.error(
                f"Error while creating remote backup folder '{remote_path}' on '{REMOTE_HOST}': {str(e)}"  # noqa E501
            )
        else:
            return ssh_client, remote_path
