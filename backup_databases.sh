#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

source helpers/load_config.sh
source helpers/logger.sh
source helpers/create_local_folder.sh
source helpers/remote_connect.sh
source helpers/remote_copy.sh

MYSQL_DB_NAMES=$(config "mysql" "db_names")
MYSQL_USER=$(config "mysql" "user")
MYSQL_USER_PASSWORD=$(config "mysql" "user_password")

POSTGRES_DB_NAMES=$(config "postgres" "db_names")
POSTGRES_PASSWD=$(config "postgres" "password")
POSTGRES_PORT=$(config "postgres" "port")
POSTGRES_SYSTEM_USER=$(config "postgres" "system_user")

REMOTE_HOST=$(config "remote" "host")
REMOTE_USER=$(config "remote" "user")
REMOTE_PATH=$(config "remote" "path")

# Create local backup folder
local_path=$(create_local_folder)

if [[ -n "$local_path" ]]; then

    ssh_client=""
    remote_path=""

    # Check if mysqldump command exists
    if command -v mysqldump &> /dev/null; then
        # Local MySQL backup
        IFS=', ' read -r -a mysql_dbs <<< "$MYSQL_DB_NAMES"
        for db in "${mysql_dbs[@]}"; do
            db_filename="${db}.sql.gz"
            dump_cmd="mysqldump --user=${MYSQL_USER} --password=${MYSQL_USER_PASSWORD} ${db} | gzip -9 -c > ${local_path}/${db_filename}"

            if eval "$dump_cmd"; then
                log "Backup file '${local_path}/${db_filename}' has been saved locally."
                remote_copy "$local_path" "$db_filename"
            else
                error "Error while trying to dump the MySQL database '${db}' locally."
                exit 1
            fi
        done
    else
        error "mysqldump command not found. Not able to backup MySQL databases."
    fi

    # Local PostgreSQL backup
    IFS=', ' read -r -a postgres_dbs <<< "$POSTGRES_DB_NAMES"
    for db in "${postgres_dbs[@]}"; do
        db_filename="${db}.dump"
        dump_cmd="su - ${POSTGRES_SYSTEM_USER} -c \"PGPASSWORD='${POSTGRES_PASSWD}' pg_dump ${db} -Fc -U ${POSTGRES_SYSTEM_USER} -p ${POSTGRES_PORT} > ${local_path}/${db_filename}\""

        if eval "$dump_cmd"; then
            log "Backup dump file '${local_path}/${db_filename}' has been saved locally."
            remote_copy "$local_path" "$db_filename"
        else
            error "Error while trying to dump the PostgreSQL database '${db}' locally."
            exit 1
        fi
    done
else
    error "Failed to create local backup folder. Exiting."
    exit 1
fi
