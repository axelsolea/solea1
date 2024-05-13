#!/bin/bash
# Author: Djetic Alexandre 
# Date: 13/05/2024
# Modified: 13/05/2024
# Description: This script makes a backup of named/bind conf files 

# Usage: ./backup_named_conf.sh <TFTP_SERVER_IP> <CONFIG_FILE>

# Check if TFTP server IP and config file are provided
if [ $# -ne 2 ]; then
    echo "Usage: $0 <TFTP_SERVER_IP> <CONFIG_FILE>"
    exit 1
fi

# env
server="$1"
config_file="$2"

# Iterate over each line in the config file
while IFS= read -r line; do
    src=$(echo "$line" | sed 's/:/ /' | awk '{print $1}')
    dst=$(echo "$line" | sed 's/:/ /' | awk '{print $2}')

    # Transfer the BIND configuration file to TFTP server
    echo "put $src $dst" | tftp "$server"
done < "$config_file"
