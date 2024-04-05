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
    TMP_IP_V4=$(ip a show "$INT" | grep "inet[^6]" | awk '{print $2}')
    TMP_IP_V6=$(ip a show "$INT" | grep "inet[^4]" | awk 'NR==1 {print $2}')

    if [ ! -z "$TMP_IP_V4" ] || [ ! -z "$TMP_IP_V6" ]; then
        echo "Adresse IP actuelle (V4): $TMP_IP_V4"
        echo "Adresse IP actuelle (V6): $TMP_IP_V6"
    else
        echo "Adresse IP actuelle: aucune"
    fi
}

# Variable d'environnement
INT="$1"
FILE_LOG="test_dhcp.log"

# Adresse IP actuelle
get_current_ip

# Suppression de l'adresse IP actuelle
echo "Suppression de l'adresse IP actuelle:"
echo "$TMP_IP_V4"
echo "$TMP_IP_V6"

dhclient -r "$INT" > /dev/null
get_current_ip

# Changement vers une IP temporaire
dhclient -i "$INT" > /dev/null

# Exécution du client DHCP (udhcpc)
if [ $? -eq 0 ]; then
    echo "Obtention d'une adresse IPv4 et IPv6 à l'aide du serveur DHCP : OK"
    get_current_ip # Détermination de la nouvelle IP
else
    echo "Obtention d'une adresse IPv4 et IPv6 à l'aide du serveur DHCP : NOK"
    get_current_ip # Détermination de la nouvelle IP
fi
