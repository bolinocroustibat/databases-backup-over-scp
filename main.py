import os
import subprocess

from helpers.create_local_folder import create_local_folder
from helpers.logger import FileLogger
from helpers.remote_connect import remote_connect
from helpers.remote_copy import remote_copy
from settings import (
    MYSQL_DATABASES,
    POSTGRES_DATABASES,
    REMOTE_HOST,
)

logger = FileLogger()


local_path: str | None = create_local_folder(logger)

if local_path:
    ssh_client = None
    remote_path = None

    # Local MySQL backup
    for db_name, db_config in MYSQL_DATABASES.items():
        try:
            db_filename: str = f"{db_name}.sql.gz"
            dump_cmd: str = f"mysqldump --user={db_config['user']} --password={db_config['password']} --port={db_config['port']} {db_name} | gzip -9 -c > {local_path}/{db_filename}"  # noqa E501
            os.system(dump_cmd)
        except Exception as e:
            logger.error(
                f"Error while trying to dump the database '{db_name}' locally: {str(e)}"  # noqa E501
            )
        else:
            logger.success(f"Backup file '{local_path}/{db_filename}' has been saved locally.")

            # Remote MySQL backup
            if REMOTE_HOST:
                if not ssh_client and not remote_path:
                    (ssh_client, remote_path) = remote_connect(logger) or (None, None)
                if ssh_client and remote_path:
                    remote_copy(logger, ssh_client, local_path, remote_path, db_filename)
                else:
                    logger.error("Couldn't copy on server, couldn't get SSH connection.")

    # Local PostgreSQL backup
    for db_name, db_config in POSTGRES_DATABASES.items():
        db_filename: str = f"{db_name}.dump"
        dump_cmd: str = f'su - {db_config["user"]} -c "PGPASSWORD="{db_config["password"]}" pg_dump {db_name} -Fc -U {db_config["user"]} -p {db_config["port"]} > {local_path}/{db_filename}"'  # noqa E501
        proc = subprocess.Popen(dump_cmd, shell=True)
        proc.wait()
        (stdout, stderr) = proc.communicate()

        if stderr:
            logger.error(
                f"Error while trying to dump the database {db_name} locally: {stderr.decode()}"  # noqa E501
            )
        else:
            logger.success(f"Backup dump file '{local_path}/{db_filename}' has been saved locally.")

            # Remote PostgreSQL backup
            if REMOTE_HOST:
                if not ssh_client and not remote_path:
                    (ssh_client, remote_path) = remote_connect(logger) or (None, None)
                if ssh_client and remote_path:
                    remote_copy(logger, ssh_client, local_path, remote_path, db_filename)
                else:
                    logger.error("Couldn't copy on server, couldn't get SSH connection.")

logger.log("Backup script completed.")

logger.close()
