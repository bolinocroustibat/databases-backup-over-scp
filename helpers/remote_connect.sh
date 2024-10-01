#!/bin/bash

# Source the logger functions
source helpers/logger.sh

# Function to read .ini file
read_ini_file() {
    local file=$1
    local section=$2
    local key=$3
    awk -F '=' -v section="$section" -v key="$key" '
    $0 ~ "\\["section"\\]" { in_section=1 }
    in_section && $1 ~ key { gsub(/^[ \t]+|[ \t]+$/, "", $2); print $2; exit }
    $0 ~ /^\[/ && !($0 ~ "\\["section"\\]") { in_section=0 }
    ' "$file"
}

# Load settings from settings.ini
REMOTE_HOST=$(read_ini_file settings.ini remote host)
REMOTE_PATH=$(read_ini_file settings.ini remote path)
REMOTE_USER=$(read_ini_file settings.ini remote user)

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
