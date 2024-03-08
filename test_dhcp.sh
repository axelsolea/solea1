#!/bin/bash
# Author: Djetic Alexandre
# Date: 16/02/2023
# Modified: 16/02/2023
# Description: This script test the DHCP server

if [ ! $EUID -eq 0 ]; then
	echo "require sudo/root access"
	exit 1
fi

dhclient -r > dhcp_client.log
dhclient -i ens160 >> dhcp_client.log

if [ $? -eq 0 ]; then
	echo "dhcp OK"
else
	echo "dhcp NOK"
fi
