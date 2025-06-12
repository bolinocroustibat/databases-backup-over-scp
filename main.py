#!/usr/bin/env -S uv run --script
# /// script
# dependencies = [
#     "paramiko<4.0.0,>=3.0.0",
#     "scp<1.0.0,>=0.14.1",
# ]
# ///

import subprocess
from pathlib import Path

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
logger.debug("Script started")

local_path: Path | None = create_local_folder(logger)

if local_path:
    logger.debug(f"Local backup path created: {local_path}")
    ssh_client = None
    remote_path = None

    # Local MySQL backup
    if MYSQL_DATABASES:
        logger.debug(f"Starting MySQL backups for {len(MYSQL_DATABASES)} databases")
    for db_name, db_config in MYSQL_DATABASES.items():
        logger.debug(f"Processing MySQL database: {db_name}")
        try:
            db_filename: str = f"{db_name}.sql.gz"
            dump_cmd: str = f"mysqldump --user={db_config['user']} --password={db_config['password']} {db_name} | gzip -9 -c > {local_path / db_filename}"  # noqa E501
            logger.debug(f"Running MySQL dump command for {db_name}")
            result = subprocess.run(
                dump_cmd, shell=True, capture_output=True, text=True, timeout=300
            )  # 5 minutes timeout

            if result.returncode != 0:
                logger.error(
                    f"Error while trying to dump the database '{db_name}' locally: {result.stderr}"  # noqa E501
                )
                continue

            logger.success(f"Backup file '{local_path / db_filename}' has been saved locally.")

            # Remote MySQL backup
            if REMOTE_HOST:
                if not ssh_client and not remote_path:
                    logger.debug("Establishing SSH connection")
                    (ssh_client, remote_path) = remote_connect(logger) or (None, None)
                if ssh_client and remote_path:
                    remote_copy(logger, ssh_client, local_path, remote_path, db_filename)
                else:
                    logger.error("Couldn't copy on server, couldn't get SSH connection.")
        except subprocess.TimeoutExpired:
            logger.error(f"Timeout while trying to dump the database '{db_name}'")
        except Exception as e:
            logger.error(
                f"Error while trying to dump the database '{db_name}' locally: {str(e)}"  # noqa E501
            )

    # Local PostgreSQL backup
    if POSTGRES_DATABASES:
        logger.debug(f"Starting PostgreSQL backups for {len(POSTGRES_DATABASES)} databases")
    for db_name, db_config in POSTGRES_DATABASES.items():
        logger.debug(f"Processing PostgreSQL database: {db_name}")
        try:
            db_filename: str = f"{db_name}.dump"
            dump_cmd: str = f'PGPASSWORD="{db_config["password"]}" pg_dump {db_name} -Fc -U {db_config["user"]} -h 127.0.0.1 -p {db_config["port"]} > {local_path / db_filename}'  # noqa E501
            logger.debug(f"Running PostgreSQL dump command for {db_name}")
            result = subprocess.run(
                dump_cmd, shell=True, capture_output=True, text=True, timeout=300
            )  # 5 minutes timeout

            if result.returncode != 0:
                logger.error(
                    f"Error while trying to dump the database {db_name} locally: {result.stderr}"  # noqa E501
                )
                continue

            logger.success(f"Backup dump file '{local_path / db_filename}' has been saved locally.")

            # Remote PostgreSQL backup
            if REMOTE_HOST:
                if not ssh_client and not remote_path:
                    logger.debug("Establishing SSH connection")
                    (ssh_client, remote_path) = remote_connect(logger) or (None, None)
                if ssh_client and remote_path:
                    remote_copy(logger, ssh_client, local_path, remote_path, db_filename)
                else:
                    logger.error("Couldn't copy on server, couldn't get SSH connection.")
        except subprocess.TimeoutExpired:
            logger.error(f"Timeout while trying to dump the database '{db_name}'")
        except Exception as e:
            logger.error(
                f"Error while trying to dump the database {db_name} locally: {str(e)}"  # noqa E501
            )

logger.log("Backup script completed.")
logger.close()
