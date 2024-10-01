#!/bin/bash

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
