import subprocess

from helpers.logger import FileLogger
from helpers.paths import TODAY_LOCAL_PATH
from helpers.remote import remote_backup
from settings import POSTGRES_DB_NAMES, POSTGRES_SYSTEM_USER, REMOTE_HOST


logger = FileLogger()


# Create local backup folde
proc = subprocess.Popen(
    f'su -c "mkdir -p {TODAY_LOCAL_PATH}" {POSTGRES_SYSTEM_USER}',
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

    # Local backup
    for db in POSTGRES_DB_NAMES:
        db_filename: str = f"{db}.dump"
        dump_cmd: str = f'su -c "pg_dump {db} > {TODAY_LOCAL_PATH}/{db_filename}" {POSTGRES_SYSTEM_USER}'  # noqa E501
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
                remote_backup(db_filename=db_filename, logger=logger)

logger.log("PostgreSQL backup script completed.")

logger.close()
