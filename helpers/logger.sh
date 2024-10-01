#!/bin/bash

source helpers/load_config.sh

BASE_LOGFILE=$(config "local" "logfile")

# Append the current date and time to the log file name
LOGFILE="${BASE_LOGFILE}_$(date +'%Y-%m-%d_%H-%M').log"

# Ensure the directory for the log file exists
LOG_DIR=$(dirname "$LOGFILE")
mkdir -p "$LOG_DIR"

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

log_write_file() {
    local message=$1
    local time=$(date +"%m/%d %H:%M:%S/%3N")
    echo "${time}: ${message}" >> "$LOGFILE"
}

log() {
    local message=$1
    echo -e "${PURPLE}${message}${ENDC}"
    log_write_file "$message"
}

debug() {
    local message=$1
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
    echo -e "${RED}${message}${ENDC}"
    log_write_file "$message"
}

success() {
    local message=$1
    echo -e "${GREEN}${message}${ENDC}"
    log_write_file "$message"
}

# Function to close log file (not needed in bash, but included for completeness)
close() {
    # No action needed in bash to close the file
    :
}
