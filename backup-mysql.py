import os
from typing import Optional

from paramiko import SSHClient

from helpers.logger import FileLogger
from helpers.paths import TODAY_LOCAL_PATH
from helpers.remote_connect import remote_connect
from helpers.remote_copy import remote_copy
from settings import MYSQL_DB_NAMES, MYSQL_USER, MYSQL_USER_PASSWORD, REMOTE_HOST


logger = FileLogger()

# Create local backup folder
try:
    os.makedirs(TODAY_LOCAL_PATH)

except Exception as e:
    logger.error(f"Error while creating local backup folder: {str(e)}")

else:
    logger.success(f"Local backup folder {TODAY_LOCAL_PATH} created.")

    ssh_client = None

    # Local backup
    for db in MYSQL_DB_NAMES:
        try:
            db_filename: str = f"{db}.sql"
            dump_cmd: str = f"mysqldump --user={MYSQL_USER} --password={MYSQL_USER_PASSWORD} {db} > {TODAY_LOCAL_PATH}/{db_filename}"  # noqa E501
            os.system(dump_cmd)
        except Exception as e:
            logger.error(
                f"Error while trying to dump the database '{db}' locally: {str(e)}"  # noqa E501
            )
        else:
            logger.success(f"Backup file '{db_filename}' has been saved locally.")

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

logger.log("MySQL backup script completed.")

logger.close()
