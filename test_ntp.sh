#!/bin/sh
# Author: Djetic Alexandre
# Date: 05/04/2024
# Modified: 05/04/2024
# Description: This script test that all server is sync NTP

##############################################################################################
# Ce script va acceder en ssh entre chaque serveur et vérifier que le serveur est synchronisé
# Il obtient le status, date et heure du serveur
##############################################################################################

# couleur
RED="\e[31m"
NOCOLOR="\e[0m"
GREEN="\033[0;32m"

# env var
FILE_SERVER="$1"

for server in $(< "FILE_SERVER")
do
  timectl_return=$(ssh axel@${server} "timedatectl")
  active_state=$(${timectl_return} | grep "NTP" | awk '{print $3}')
  current_date=$(${timectl_return} | grep "Local time" | awk '{print $4}')
  hour=$(${timectl_return} | grep "Local time" | awk '{print $5}')
  
  # affichage des informations
  echo "---------------------------------------------"
  echo -e "nom du server: ${RED}$server${NOCOLOR}"
  echo -e "status: ${GREEN}$active_state${NOCOLOR}"
  echo "date: $current_date"
  echo -e "heure: ${GREEN}$hour${NOCOLOR}"
  echo -e "---------------------------------------------\n"
done
