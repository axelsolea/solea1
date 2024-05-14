#!/bin/bash
# Author: Djetic Alexandre
# Date: 14/05/2024
# Modified: 14/05/2024
# Description: this script install all requirement for the script save_tftp.py

if [ $EUID -ne 0 ]; then
  echo "require sudo/root access"
  exit 1
fi

echo "install requirement: python3 python3-pip tftp"
apt install python3 python3-pip tftp -y
