#!/bin/bash

source helpers/load_config.sh

LOG_PATH=$(config "local" "log_path")

# Append the current date and time to the log file name
LOGFILE="${LOG_PATH}$(date +'%Y-%m-%d_%H-%M').log"

# Ensure the directory for the log file exists
LOG_DIR=$(dirname "$LOGFILE")
if [[ ! -d "$LOG_DIR" ]]; then
    mkdir -p "$LOG_DIR" || { echo "Error: Unable to create log directory '$LOG_DIR'."; exit 1; }
fi

if [[ ! -w "$LOG_DIR" ]]; then
    echo "Warning: Log directory '$LOG_DIR' is not writable. Logging to file will not work."
fi

# Define color codes
PURPLE="\033[95m"
BLUE="\033[94m"
CYAN="\033[96m"
GREEN="\033[92m"
YELLOW="\033[93m"
RED="\033[91m"
ENDC="\033[0m"
BOLD="\033[1m"
UNDERLINE="\033[4m"

# Log to file
log_write_file() {
    local message=$1
    local time=$(date +"%Y/%m/%d %H:%M:%S")
    echo "${time}: ${message}" >> "$LOGFILE" 2>/dev/null || \
    echo "Warning: Unable to write to log file '$LOGFILE'."
}

# Logging functions
log() {
    local message=$1
    echo -e "${PURPLE}${message}${ENDC}"
    log_write_file "$message"
}

debug() {
    echo -e "${CYAN}${message}${ENDC}"
    log_write_file "$message"
}

warning() {
    local message=$1
    echo -e "${YELLOW}${message}${ENDC}"
    log_write_file "$message"
}

error() {
    local message=$1
    echo -e "${RED}${message}${ENDC}" >&2
    log_write_file "$message"
}

success() {
    local message=$1
    echo -e "${GREEN}${message}${ENDC}"
    log_write_file "$message"
}

run_command() {
    local cmd=$1
    debug "Executing command: $cmd"
    eval "$cmd"
    local status=$?
    if [[ $status -ne 0 ]]; then
        error "Command failed with status $status: $cmd"
    fi
    return $status
}
