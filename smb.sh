#/bin/env bash
#Author : Axel 
#Date : 16/02/2024
#Last edit : 16/02/2024
#Desc : Permet de se connecter au serveur samba, crée un dossier, un fichier et de cleanup
#smbclient -U DOMAIN\user_name //server_name/share_name -c "cd /example/ ; get example.txt ; exit"

echo "Lancement du script..."
smbclient -U admin1%123 -L //172.18.0.252
smbclient -U admin1%123 //172.18.0.252/solea_document -c "mkdir demo ; cd /demo/ ; get example.txt ; exit"

