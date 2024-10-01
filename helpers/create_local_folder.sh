#!/bin/bash

source helpers/load_config.sh
source helpers/logger.sh

POSTGRES_SYSTEM_USER=$(config "postgres" "system_user")
LOCAL_PATH=$(config "local" "path")

create_local_folder() {
    local now=$(date -u +"%Y-%m-%d_%H-%M")
    local local_path="${LOCAL_PATH}${now}"

    if id "$POSTGRES_SYSTEM_USER" &>/dev/null; then
        # If we have a PostgreSQL system user, we create the folder as owned by it
        # so it can also be writable by the PostgreSQL script using the same folder
        cmd="su - $POSTGRES_SYSTEM_USER -c \"mkdir -p $local_path\""
    else
        warning "PostgreSQL system user '${POSTGRES_SYSTEM_USER}' does not exist. Creating folder as current user."
        cmd="mkdir -p $local_path"
    fi

    eval $cmd
    local status=$?

    if [[ $status -ne 0 ]]; then
        error "Error while creating local backup folder: $status"
        return 1
    else
        success "Local backup folder '$local_path' created."
        echo "$local_path"
        return 0
    fi
}
