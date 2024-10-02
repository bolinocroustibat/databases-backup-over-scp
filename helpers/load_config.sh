#!/bin/bash

install_yq() {
    echo "yq not found. Installing..."

    # Check the OS type and install yq accordingly
    if command -v apt &> /dev/null; then
        sudo apt update && sudo apt install -y yq
    elif command -v brew &> /dev/null; then
        brew install yq
    elif command -v dnf &> /dev/null; then
        sudo dnf install -y yq
    elif command -v pacman &> /dev/null; then
        sudo pacman -S --noconfirm yq
    else
        echo "Error: Package manager not supported. Please install yq manually."
        return 1
    fi

    echo "yq installed successfully."
}

config() {
    local section="$1"
    local key="$2"

    # Check for yq and install if not found
    if ! command -v yq &> /dev/null; then
        install_yq || return 1
    fi

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
