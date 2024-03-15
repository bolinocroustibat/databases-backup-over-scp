import os
import subprocess

from helpers.logger import FileLogger
from helpers.create_local_folder import create_local_folder
from helpers.remote_connect import remote_connect
from helpers.remote_copy import remote_copy
from settings import (
    MYSQL_DB_NAMES,
    MYSQL_USER,
    MYSQL_USER_PASSWORD,
    POSTGRES_DB_NAMES,
    POSTGRES_SYSTEM_USER,
    POSTGRES_PASSWD,
    POSTGRES_PORT,
    REMOTE_HOST,
)


logger = FileLogger()


local_path: str | None = create_local_folder(logger)

if local_path:
    ssh_client = None
    remote_path = None

    # Local MySQL backup
    for db in MYSQL_DB_NAMES:
        try:
            db_filename: str = f"{db}.sql.gz"
            dump_cmd: str = f"mysqldump --user={MYSQL_USER} --password={MYSQL_USER_PASSWORD} {db} | gzip -9 -c > {local_path}/{db_filename}"  # noqa E501
            os.system(dump_cmd)
        except Exception as e:
            logger.error(
                f"Error while trying to dump the database '{db}' locally: {str(e)}"  # noqa E501
            )
        else:
            logger.success(f"Backup file '{db_filename}' has been saved locally.")

            # Remote MySQL backup
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

    # Local PostgreSQL backup
    for db in POSTGRES_DB_NAMES:
        db_filename: str = f"{db}.gzip"
        dump_cmd: str = f'su - {POSTGRES_SYSTEM_USER} -c "PGPASSWORD="{POSTGRES_PASSWD}" pg_dump {db} -Fc -U {POSTGRES_SYSTEM_USER} -p {POSTGRES_PORT} > {local_path}/{db_filename}'  # noqa E501
        proc = subprocess.Popen(dump_cmd, shell=True)
        proc.wait()
        (stdout, stderr) = proc.communicate()

        if stderr:
            logger.error(
                f"Error while trying to dump the database {db} locally: {stderr.decode()}"  # noqa E501
            )
        else:
            logger.success(f"Backup dump file '{db_filename}' has been saved locally.")

            # Remote PostgreSQL backup
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

logger.log("Backup script completed.")

logger.close()
