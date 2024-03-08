#!/bin/sh

# LDAP server details
LDAP_SERVER="172.18.0.252"
LDAP_BASE="DC=solea,DC=local"

# Install required packages
apk add openldap openldap-clients nss-pam-ldapd openldap-back-mdb

# Configure nslcd
cat <<EOF > /etc/nslcd.conf
uid nslcd
gid ldap
uri ldap://${LDAP_SERVER}
base ${LDAP_BASE}
EOF

# Configure nsswitch.conf
sed -i '/^passwd:/ s/$/ ldap/' /etc/nsswitch.conf
sed -i '/^shadow:/ s/$/ ldap/' /etc/nsswitch.conf
sed -i '/^group:/ s/$/ ldap/' /etc/nsswitch.conf

# Configure pam.d/system-login
sed -i '1i auth    required    pam_ldap.so' /etc/pam.d/system-login

# Restart nslcd
service nslcd restart

echo "LDAP authentication configured successfully."
