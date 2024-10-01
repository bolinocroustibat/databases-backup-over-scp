#!/bin/bash

# Load read_ini_file function
source helpers/read_ini_file.sh
# Load settings
source settings.ini
# Source the logger functions
source helpers/logger.sh

# Load settings from settings.ini
POSTGRES_SYSTEM_USER=$(read_ini_file settings.ini postgres system_user)
LOCAL_PATH=$(read_ini_file settings.ini local path)


# Function to create local backup folder
create_local_folder() {
    local now=$(date -u +"%Y-%m-%d_%H-%M")
    local local_path="${LOCAL_PATH}${now}"

    if [[ -n "$POSTGRES_SYSTEM_USER" ]]; then
        # If we have a PostgreSQL system user, we create the folder as owned by it
        # so it can also be writable by the PostgreSQL script using the same folder
        cmd="su - $POSTGRES_SYSTEM_USER -c \"mkdir -p $local_path\""
    else
        cmd="mkdir -p $local_path"
    fi

    eval $cmd
    local status=$?

    if [[ $status -ne 0 ]]; then
        error "Error while creating local backup folder: $status"
        return 1
    else
        success "Local backup folder $local_path created."
        echo "$local_path"
        return 0
    fi
}

# Example usage
create_local_folder
