#!/bin/bash
#Author : Axel CHALVIN
#Creation date : 08/03/2024
#Last edit : 05/04/2024

function test_ping {
  # $1 : name or IP
  #
  # couleur
  RED="\e[31m"
  NOCOLOR="\e[0m"
  GREEN="\033[0;32m"

  # récupération des valeurs
  value=$(ping -c 1 "$1" | grep "ping statistics" -A 1) 
  echo "$value" >> test_internet_v2.log
  return_value=$(echo "$value" | awk 'NR==2 {print $6}')
  
  echo "$return_value"

  echo "nom: ${RED}$1${NOCOLOR}"
  if [[ "$return_value" == "0%" ]];then
    echo -e "connexion: \n${GREEN}OK ✓{NOCOLOR}"
  else
    echo -e "connexion: \n${RED}NOK ✘{NOCOLOR}" 
  fi
}

echo "Script lancé"
echo "Script started : $(date)" > test_internet_v2.log

test_ping "google.com"
test_ping "172.18.0.254"
test_ping "172.21.255.254"
test_ping "172.22.255.254"
test_ping "172.23.255.254"
test_ping "172.24.255.254"
test_ping "172.26.255.254"
test_ping "172.28.255.254"
test_ping "172.29.255.254"
test_ping "172.30.255.254"

echo "Fin d'execution du script $(date)" >> test_internet_v2.log

echo "Afficher les logs? (y/n)"

read ans

if [ "$ans" = "y" ];then 
  cat test_internet_v2.log
fi
 
