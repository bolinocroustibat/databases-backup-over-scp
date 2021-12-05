from paramiko import SSHClient
from scp import SCPClient

from logger import TODAY_LOCAL_PATH, TODAY_REMOTE_PATH
from settings import REMOTE_URL, REMOTE_USER, REMOTE_PATH


def remote_backup(db_names: list, logger) -> None:
    try:
        # Connect to backup server
        ssh = SSHClient()
        ssh.load_system_host_keys()
        ssh.connect(REMOTE_URL, username=REMOTE_USER)
    except Exception as e:
        logger.log(f"### ERROR ### while connecting to remote '{REMOTE_URL}': {str(e)}")
    else:
        # Create remote backup folder
        try:
            ssh.exec_command(f"mkdir -p {TODAY_REMOTE_PATH}")
            ssh.close
            logger.log(
                f"Remote backup folder {TODAY_REMOTE_PATH} created on '{REMOTE_URL}'"
            )
        except Exception as e:
            logger.log(
                f"### ERROR ### while creating remote backup folder '{TODAY_REMOTE_PATH}' on '{REMOTE_URL}': {str(e)}"
            )
        else:
            # Initiate distant file transfer. SCPClient takes a paramiko transport as its only argument
            scp = SCPClient(ssh.get_transport())
            # Copy on remote
            for db in db_names:
                try:
                    scp.put(
                        f"{TODAY_LOCAL_PATH}/{db}.sql", f"{TODAY_REMOTE_PATH}/{db}.sql"
                    )
                    logger.log(
                        f"Backup file '{db}.sql' has been copied on '{REMOTE_URL}'"
                    )
                except Exception as e:
                    logger.log(
                        f"### ERROR ### while copying '{db}.sql' on '{REMOTE_URL}': {str(e)}"
                    )
            scp.close()
