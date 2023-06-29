import os

from helpers.logger import FileLogger
from helpers.paths import TODAY_LOCAL_PATH
from helpers.remote import remote_backup
from settings import MYSQL_DB_NAMES, MYSQL_USER, MYSQL_USER_PASSWORD, REMOTE_HOST


logger = FileLogger()

# Create local backup folder
try:
    os.makedirs(TODAY_LOCAL_PATH)
except Exception as e:
    logger.log(f"### ERROR ### while creating local backup folder: {str(e)}")
else:
    logger.log(f"Local backup folder {TODAY_LOCAL_PATH} created.")

    # Local backup
    for db in MYSQL_DB_NAMES:
        try:
            dump_cmd: str = f"mysqldump --user={MYSQL_USER} --password={MYSQL_USER_PASSWORD} {db} > {TODAY_LOCAL_PATH}/{db}.sql"  # noqa E501
            os.system(dump_cmd)
        except Exception as e:
            logger.log(
                f"### ERROR ### while trying to dump the database '{db}' locally: {str(e)}"  # noqa E501
            )
        else:
            logger.log(f"Backup dump file {db}.sql has been saved locally.")
            # Remote backup
            if REMOTE_HOST:
                remote_backup(db_names=MYSQL_DB_NAMES, logger=logger)

logger.log("MySQL backup script completed.")

logger.close()
