#!/bin/bash
# Auteur: Alexandre Djetic
# Date: 05/04/2024
# Modifié: 05/04/2024
# Description: Ce script vérifie que tous les serveurs sont synchronisés via NTP

##############################################################################################
# Ce script se connecte en ssh à chaque serveur et vérifie s'il est synchronisé
# Il obtient le statut, la date et l'heure du serveur
##############################################################################################

# Couleurs
ROUGE="\e[31m"
SANS_COULEUR="\e[0m"
VERT="\033[0;32m"

# Variables d'environnement
FICHIER_SERVEUR="$1"

echo -e "---------- ${ROUGE}test NTP${SANS_COULEUR} ----------\n"

for serveur in $(cat "$FICHIER_SERVEUR")
do
  #obtient les informations
  resultat_timectl=$(ssh axel@$serveur "timedatectl")
  etat_actif=$(echo "$resultat_timectl" | grep "NTP" | awk '{print $3}')
  date_actuelle=$(echo "$resultat_timectl" | grep "Local time" | awk '{print $4}')
  heure=$(echo "$resultat_timectl" | grep "Local time" | awk '{print $5}')
  
  # Affichage des informations
  echo "---------------------------------------------"
  echo -e "Nom du serveur: ${ROUGE}$serveur${SANS_COULEUR}"
  echo -e "Statut: ${VERT}$etat_actif${SANS_COULEUR}"
  echo "Date: $date_actuelle"
  echo -e "Heure: ${VERT}$heure${SANS_COULEUR}"
  echo -e "---------------------------------------------\n"
done
