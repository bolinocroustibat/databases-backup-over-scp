#!/usr/bin/python

import os

from logger import TODAY_LOCAL_PATH, FileLogger
from remote import remote_backup
from settings import MYSQL_DB_NAMES, MYSQL_USER, MYSQL_USER_PASSWORD, REMOTE_URL


logger = FileLogger()

# Create local backup folder
try:
    os.makedirs(TODAY_LOCAL_PATH)
    logger.log(f"Local backup folder {TODAY_LOCAL_PATH} created.")
except Exception as e:
    logger.log(f"### ERROR ### while creating local backup folder: {str(e)}")

# Local backup
for db in MYSQL_DB_NAMES:
    try:
        dump_cmd = f"mysqldump --user={MYSQL_USER} --password={MYSQL_USER_PASSWORD} {db} > {TODAY_LOCAL_PATH}/{db}.sql"
        os.system(dump_cmd)
        logger.log(f"Backup dump file {db}.sql has been saved locally.")
    except Exception as e:
        logger.log(
            f"### ERROR ### while trying to dump the database '{db}' locally: {str(e)}"
        )

# Remote backup
if REMOTE_URL:
    remote_backup(db_names=MYSQL_DB_NAMES, logger=logger)

logger.log("MySQL backup script completed.")

logger.close()
