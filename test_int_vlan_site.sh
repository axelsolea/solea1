#!/bin/bash
# Author: CHOLLET Emeline
# Date: 16/02/2024
# Modified: 29/02/2024
# Description: Test inter vlan inter site 
# piste d'amelioration : mettre le nom du vlan dans une variable et afficher la variable 
#2 bloc : intern vlan, inter site -> site valence faire traceroute 


tab[0]=172.18.0.254
tab[1]=2001:470:C84C:100:FFFF:FFFF:FFFF:FF00%64  #Vlan18 Serveur
tab[2]=172.21.254.254 
tab[3]=2001:470:C84C:1400:FFFF:FFFF:FFFF:FF00%64 #Vlan21 RND
tab[4]=172.22.254.254 
tab[5]=2001:470:C84C:3400:FFFF:FFFF:FFFF:FF00%64 #Vlan22 Direction
tab[6]=172.23.254.254
tab[7]=2001:470:C84C:3400:FFFF:FFFF:FFFF:FF00%64 #Vlan23 Employe
tab[8]=172.24.254.254
tab[9]=2001:470:C84C:4400:FFFF:FFFF:FFFF:FF00%64 #Vlan24 Responsable 
tab[10]=172.28.254.254
tab[11]=2001:470:C84C:300:FFFF:FFFF:FFFF:FF00%64 #Vlan28 Téléphonie
tab[12]=172.30.254.254
tab[13]=2001:470:C84C:200:FFFF:FFFF:FFFF:FF00%64 #Vlan30 Wifi

tab[14]=172.26.255.254
tab[15]=2001:470:c84c:600::1/64 #Vlan26 Site Valence PC
tab[16]=172.29.255.254
tab[17]=2001:470:c84c:900::1/64 #Vlan29 Site Valence Téléphonie


#### TEST inter vlan IPv4/IPv6 ####
echo " Test des interfaces des vlan et des 2 sites"
i=1
while (( $i < ${#tab[*]} )); do
ping -c 1 ${tab[$i]} -q
tabR[$i]=${?};
i=$((i+1));
done
clear
i=1
while (( $i < ${#tab[*]} )); do
if [ ${tabR[$i]} -eq 0 ];
then echo " ${tab[$i]} répond correctement au ping. "
else echo " ${tab[$i]} ne répond pas."
    traceroute ${tab[$i]}
fi
i=$((i+1));
done


