#!/bin/env bash
#Author : Axel 
#Date : 15/02/2024
#Last edit : 16/02/2024
#Desc : make an ip get banned via ssh on asterisk
ip=192.168.141.252
#ip=172.18.0.4

echo "Lancement du script..."
for i in 1 2 3 4
do
	echo "Tentative $i" 
	sshpass -p motdepasseerrone ssh admin-solea@${ip}
done
echo "Script terminé"
