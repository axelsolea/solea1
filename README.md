# solea1

## Description
ce github contient tout les scripts pour le porjet étudiant solea1.

## Dépendance

### Installation de python:
- ubuntu/debian:
```bash
apt install python3 python-pip
```

- almalinux/redhat:
```bash
dnf install python3 python-pip
```

### Installation de bash

- ubuntu/debian:
```bash
apt install bash
```

- almalinux/redhat:
```bash
dnf install bash
```

⚠️ certain script demande un accès root ou privilégié ⚠️

## Lancement de script

### Script python
- example d'usage
```bash
python3 test_dns.py -s 1.1.1.1 -f list_name.csv -4 -6 -v -e
```

### Script bash
- donner les permissions d'exécution
```bash
chmod +x *.sh
```

- lancement du script avec un chemin relatif:
```bash
./test_internet_v2.sh
```

- lancement du script avec un chemin absolut:
```bash
/chemin/du/fichier.sh
```


- lancement du script avec un chemin relatif(accès root):
```bash
sudo ./test_internet_v2.sh
```

- lancement du script avec un chemin absolut(accès root):
```bash
sudo /chemin/du/fichier.sh
```
