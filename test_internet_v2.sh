#!/bin/env bash
#Author : Axel CHALVIN
#Creation date : 08/03/2024
#Last edit : 08/03/2024

echo "Script lancé"
echo "Script started : $(date)" > test_internet_v2.log

echo "Tentative de ping google.com (internet)..."
ping -c 1 -q google.com | grep "ping statistics" -A 1 >> test_internet_v2.log
if [[ $? == 0 ]];then
echo "OK ✓"
fi

echo "Tentative de ping 172.18.0.254 (GW Vlan 18)..."
ping -c 1 -q 172.18.0.254 | grep "ping statistics" -A 1 >> test_internet_v2.log
if [[ $? == 0 ]];then
echo "OK ✓"
fi

echo "Tentative de ping 172.21.254.254 (GW Vlan 21)..."
ping -c 1 -q 172.21.254.254 | grep "ping statistics" -A 1 >> test_internet_v2.log
if [[ $? == 0 ]];then
echo "OK ✓"
fi

echo "Tentative de ping 172.22.254.254 (GW Vlan 22)..."
ping -c 1 -q 172.22.254.254 | grep "ping statistics" -A 1 >> test_internet_v2.log
if [[ $? == 0 ]];then
echo "OK ✓"
fi

echo "Tentative de ping 172.23.254.254 (GW Vlan 23)..."
ping -c 1 -q 172.23.254.254 | grep "ping statistics" -A 1 >> test_internet_v2.log
if [[ $? == 0 ]];then
echo "OK ✓"
fi

echo "Tentative de ping 172.24.254.254 (GW Vlan 24)..."
ping -c 1 -q 172.24.254.254 | grep "ping statistics" -A 1 >> test_internet_v2.log
if [[ $? == 0 ]];then
echo "OK ✓"
fi

echo "Tentative de ping 172.26.255.254 (GW Vlan 26)..."
ping -c 1 -q 172.26.255.254 | grep "ping statistics" -A 1 >> test_internet_v2.log
if [[ $? == 0 ]];then
echo "OK ✓"
fi

echo "Tentative de ping 172.28.254.254 (GW Vlan 28)..."
ping -c 1 -q 172.28.254.254 | grep "ping statistics" -A 1 >> test_internet_v2.log
if [[ $? == 0 ]];then
echo "OK ✓"
fi

echo "Tentative de ping 172.29.254.254 (GW Vlan 29 via tunnel GRE)..."
ping -c 1 -q 172.21.254.254 | grep "ping statistics" -A 1 >> test_internet_v2.log
if [[ $? == 0 ]];then
echo "OK ✓"
fi

echo "Tentative de ping 172.30.254.254 (GW Vlan 30 via tunnel GRE)..."
ping -c 1 -q 172.21.254.254 | grep "ping statistics" -A 1 >> test_internet_v2.log
if [[ $? == 0 ]];then
echo "OK ✓"
fi

echo "Fin d'execution du script $(date)" >> test_internet_v2.log

echo "Afficher les logs? (y/n)"
read ans
if [ "$ans" = "y" ];then 
cat test_internet_v2.log
fi
 
