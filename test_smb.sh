#!/bin/bash
# Auteur: Axel 
# Date: 16/02/2024
# Dernière modification: 05/04/2024
# Description: Permet de se connecter au serveur samba, créer un dossier, un fichier et de nettoyer

#########################################################################
# Ce script réalise un test complet d'un partage de fichier samba:
# - Création du dossier de partage
# - Connexion avec le serveur 
# - Liaison du dossier de partage et le serveur
# - Création d'un fichier texte
# - Lecture du fichier créé précédemment
# - Suppression du lien du dossier de partage et le serveur
# - Vérification de la connexion au partage avec un identifiant inconnu
#########################################################################

if [ $EUID -ne 0 ]; then
  echo "un accès root/sudo est requie pour l'execution"
  exit 1 
fi

# couleur
RED="\e[31m"
NOCOLOR="\e[0m"
GREEN="\033[0;32m"

# Variables d'environnement
IP="172.18.0.252"
NAME="share.solea.local"
SHARE="solea_document"
SHARE_DIR="/mnt/smb_share"
USER_SHARE="admin1"
PASS="123"

# Test
echo -e "${RED}Test du partage de solea${NOCOLOR}"

echo -e "\n---- Informations sur le test, paramètres ----"
echo "Adresse IP du serveur de partage: $IP"
echo "Nom du serveur de partage: $NAME "
echo "Sélection du partage: $SHARE"
echo "Dossier de partage: $SHARE_DIR"
echo "Utilisateur: $USER_SHARE"
echo "Mot de passe: $PASS"
echo "----------------------------------------------"

echo -e "\n1) Création du dossier de partage: $SHARE_DIR"
mkdir -p "$SHARE_DIR"

if [ $? -eq 0 ]; then
  echo -e "Création du dossier... ${GREEN}succès${NOCOLOR}"
else
  echo -e "Création du dossier... ${RED}échec${NOCOLOR}"
fi


echo -e "\n2) Connexion avec le serveur de partage de fichiers et de dossiers: $NAME"
ping -c 1 $NAME >> /dev/null

if [ $? -eq 0 ]; then
  echo -e "Connexion en cours... ${GREEN}succès${NOCOLOR}"
else 
  echo -e "Connexion en cours... ${RED}échec${NOCOLOR}"
fi 


echo -e "\n3) Liaison du dossier de partage au partage du serveur: $SHARE_DIR"
mount -t cifs "//$IP/$SHARE" "$SHARE_DIR" -o username="$USER_SHARE",password="$PASS" >> /dev/null

if [ $? -eq 0 ]; then
  echo -e "Liaison en cours... ${GREEN}succès${NOCOLOR}"
else
  echo -e "Liaison en cours... ${RED}échec${NOCOLOR}"
fi


echo -e "\n4) Création d'un fichier admin1.txt dans le dossier partagé"
echo "contenue du fichier $SHARE_DIR/admin1.txt prévue:"
echo -e "Texte de admin1\n"
echo "Texte de admin1" > "$SHARE_DIR/admin1.txt"

if [ $? -eq 0 ]; then 
  echo -e "Création du fichier $SHARE_DIR/admin1.txt... ${GREEN}succès${NOCOLOR}"
else 
  echo -e "Création du fichier $SHARE_DIR/admin1.txt... ${RED}échec${NOCOLOR}"
fi 


echo -e "\n5) Lecture du fichier: $SHARE_DIR/admin1.txt"
CONTENT=$(cat "${SHARE_DIR}/admin1.txt")

echo "Contenu de $SHARE_DIR/admin1.txt:"
echo "$CONTENT"

if [ -z "$CONTENT" ]; then 
  echo "Le contenue de $SHARE_DIR/admin1.txt est vide..."
fi 

if [ "$CONTENT" == "Texte de admin1" ]; then 
  echo -e "Le contenu du fichier est correcte... ${GREEN}succès${NOCOLOR}"
else 
  echo -e "Le contenu du fichier n'est pas correcte... ${RED}échec${NOCOLOR}"
fi 


echo -e "\n6) Suppression du lien du dossier de partage et du serveur"
umount $SHARE_DIR >> /dev/null

if [ $? -eq 0 ]; then 
  echo -e "Suppression du lien... ${GREEN}succès${NOCOLOR}"
else 
  echo -e "Suppression du lien... ${RED}échec${NOCOLOR}"
fi


echo -e "\n7) Tentative de connexion au partage avec un identifiant incorrect"

echo -e "\nUtilisateur inexistant du partage:"
echo "Nom: jhon"
echo "Mot de passe: smith"

mount -t cifs "//$NAME/$SHARE" "$SHARE_DIR" -o username="jhon",password="smith" 2> /dev/null

if [ $? -eq 0 ]; then
  echo -e "\nLa connexion au serveur ne doit pas fonctionner ici... ${RED}échec${NOCOLOR}"
else 
  echo -e "\nLa connexion au serveur ne doit pas fonctionner ici... ${GREEN}succès${NOCOLOR}"
fi
