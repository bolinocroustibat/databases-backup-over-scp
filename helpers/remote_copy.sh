#!/bin/bash

source helpers/load_config.sh
source helpers/logger.sh

REMOTE_HOST=$(config "remote" "host")

remote_copy() {
    local local_path=$1
    local db_filename=$2

    if [[ -n "$REMOTE_HOST" ]]; then
        if [[ -z "$ssh_client" && -z "$remote_path" ]]; then
            remote_connect_result=$(remote_connect)
            ssh_client=$(echo "$remote_connect_result" | head -n 1)
            remote_path=$(echo "$remote_connect_result" | tail -n 1)
        fi
        if [[ -n "$ssh_client" && -n "$remote_path" ]]; then
            # Perform the SCP copy
            scp "${local_path}/${db_filename}" "${ssh_client}:${remote_path}/${db_filename}"
            local status=$?

            if [[ $status -ne 0 ]]; then
                error "Error while copying '${db_filename}' on '${ssh_client}': $status"
                return 1
            else
                success "Backup file '${db_filename}' has been copied on '${ssh_client}'"
                return 0
            fi
        else
            error "Couldn't copy on server, couldn't get SSH connection."
            return 1
        fi
    fi
}
