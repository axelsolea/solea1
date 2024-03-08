#!/bin/bash
# Author: CHOLLET Emeline
# Date: 08/03/2024
# Modified: $DATE
# Modified: 29/02/2024
# Description: Test inter vlan inter site 


#### TEST inter vlan IPv4/IPv6 ####
# Gateway vlan18 serveur
echo " "
echo "Test Vlan 18 "
echo " "
ping -c 1 172.18.0.254 
ping -c 1 2001:470:C84C:100:FFFF:FFFF:FFFF:FF00%64 

# Gateway vlan21 RND
echo " " 
echo "Test Vlan 21 "
echo " "
ping -c 1 172.21.254.254 
ping -c 1 2001:470:C84C:1400:FFFF:FFFF:FFFF:FF00%64 

# Gateway vlan22 Direction 
echo " " 
echo "Test Vlan 22 "
echo " "
ping -c 1 172.22.254.254 
ping -c 1 2001:470:C84C:2400:FFFF:FFFF:FFFF:FF00%64 

# Gateway vlan23 Employé
echo " "
echo "Test Vlan 23 "
echo " "
ping -c 1 172.23.254.254
ping -c 1 2001:470:C84C:3400:FFFF:FFFF:FFFF:FF00%64

# Gateway vlan24 Responsable 
echo " " 
echo "Test Vlan 24 "
echo " "
ping -c 1 172.24.254.254
ping -c 1 2001:470:C84C:4400:FFFF:FFFF:FFFF:FF00%64

# Gateway vlan30 wifi 
echo " " 
echo "Test Vlan 30 "
echo " "
ping -c 1 172.30.254.254
ping -c 1 2001:470:C84C:200:FFFF:FFFF:FFFF:FF00%64

# Gateway vlan28 Téléphone
echo " " 
echo "Test Vlan 28 "
echo " "
ping -c 1 172.28.254.254
ping -c 1 2001:470:C84C:300:FFFF:FFFF:FFFF:FF00%64

##### Test Inter site #####
# Gateway vlan 26 PC val
echo " "
echo "Test Vlan 26 PC Valence "
echo " "
ping -c 1 172.26.255.254
ping -c 1 2001:470:c84c:600::1/64
traceroute 172.26.255.254

# Gateway Vlan29 Téléphone Val 
echo " " 
echo "Test Vlan 29 Tel Val "
echo " "
ping -c 1 172.29.255.254
ping -c 1 2001:470:c84c:900::1/64
traceroute 172.29.255.254
