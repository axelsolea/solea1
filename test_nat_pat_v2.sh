#!/bin/env bash
#Author : Axel CHALVIN
#Creation date : 08/03/2024
#Last edit : 08/03/2024

PORTS="22200 22202 22253 22252 22004"
SCRIPT="hostname"
for PORT in ${PORTS} ; do
    sshpass -p Solea05axel ssh axel@192.168.141.2 -p ${PORT} "${SCRIPT}"
done
