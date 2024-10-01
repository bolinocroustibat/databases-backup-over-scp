#!/bin/bash

config() {
    local section=$1
    local key=$2
    yq eval ".${section}.${key}" "config.yaml"
}
