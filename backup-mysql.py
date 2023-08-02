import os
from typing import Optional

from helpers.logger import FileLogger
from helpers.create_local_folder import create_local_folder
from helpers.remote_connect import remote_connect
from helpers.remote_copy import remote_copy
from settings import (
    MYSQL_DB_NAMES,
    MYSQL_USER,
    MYSQL_USER_PASSWORD,
    REMOTE_HOST,
)


logger = FileLogger()


local_path: Optional[str] = create_local_folder(logger)

if local_path:
    ssh_client = None
    remote_path = None

    # Local backup
    for db in MYSQL_DB_NAMES:
        try:
            db_filename: str = f"{db}.sql"
            dump_cmd: str = f"mysqldump --user={MYSQL_USER} --password={MYSQL_USER_PASSWORD} {db} > {local_path}/{db_filename}"  # noqa E501
            os.system(dump_cmd)
        except Exception as e:
            logger.error(
                f"Error while trying to dump the database '{db}' locally: {str(e)}"  # noqa E501
            )
        else:
            logger.success(f"Backup file '{db_filename}' has been saved locally.")

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

logger.log("MySQL backup script completed.")

logger.close()
