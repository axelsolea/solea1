#!/bin/env bash
#Author : Axel CHALVIN
#Creation date : 08/03/2024
#Last edit : 08/03/2024

echo "Lancement du script..."

#test que tout les acces fonctionnes
function test_accès_ssh_avec_ldap {
    # $1: user
    # $2: pass
    
    USER="$1"
    PASS="$2"
    PORTS="22200 22202 22253 22004"
    SCRIPT="echo 'Nom de la machine : '; hostname"
    KEY="/home/solea/.ssh/ssh_solea.pub"
    
    for PORT in ${PORTS}; do
    echo "Accès SSH via l'ip publique (192.168.141.2) sur le port ${PORT}"  
    ssh -i "$KEY" -p "${PORT}" $USER@192.168.141.2 "${SCRIPT}"
    echo ""
done
}


echo "--------------------------------- accès avec compte LDAP: axel --------------------------------"
test_accès_ssh_avec_ldap "axel" "Solea05axel"
echo -e "----------------------------------------------------------------------------------------------------\n"

echo "--------------------------------- accès avec compte LDAP: alexandre --------------------------------"
test_accès_ssh_avec_ldap "alexandre" "Solea05alexandre"
echo -e "----------------------------------------------------------------------------------------------------\n"


echo "--------------------------------- accès avec compte LDAP: thomas --------------------------------"
test_accès_ssh_avec_ldap "thomas" "Solea05thomas"
echo -e "----------------------------------------------------------------------------------------------------\n"

echo "--------------------------------- accès avec compte LDAP: jhon --------------------------------"
test_accès_ssh_avec_ldap "jhon" "Solea05jhon"
echo -e "----------------------------------------------------------------------------------------------------\n"

echo "--------------------------------- accès avec compte LDAP: compte locale --------------------------------"
echo "Accès SSH via l'ip publique sur le port 22252"  
echo "Accès SSH via l'ip publique (192.168.141.2) sur le port 22252"  
echo 'Nom de la machine : '
sshpass -p " " ssh admin-solea@192.168.141.2 -p 22252 "hostname"
echo -e "----------------------------------------------------------------------------------------------------\n"

echo "Arrêt du script..."
