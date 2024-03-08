#!/bin/env bash
#Author : Axel CHALVIN
#Creation date : 08/03/2024
#Last edit : 08/03/2024

PORTS="22202 22253"
SCRIPT="echo 'Nom de la machine : '; hostname"
for PORT in ${PORTS} ; do
    echo "Accès SSH via l'ip publique sur le port ${PORT}"  
    sshpass -p Solea05axel ssh axel@192.168.141.2 -p ${PORT} "${SCRIPT}"
    echo ""
done

echo "Accès SSH via l'ip publique sur le port 22200"  
echo 'Nom de la machine : '
sshpass -p Solea05dns ssh admin-solea@192.168.141.2 -p 22200 "hostname"
echo ""

echo "Accès SSH via l'ip publique sur le port 22252"  
echo 'Nom de la machine : '
sshpass -p " " ssh admin-solea@192.168.141.2 -p 22252 "hostname"

echo "Accès SSH via l'ip publique sur le port 22004"  
echo "ignoré tant que le serveur toip.solea.local a une adresse sur le VLAN 140"
#echo 'Nom de la machine : '
#sshpass -p " " ssh admin-solea@192.168.141.2 -p 22004 "hostname"
