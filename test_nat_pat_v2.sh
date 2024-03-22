#!/bin/env bash
#Author : Axel CHALVIN
#Creation date : 08/03/2024
#Last edit : 08/03/2024

echo "Lancement du script..."

PORTS="22202 22253 22200 22004"
SCRIPT="echo 'Nom de la machine : '; hostname"

for PORT in ${PORTS}; do
    echo "Accès SSH via l'ip publique (192.168.141.2) sur le port ${PORT}"  
    sshpass -p "Solea05axel" ssh axel@192.168.141.2 -p ${PORT} "${SCRIPT}"
    echo ""
done

for PORT in ${PORTS}; do
    echo "Accès SSH via l'ip publique (192.168.141.2) sur le port ${PORT}"  
    sshpass -p "Solea05alexandre" ssh alexandre@192.168.141.2 -p ${PORT} "${SCRIPT}"
    echo ""
done

echo "Accès SSH via l'ip publique sur le port 22252"  
echo "Accès SSH via l'ip publique (192.168.141.2) sur le port 22252"  
echo 'Nom de la machine : '
sshpass -p " " ssh admin-solea@192.168.141.2 -p 22252 "hostname"
echo ""

echo "Arrêt du script..."
