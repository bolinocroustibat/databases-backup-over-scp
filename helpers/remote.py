from paramiko import SSHClient
from scp import SCPClient

from helpers.paths import TODAY_LOCAL_PATH, TODAY_REMOTE_PATH
from settings import REMOTE_HOST, REMOTE_USER


def remote_backup(db_filename: str, logger) -> None:
    try:
        # Connect to backup server
        ssh = SSHClient()
        ssh.load_system_host_keys()
        ssh.connect(REMOTE_HOST, username=REMOTE_USER)
    except Exception as e:
        logger.error(f"Error while connecting to remote '{REMOTE_HOST}': {str(e)}")
    else:
        # Create remote backup folder
        try:
            ssh.exec_command(f"mkdir -p {TODAY_REMOTE_PATH}")
            ssh.close
            logger.success(
                f"Remote backup folder {TODAY_REMOTE_PATH} created on '{REMOTE_HOST}'"
            )
        except Exception as e:
            logger.error(
                f"Error while creating remote backup folder '{TODAY_REMOTE_PATH}' on '{REMOTE_HOST}': {str(e)}"  # noqa E501
            )
        else:
            # Initiate distant file transfer.
            # SCPClient takes a paramiko transport as its only argument
            transport = ssh.get_transport()
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
