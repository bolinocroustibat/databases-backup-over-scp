import subprocess
from typing import Optional

from paramiko import SSHClient

from helpers.logger import FileLogger
from helpers.paths import TODAY_LOCAL_PATH
from helpers.remote_connect import remote_connect
from helpers.remote_copy import remote_copy
from settings import POSTGRES_DB_NAMES, POSTGRES_SYSTEM_USER, REMOTE_HOST


logger = FileLogger()


# Create local backup folder
proc = subprocess.Popen(
    f'su - {POSTGRES_SYSTEM_USER} -c "mkdir -p {TODAY_LOCAL_PATH}"',
    shell=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)
proc.wait()
(stdout, stderr) = proc.communicate()

if stderr:
    logger.error(f"Error while creating local backup folder: {stderr.decode()}")

else:
    logger.success(f"Local backup folder {TODAY_LOCAL_PATH} created.")

    ssh_client = None

    # Local backup
    for db in POSTGRES_DB_NAMES:
        db_filename: str = f"{db}.dump"
        dump_cmd: str = f'su - {POSTGRES_SYSTEM_USER} -c "pg_dump {db} > {TODAY_LOCAL_PATH}/{db_filename}" '  # noqa E501
        proc = subprocess.Popen(dump_cmd, shell=True)
        proc.wait()
        (stdout, stderr) = proc.communicate()

        if stderr:
            logger.error(
                f"Error while trying to dump the database {db} locally: {stderr.decode()}"  # noqa E501
            )
        else:
            logger.success(f"Backup dump file '{db_filename}' has been saved locally.")

            # Remote backup
            if REMOTE_HOST:
                if not ssh_client:
                    ssh_client: Optional[SSHClient] = remote_connect(logger)
                if ssh_client:
                    remote_copy(ssh_client, db_filename, logger)
                else:
                    logger.error(
                        "Couldn't copy on server, couldn't get SSH connection."
                    )

logger.log("PostgreSQL backup script completed.")

logger.close()
