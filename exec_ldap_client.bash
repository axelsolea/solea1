#!/bin/sh
# Author: Djetic Alexandre
# Date: 02/02/2024
# Modified: 02/02/2024
# Description: this script setup a LDAP client on debian base distro

if [ $# -ne 2 ]; then
  echo "Usage: $0 <user> <machineip>"
  exit 1
fi

#copy file to remote server
scp ldap-client-setup.sh $1@$2:~

# Connect to the remote machine and execute the script
ssh $1@$2 -S "sudo -E ./ldap-client-setup.sh"
