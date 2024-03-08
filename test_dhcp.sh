#!/bin/bash
# Auteur: Djetic Alexandre
# Date: 16/02/2023
# Modifié: 16/02/2023
# Description: Ce script teste le serveur DHCP

if [ "$EUID" -ne 0 ]; then
    echo "Requiert un accès en tant que sudo/root"
    exit 1
fi

function get_current_ip {
    TMP_IP=$(ip a show "$INT" | grep "inet[^6]" | awk '{print $2}')

    if [ ! -z "$TMP_IP" ]; then
        echo "Adresse IP actuelle: $TMP_IP"
    else
        echo "Adresse IP actuelle: aucune"
    fi
}

# Variable d'environnement
INT="$1"
TMP_IP=$(ip a show "$INT" | grep "inet[^6]" | awk '{print $2}')
FILE_LOG="test_dhcp.log"

# Adresse IP actuelle
get_current_ip

# Suppression de l'adresse IP actuelle
echo "Suppression de l'adresse IP actuelle: $TMP_IP"
dhclient -r "$INT" > /dev/null
get_current_ip

# Changement vers une IP temporaire
dhclient -i "$INT" > /dev/null

# Exécution du client DHCP (udhcpc)
if [ $? -eq 0 ]; then
    echo "Obtention d'une IP à l'aide du serveur DHCP : OK"
    get_current_ip
else
    echo "Obtention d'une IP à l'aide du serveur DHCP : NOK"
    get_current_ip
fi

# Détermination de la nouvelle IP
get_current_ip
