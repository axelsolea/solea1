#!/bin/env bash
#Author : Axel 
#Date : 16/02/2024
#Last edit : 16/02/2024
#Desc : Raw dns testing

echo "Script started"

echo "Resolving resolver1"
nslookup resolver1.solea.local
nslookup 172.18.0.200

echo "Resolving zone1"
nslookup zone1.solea.local
nslookup 172.18.0.202

echo "Resolving dhcp"
nslookup dhcp.solea.local
nslookup 172.18.0.253

echo "Resolving toip"
nslookup toip.solea.local
nslookup 172.18.0.4

echo "Resolving share (samba)"
nslookup share.solea.local
nslookup 172.18.0.252

echo "Resolving gw"
nslookup gw.solea.local
nslookup 172.18.0.254

echo "Resolving esxi"
nslookup esxi.solea.local
#nslookup 192.168.141.3 => entrée ptr inexistante
