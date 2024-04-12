#!/bin/env bash
#Author : Axel CHALVIN
#Creation date : 08/03/2024
#Last edit : 22/03/2024

#######################################################################################################
# Ce script se connecte à la console de chaque serveur du site d'AIX avec différents utilisateurs LDAP.
# Il lance la commande affichant le nom du serveur donné sur chaque serveur.
#######################################################################################################

echo "Lancement du script..."

#test que tout les acces fonctionnes
function test_accès_ssh_avec_ldap {
    # $1: user
    # $2: pass

    # couleur
    RED="\e[31m"
    NOCOLOR="\e[0m"
    GREEN="\033[0;32m"
    
    USER="$1"
    PASS="$2"
    PORTS="22200 22202 22253 22004"
    SCRIPT="echo 'Nom de la machine : '; echo -e '${GREEN}$(hostname)${NOCOLOR}'"
    
    for PORT in ${PORTS}; 
    do
        echo "Accès SSH via l'ip publique (192.168.141.2) sur le port ${PORT}"  
        echo -e "$(ssh -p "${PORT}" $USER@192.168.141.2 ${SCRIPT})"
    done
}

function clear_terminal {
    # $1 : user
    echo "prochain utilisateur...$1"
    read 
    clear
}

echo "--------------------------------- accès avec compte LDAP: axel --------------------------------"
test_accès_ssh_avec_ldap "axel" "Solea05axel"
echo -e "----------------------------------------------------------------------------------------------------\n"

clear_terminal "alexandre"
echo "--------------------------------- accès avec compte LDAP: alexandre --------------------------------"
test_accès_ssh_avec_ldap "alexandre" "Solea05alexandre"
echo -e "----------------------------------------------------------------------------------------------------\n"

clear_terminal "thomas"
echo "--------------------------------- accès avec compte LDAP: thomas --------------------------------"
test_accès_ssh_avec_ldap "thomas" "Solea05thomas"
echo -e "----------------------------------------------------------------------------------------------------\n"

clear_terminal "admin-solea"
echo "--------------------------------- accès avec compte LDAP: compte local --------------------------------"
echo "Accès SSH via l'ip publique sur le port 22252"  
echo "Accès SSH via l'ip publique (192.168.141.2) sur le port 22252"  
echo 'Nom de la machine : '
sshpass -p " " ssh admin-solea@192.168.141.2 -p 22252 "hostname"
echo -e "----------------------------------------------------------------------------------------------------\n"

clear_terminal "echec"
echo "--------------------------------- accès avec compte LDAP: echec --------------------------------"
USER_SSH="echec"
PASS="echec"
PORTS="22200 22202 22253 22004"
SCRIPT="echo 'Nom de la machine : '; hostname"

 # couleur
RED="\e[31m"
NOCOLOR="\e[0m"
GREEN="\033[0;32m"

for PORT in ${PORTS}; 
do
    echo "Accès SSH via l'ip publique (192.168.141.2) sur le port ${PORT}"  
    ssh -p "${PORT}" $USER@192.168.141.2 "${SCRIPT}" 2>> /dev/null

    if [ $? -ne 1 ]; then
        echo -e "failed: ${RED}$PORT${NOCOLOR}"
    else
        echo -e "success: ${GREEN}$PORT${NOCOLOR}"
    fi
done
echo -e "----------------------------------------------------------------------------------------------------\n"

echo "Arrêt du script..."
