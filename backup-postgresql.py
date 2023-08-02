import subprocess
from typing import Optional

from helpers.logger import FileLogger
from helpers.create_local_folder import create_local_folder
from helpers.remote_connect import remote_connect
from helpers.remote_copy import remote_copy
from settings import POSTGRES_DB_NAMES, POSTGRES_SYSTEM_USER, REMOTE_HOST


logger = FileLogger()


local_path: Optional[str] = create_local_folder(logger)

if local_path:
    ssh_client = None
    remote_path = None

    # Local backup
    for db in POSTGRES_DB_NAMES:
        db_filename: str = f"{db}.dump"
        dump_cmd: str = f'su - {POSTGRES_SYSTEM_USER} -c "pg_dump {db} > {local_path}/{db_filename}" '  # noqa E501
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
                if not ssh_client and not remote_path:
                    (ssh_client, remote_path) = remote_connect(logger) or (None, None)
                if ssh_client and remote_path:
                    remote_copy(
                        logger, ssh_client, local_path, remote_path, db_filename
                    )
                else:
                    logger.error(
                        "Couldn't copy on server, couldn't get SSH connection."
                    )

logger.log("PostgreSQL backup script completed.")

logger.close()
