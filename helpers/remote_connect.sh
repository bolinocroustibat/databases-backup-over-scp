#!/bin/bash

source helpers/load_config.sh
source helpers/logger.sh

# Load settings from settings.ini
REMOTE_HOST=$(config "remote" "host")
REMOTE_PATH=$(config "remote" "path")
REMOTE_USER=$(config "remote" "user")

# Function to connect to remote server and create backup folder
remote_connect() {
    local now=$(date -u +"%Y-%m-%d_%H-%M")
    local remote_path="${REMOTE_PATH}${now}"

    # Connect to backup server
    ssh -o BatchMode=yes -o ConnectTimeout=10 "$REMOTE_USER@$REMOTE_HOST" "mkdir -p $remote_path"
    local status=$?

    if [[ $status -ne 0 ]]; then
        error "Error while connecting to remote '$REMOTE_HOST' or creating folder: $status"
        return 1
    else
        success "Remote backup folder $remote_path created on '$REMOTE_HOST'"
        echo "$remote_path"
        return 0
    fi
}
