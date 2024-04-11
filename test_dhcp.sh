#!/bin/bash
# Auteur: Djetic Alexandre
# Date: 16/02/2023
# Modifié: 05/04/2023
# Description: Ce script teste le serveur DHCP

############################################################################################################################
# Ce script teste l'obtention d'adresses IPv4 et IPv6 en réalisant une requête au serveur DHCP.
# - Dans un premier temps, il affiche les adresses actuelles.
# - Dans un second temps, il supprime les adresses IP actuelles et les affiche pour s'assurer qu'aucune adresse IP ne reste.
# - Enfin, il réalise une nouvelle demande d'adresses IP et les affiche.
############################################################################################################################

# couleur
RED="\e[31m"
NOCOLOR="\e[0m"
GREEN="\033[0;32m"

if [ "$EUID" -ne 0 ]; then
    echo "Requiert un accès en tant que sudo/root"
    exit 1
fi

function get_current_ip {
  TMP_IP_V4=$(ip -4 addr show "$INT" | grep -oP '(?<=inet\s)\d+(\.\d+){3}')
  TMP_IP_V6=$(ip -6 addr show "$INT" | grep -oP '(?<=inet6\s)[\da-fA-F:]+')

  # Exclure les adresses IPv6 de lien local (fe80::)
  TMP_IP_V6_FILTERED=$(echo "$TMP_IP_V6" | grep -v '^fe80')

  if [ ! -z "$TMP_IP_V4" ] || [ ! -z "$TMP_IP_V6_FILTERED" ]; then
    echo -e "Adresse IP actuelle (V4): ${GREEN}$TMP_IP_V4${NOCOLOR}"
    if [ ! -z "$TMP_IP_V6_FILTERED" ]; then
      echo -e "Adresse IP actuelle (V6): ${GREEN}$TMP_IP_V6_FILTERED${NOCOLOR}"
    else
      echo "Adresse IP actuelle (V6): Aucune"
    fi
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
dhclient -r -v "$INT" > /dev/null 2>> /dev/null
ip addr flush dev "$INT" > /dev/null
get_current_ip

# Changement vers une IP temporaire
dhclient -4 -v -i "$INT" > /dev/null 2>> /dev/null
dhclient -6 -v -i "$INT" > /dev/null 2>> /dev/null

# Exécution du client DHCP (udhcpc)
if [ $? -eq 0 ]; then
    echo "Obtention d'une adresse IPv4 et IPv6 à l'aide du serveur DHCP : OK"
    get_current_ip # Détermination de la nouvelle IP
else
    echo "Obtention d'une adresse IPv4 et IPv6 à l'aide du serveur DHCP : NOK"
    get_current_ip # Détermination de la nouvelle IP
fi
