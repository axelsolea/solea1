#!/bin/bash
# Auteur : Axel CHALVIN
# Date de création : 08/03/2024
# Dernière modification : 05/04/2024

##########################################################################
# Ce script permet de tester la connectivité de chaque équipement réseau
# de l'entreprise SOLEA en utilisant la commande ping, et vérifie
# qu'il n'y a pas de perte de paquets différente de 0%.
##########################################################################


function test_ping {
  # $1 : nom ou IP

  # couleurs
  ROUGE="\e[31m"
  AUCUNE_COULEUR="\e[0m"
  VERT="\033[0;32m"

  # récupération des valeurs
  valeur=$(ping -c 1 "$1" | grep "ping statistics" -A 1) 
  echo "$valeur" >> test_internet_v2.log
  valeur_retour=$(echo "$valeur" | awk 'NR==2 {print $6}')
  
  echo -e "Nom : ${ROUGE}${1}${AUCUNE_COULEUR}"
  if [[ "$valeur_retour" == "0%" ]];then
    echo -e "- Connexion : ${VERT}OK ✓${AUCUNE_COULEUR}"
  else
    echo -e "- Connexion : ${ROUGE}NOK ✘${AUCUNE_COULEUR}" 
  fi
}

echo "Lancement du script"
echo "Début du script : $(date)" > test_internet_v2.log

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

echo "Fin du script $(date)" >> test_internet_v2.log

echo "Afficher les logs ? (o/n)"

read reponse

if [ "$reponse" = "o" ];then 
  cat test_internet_v2.log
fi
