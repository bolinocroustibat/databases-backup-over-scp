#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status
set -o pipefail  # Catch errors in piped commands

source helpers/check_deps.sh
source helpers/load_config.sh
source helpers/logger.sh

# Setup interrupt handling
trap 'echo "Interrupt signal received. Exiting..."; exit 1' SIGINT

MYSQL_USER=$(config "mysql" "user")
MYSQL_USER_PASSWORD=$(config "mysql" "user_password")

POSTGRES_PASSWD=$(config "postgres" "password")
POSTGRES_PORT=$(config "postgres" "port")
POSTGRES_SYSTEM_USER=$(config "postgres" "system_user")

LOCAL_PATH=$(config "local" "path")

REMOTE_HOST=$(config "remote" "host")
REMOTE_USER=$(config "remote" "user")
REMOTE_PATH=$(config "remote" "path")

now=$(date -u +"%Y-%m-%d_%H-%M")

remote_copy() {
    local local_path=$1
    local db_filename=$2

    if [[ -n "$REMOTE_HOST" ]]; then
        # Connect to the remote server and create the backup folder
        remote_path="${REMOTE_PATH}${now}"
        timeout 30 ssh -o BatchMode=yes -o ConnectTimeout=10 "$REMOTE_USER@$REMOTE_HOST" "mkdir -p $remote_path"
        local status=$?

        if [[ $status -ne 0 ]]; then
            error "Error while connecting to remote '$REMOTE_HOST' or creating folder: $status"
            return 1
        else
            success "Remote backup folder $remote_path created on '$REMOTE_HOST'."
        fi

        # Perform the SCP copy with a timeout
        timeout 60 scp "${local_path}/${db_filename}" "${REMOTE_USER}@${REMOTE_HOST}:${remote_path}/${db_filename}"
        status=$?

        if [[ $status -ne 0 ]]; then
            error "Error while copying '${db_filename}' to '${REMOTE_HOST}': $status"
            return 1
        else
            success "Backup file '${db_filename}' has been copied to '${REMOTE_HOST}'"
            return 0
        fi
    fi
}

# Add debug logs
log "Starting backup process..."

# Create local backup folder
local_path="${LOCAL_PATH}${now}"
debug "Creating local backup folder '$local_path'..."
if id "$POSTGRES_SYSTEM_USER" &>/dev/null; then
    su - "$POSTGRES_SYSTEM_USER" -c "mkdir -p '$local_path'" || {
        error "Error while creating local backup folder as PostgreSQL user."
        return 1
    }
else
    warning "PostgreSQL system user '${POSTGRES_SYSTEM_USER}' does not exist. Creating folder as current user."
    mkdir -p "$local_path" || {
        error "Error while creating local backup folder as current user."
        return 1
    }
fi
success "Local backup folder '$local_path' created."

# MySQL backup
if check_dependency "mysqldump"; then
    log "mysqldump command found. Starting MySQL backups..."
    mysql_dbs=$(config "mysql" "db_names")
    debug "mysql_dbs=${mysql_dbs}"
    for db in $mysql_dbs; do
        db_filename="${db}.sql.gz"
        dump_cmd="mysqldump --user=${MYSQL_USER} --password=${MYSQL_USER_PASSWORD} ${db} | gzip -9 -c > ${local_path}/${db_filename}"
        if eval "$dump_cmd"; then
            success "MySQL backup file '${local_path}/${db_filename}' has been saved locally."
            remote_copy "$local_path" "$db_filename"
        else
            error "Error while trying to dump the MySQL database '${db}' locally."
        fi
    done
else
    warning "mysqldump command not found, MySQL backups skipped."
fi

# PostgreSQL backup
if check_dependency "pg_dump" "$POSTGRES_SYSTEM_USER"; then
    log "pg_dump command found for PostgreSQL system user '${POSTGRES_SYSTEM_USER}'"

    if id "$POSTGRES_SYSTEM_USER" &>/dev/null; then
        log "Starting PostgreSQL backups..."
        postgres_dbs=$(config "postgres" "db_names")
        debug "postgres_dbs=${postgres_dbs}"
        for db in $postgres_dbs; do
            db_filename="${db}.dump"  # Define the db_filename for PostgreSQL dump files
            dump_cmd="sudo -u ${POSTGRES_SYSTEM_USER} PGPASSWORD='${POSTGRES_PASSWD}' pg_dump ${db} -Fc -U ${POSTGRES_SYSTEM_USER} -p ${POSTGRES_PORT} > ${local_path}/${db_filename}"
            if eval "$dump_cmd"; then
                success "PostgreSQL backup dump file '${local_path}/${db_filename}' has been saved locally."
                remote_copy "$local_path" "$db_filename"
            else
                error "Error while trying to dump the PostgreSQL database '${db}' locally."
            fi
        done
    else
        error "PostgreSQL system user '${POSTGRES_SYSTEM_USER}' does not exist. Skipping PostgreSQL backups."
    fi
else
    warning "pg_dump command not found, PostgreSQL backups skipped."
fi

success "Backup process completed."
