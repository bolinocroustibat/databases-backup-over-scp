from pathlib import Path

from paramiko import SSHClient
from scp import SCPClient

from settings import REMOTE_HOST


def remote_copy(
    logger, ssh_client: SSHClient, local_path: Path, remote_path: Path, db_filename: str
) -> None:
    """
    Initiate distant file transfer.
    SCPClient takes a paramiko transport as its only argument
    """
    transport = ssh_client.get_transport()
    if transport:
        logger.debug(f"Starting SCP transfer of {db_filename} to {REMOTE_HOST}")
        scp = SCPClient(transport)
        try:
            local_file = local_path / db_filename
            remote_file = str(remote_path / db_filename)
            logger.debug(f"Copying {local_file} to {remote_file}")
            scp.put(
                str(local_file),
                remote_file,
            )
            logger.success(f"Backup file '{db_filename}' has been copied on '{REMOTE_HOST}'")
        except Exception as e:
            logger.error(f"Error while copying '{db_filename}' on '{REMOTE_HOST}': {str(e)}")
        scp.close()
