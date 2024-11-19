# Function to check if a command is available for a specific user
# Arguments:
#   $1 - The command to check (e.g., "pg_dump")
#   $2 - (Optional) The username to check the command for (e.g., "postgres")
# Returns:
#   0 if the command is found, 1 if not found
#   Logs the status for success or failure.
check_dependency() {
    local cmd="$1"
    local user="$2"  # Optional: specify the user to check the command for

    if [[ -n "$user" ]]; then
        debug "Checking if command '$cmd' is available for user '$user'..."
        
        # Check if the command is available for the specified user using sudo
        if ! sudo -u "$user" command -v "$cmd" &>/dev/null; then
            debug "Command '$cmd' not found for user '$user'."
            return 1
        fi
    else
        # Otherwise, check for the command in the current user's environment
        if ! command -v "$cmd" &>/dev/null; then
            return 1
        fi
    fi

    return 0  # Command found
}
