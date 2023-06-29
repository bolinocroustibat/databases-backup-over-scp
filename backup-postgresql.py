import os

from helpers.logger import FileLogger
from helpers.paths import TODAY_LOCAL_PATH
from helpers.remote import remote_backup
from settings import POSTGRES_DB_NAMES, POSTGRES_SYSTEM_USER, REMOTE_HOST


logger = FileLogger()

# Create local backup folder
try:
    os.system(f'su -c "mkdir -p {TODAY_LOCAL_PATH}" {POSTGRES_SYSTEM_USER}')
    logger.log(f"Local backup folder {TODAY_LOCAL_PATH} created.")
except Exception as e:
    logger.log(f"### ERROR ### while creating local backup folder: {str(e)}")

# Local backup
for db in POSTGRES_DB_NAMES:
    try:
        dump_cmd: str = (
            f'su -c "pg_dump {db} > {TODAY_LOCAL_PATH}/{db}.sql" {POSTGRES_SYSTEM_USER}'
        )
        os.system(dump_cmd)
        logger.log(f"Backup dump file {db}.sql has been saved locally.")
    except Exception as e:
        logger.log(
            f"### ERROR ### while trying to dump the database {db} locally: {str(e)}"
        )

# Remote backup
if REMOTE_HOST:
    remote_backup(db_names=POSTGRES_DB_NAMES, logger=logger)

logger.log("PostgreSQL backup script completed.")

logger.close()
