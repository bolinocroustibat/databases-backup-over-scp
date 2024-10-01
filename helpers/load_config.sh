#!/bin/bash

config() {
    local section=$1
    local key=$2
    local value_type=$(yq eval ".${section}.${key} | type" "config.yaml")

    if [[ $value_type == "!!seq" ]]; then
        # Return the list items
        yq eval ".${section}.${key} | .[]" "config.yaml"
    else
        # Return the scalar value
        yq eval ".${section}.${key}" "config.yaml"
    fi
}
