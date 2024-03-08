#!/bin/bash
# Author: CHOLLET Emeline
# Date: 16/02/2024
# Modified: 08/03/2024
# Description: Test inter vlan inter site 
# piste d'amelioration : mettre le nom du vlan dans une variable et afficher la variable 

set -u

# cette fonction log un chemin prit par un paquet
function log_chemin {
  # $1: chemin de router
  # $2: ip de gw
  # $3: fichier de log

  if [ ! -z "$1" ]; then
    echo "chemin utilisé pour ${2}: ${1}" >> "$3"
    echo "${2} OK, le ping passe" >> "$3"
  else
    echo "aucun chemin trouvé pour ${2}" >> "$3"
  fi
}

#env var
LIST_IP="list_ip.txt"
FILE_LOG="test_init_vlan_site.log"
CPT=0
CPT_FINALE=$(cat "$LIST_IP" | wc -l) #compte nombre de ligne

#### TEST vlan aix IPv4/IPv6####
echo "---------------- debut vlan solea ----------------" > "$FILE_LOG"

for ip in $(cat "$LIST_IP")
do
  ping -c 2 "$ip" > /dev/null
  
  if [ $? -eq 0 ]; then
    CPT=$((CPT+1))
    echo "=> ${ip} OK, le ping réussit avec succès" >> "$FILE_LOG"
  else
    echo "=> ${ip} NOK, le ping vient d'échouer" >> "$FILE_LOG"
  fi
done

echo "---------------- fin test vlan solea ----------------" >> "$FILE_LOG"

#### TEST traceroute inter-site ####
echo "---------------- debut traceroute solea ----------------" >> "$FILE_LOG"
GW_IP_VALENCE_PC="172.26.255.254"
GW_IP_VALENCE_TEL="172.29.255.254"

# obtention des chemins des paquets
PATH_VAL_PC_GW=$(traceroute "$GW_IP_VALENCE_PC" | awk 'NR==2 {print $2,$3}')
PATH_VAL_TEL_GW=$(traceroute "$GW_IP_VALENCE_TEL" | awk 'NR==2 {print $2,$3}')

# log des chemins
log_chemin "$PATH_VAL_PC_GW" "$GW_IP_VALENCE_PC" "$FILE_LOG"
log_chemin "$PATH_VAL_TEL_GW" "$GW_IP_VALENCE_TEL" "$FILE_LOG"

echo "---------------- fin traceroute solea ----------------" >> "$FILE_LOG"

#check que tout les ping sont passés
if [ "$CPT" -eq "$CPT_FINALE" ]; then
  echo "tout les ping ont fonctionné avec succès" 
else
  echo "tout les ping n'ont pas fonctionné"
fi
