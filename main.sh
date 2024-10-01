#!/bin/bash

source helpers/read_ini_file.sh
source helpers/logger.sh
source helpers/create_local_folder.sh
source helpers/remote_connect.sh
source helpers/remote_copy.sh

# Load settings from settings.ini
CONFIG_FILE="settings.ini"

MYSQL_DB_NAMES=$(read_ini_file "$CONFIG_FILE" "mysql" "db_names")
MYSQL_USER=$(read_ini_file "$CONFIG_FILE" "mysql" "user")
MYSQL_USER_PASSWORD=$(read_ini_file "$CONFIG_FILE" "mysql" "user_password")

POSTGRES_DB_NAMES=$(read_ini_file "$CONFIG_FILE" "postgres" "db_names")
POSTGRES_PASSWD=$(read_ini_file "$CONFIG_FILE" "postgres" "password")
POSTGRES_PORT=$(read_ini_file "$CONFIG_FILE" "postgres" "port")
POSTGRES_SYSTEM_USER=$(read_ini_file "$CONFIG_FILE" "postgres" "system_user")

REMOTE_HOST=$(read_ini_file "$CONFIG_FILE" "remote" "host")
REMOTE_USER=$(read_ini_file "$CONFIG_FILE" "remote" "user")
REMOTE_PATH=$(read_ini_file "$CONFIG_FILE" "remote" "path")

# Create local backup folder
local_path=$(create_local_folder)

if [[ -n "$local_path" ]]; then
    ssh_client=""
    remote_path=""

    # Local MySQL backup
    IFS=', ' read -r -a mysql_dbs <<< "$MYSQL_DB_NAMES"
    for db in "${mysql_dbs[@]}"; do
        db_filename="${db}.sql.gz"
        dump_cmd="mysqldump --user=${MYSQL_USER} --password=${MYSQL_USER_PASSWORD} ${db} | gzip -9 -c > ${local_path}/${db_filename}"

        if eval "$dump_cmd"; then
            info "Backup file '${local_path}/${db_filename}' has been saved locally."
            remote_copy "$local_path" "$db_filename"
        else
            error "Error while trying to dump the database '${db}' locally."
        fi
    done

    # Local PostgreSQL backup
    IFS=', ' read -r -a postgres_dbs <<< "$POSTGRES_DB_NAMES"
    for db in "${postgres_dbs[@]}"; do
        db_filename="${db}.dump"
        dump_cmd="su - ${POSTGRES_SYSTEM_USER} -c \"PGPASSWORD='${POSTGRES_PASSWD}' pg_dump ${db} -Fc -U ${POSTGRES_SYSTEM_USER} -p ${POSTGRES_PORT} > ${local_path}/${db_filename}\""

        if eval "$dump_cmd"; then
            info "Backup dump file '${local_path}/${db_filename}' has been saved locally."
            remote_copy "$local_path" "$db_filename"
        else
            error "Error while trying to dump the database '${db}' locally."
        fi
    done
fi
