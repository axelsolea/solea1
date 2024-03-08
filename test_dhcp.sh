#!/bin/bash
# Author: Djetic Alexandre
# Date: 16/02/2023
# Modified: 16/02/2023
# Description: This script test the DHCP server

if [ ! $EUID -eq 0 ]; then
	echo "require sudo/root access"
	exit 1
fi

#env var
FILE_LOG="dhcp_client.log"

dhclient -r > "$FILE_LOG"
dhclient -i ens160 >> "$FILE_LOG"

if [ $? -eq 0 ]; then
	echo "dhcp OK"
else
	echo "dhcp NOK"
fi
