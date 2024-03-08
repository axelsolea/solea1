#!/bin/bash
# Author: Djetic Alexandre
# Date: 16/02/2023
# Modified: 16/02/2023
# Description: This script tests the DHCP server

if [ "$EUID" -ne 0 ]; then
    echo "Require sudo/root access"
    exit 1
fi

INT="$1"
TMP_IP=$(ip a show "$INT" | grep "inet[^6]" | awk '{print $2}')

# Current IP address
echo "Adresse IP actuelle: $TMP_IP"

# Changing to a temporary IP
ip a del "$TMP_IP" dev "$INT"
ip a add 199.199.199.199/32 dev "$INT"
TMP_IP=$(ip a show "$INT" | grep "inet[^6]" | awk '{print $2}')
echo "Nouvelle IP statique actuelle avant DHCP: $TMP_IP"

# Stop any existing udhcpc
killall -q udhcpc

# Running DHCP client (udhcpc)
if udhcpc -i "$INT" -s /usr/share/udhcpc/default.script -b -q; then
    echo "obtention d'une IP à l'aide du serveur DHCP : OK"
else
    echo "obtention d'une IP à l'aide du serveur DHCP : NOK"
fi

# Determining the new IP
TMP_IP=$(ip a show "$INT" | grep "inet[^6]" | awk '{print $2}')
echo "Nouvelle IP dynamique actuelle après DHCP: $TMP_IP"
