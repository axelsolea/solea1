# Commande à lancer pour la recette

## Donnez les droits d'éxecution

```bash
chmod +x *.sh
```

## LDAP et NAT

```bash
./test_nat_pat_v2.sh
```

## test de flood(iperf)

- flood TCP

```bash
iperf3 –c 172.26.255.253 -t 30
```

- flood UDP

 ```bash
iperf3 –c 172.26.255.253 -t 30 –b 1G –u
``` 

## DHCP

```bash
sudo  ./test_dhcp.sh ens160
```

## DNS

- enregistrement valide :
```bash
python3 dns/test_dns.py -s 172.18.0.200 -f dns/list_name.csv -4 -6 -v
```

- enregistrement non valide :
```bash
python3 dns/test_dns.py -s 172.18.0.200 -f dns/list_name_false_data.csv -4 -6 -v
```

## samba

```bash
cd samba
sudo python3 main.py -s smb.solea.local -l list_users.csv
sudo python3 main.py -s 172.18.0.251 -l list_users.csv
```

## NTP

```bash
./test_ntp.sh server_name.txt 
```

## sauvegarde automatique(TFTP)

```bash
python3 solea1/save_tftp/main.py -s backup.solea.local -f solea1/save_tftp/config_dhcp.json
python3 solea1/save_tftp/main.py -s 172.18.0.5 -f solea1/save_tftp/config_dhcp.json
```
