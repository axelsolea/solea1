#!/bin/sh
# Author: Djetic Alexandre
# Date: 16/02/2024
# Modified: 16/03/2024

ping -c 3 8.8.8.8 >> test_internet.log

if [ $? -eq 0 ]; then
	echo "internet access OK"
else
	echo "internet access NOK"
fi
