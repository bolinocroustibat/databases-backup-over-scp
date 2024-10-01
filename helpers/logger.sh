#!/bin/bash

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

# Log file path
LOGFILE="logfile.log"

# Function to write log to file with timestamp
log_write_file() {
    local message=$1
    local time=$(date +"%m/%d %H:%M:%S/%3N")
    echo "${time}: ${message}" >> "$LOGFILE"
}

# Function to log message with color
log() {
    local message=$1
    echo -e "${PURPLE}${message}${ENDC}"
    log_write_file "$message"
}

# Function to log debug message with color
debug() {
    local message=$1
    echo -e "${CYAN}${message}${ENDC}"
    log_write_file "$message"
}

# Function to log warning message with color
warning() {
    local message=$1
    echo -e "${YELLOW}${message}${ENDC}"
    log_write_file "$message"
}

# Function to log error message with color
error() {
    local message=$1
    echo -e "${RED}${message}${ENDC}"
    log_write_file "$message"
}

# Function to log success message with color
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
