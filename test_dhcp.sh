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
    TMP_IP_V4=$(ip -4 addr show "$INT" | grep -oP '(?<=inet\s)\d+(\.\d+){3}')
    TMP_IP_V6=$(ip -6 addr show "$INT" | grep -oP '(?<=inet6\s)[\da-fA-F:]+')

    if [ ! -z "$TMP_IP_V4" ] || [ ! -z "$TMP_IP_V6" ]; then
        echo "Adresse IP actuelle (V4): $TMP_IP_V4"
        echo "Adresse IP actuelle (V6): $TMP_IP_V6"
    else
        echo "Adresse IP actuelle: aucune"
    fi
}

# Variable d'environnement
INT="ens160"

# Adresse IP actuelle
get_current_ip

# Suppression de l'adresse IP actuelle
echo "Suppression de l'adresse IP actuelle:"
dhclient -r "$INT" > /dev/null 2>> /dev/null
ip addr flush dev "$INT" > /dev/null
get_current_ip

# Changement vers une IP temporaire
dhclient -v "$INT" > /dev/null 2>> /dev/null

# Exécution du client DHCP (udhcpc)
if [ $? -eq 0 ]; then
    echo "Obtention d'une adresse IPv4 et IPv6 à l'aide du serveur DHCP : OK"
    get_current_ip # Détermination de la nouvelle IP
else
    echo "Obtention d'une adresse IPv4 et IPv6 à l'aide du serveur DHCP : NOK"
    get_current_ip # Détermination de la nouvelle IP
fi
