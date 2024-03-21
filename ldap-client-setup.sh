#!/bin/sh
# Author: Djetic Alexandre
# Date: 02/02/2024
# Modified: 02/02/2024
# Description: this script setup a LDAP client on debian base distro

#non interactif
#export DEBIAN_FRONTEND=noninteractive

# Install required packages
sudo apt update && sudo apt upgrade -y
sudo apt -y install neovim vim nano curl libnss-ldap libpam-ldap ldap-utils

# Configure /etc/nsswitch.conf
sudo sh -c 'echo "passwd: compat systemd ldap" > /etc/nsswitch.conf'
sudo sh -c 'echo "group: compat systemd ldap" >> /etc/nsswitch.conf'
sudo sh -c 'echo "shadow: compat" >> /etc/nsswitch.conf'

# Configure /etc/pam.d/common-password
sudo sh -c 'echo "password [success=1 user_unknown=ignore default=die] pam_ldap.so try_first_pass" > /etc/pam.d/common-password'

# Configure /etc/pam.d/common-session
sudo sh -c 'echo "session optional pam_mkhomedir.so skel=/etc/skel umask=077" > /etc/pam.d/common-session'
