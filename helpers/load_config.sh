#!/bin/bash

config() {
    local section="$1"
    local key="$2"

    # Validate inputs
    if [[ -z "$section" || -z "$key" ]]; then
        echo "Usage: config <section> <key>"
        return 1
    fi

    # Fetch the value and check its type
    local value
    value=$(yq eval ".${section}.${key}" "config.yaml" 2>/dev/null)

    if [[ $? -ne 0 ]]; then
        echo "Error: Could not read from config.yaml"
        return 1
    fi

    local value_type
    value_type=$(yq eval ".${section}.${key} | type" "config.yaml" 2>/dev/null)

    if [[ $value_type == "!!seq" ]]; then
        # Return the list items
        echo "$value" | yq eval '.[]' - 
    else
        # Return the scalar value
        echo "$value"
    fi
}
