#!/bin/env bash
#Author : Axel CHALVIN
#Creation date : 08/03/2024
#Last edit : 08/03/2024

echo "Lancement du script..."

PORTS="22202 22253 22004 22200"
SCRIPT="echo 'Nom de la machine : '; hostname"
for PORT in ${PORTS} ; do
    echo "Accès SSH via l'ip publique (192.168.141.2) sur le port ${PORT}"  
    sshpass -p Solea05axel ssh axel@192.168.141.2 -p ${PORT} "${SCRIPT}"
    echo ""
done

echo "Arrêt du script..."
