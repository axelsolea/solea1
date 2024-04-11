# solea1

## Description
Ce dépôt GitHub contient tous les scripts pour le projet étudiant solea1.

## Dépendances

### Installation de Python :
- Pour Ubuntu/Debian :
  ```bash
  apt install python3 python-pip
  ```
- Pour AlmaLinux/RedHat :
  ```bash
  dnf install python3 python-pip
  ```

### Installation de Bash :
- Pour Ubuntu/Debian :
  ```bash
  apt install bash
  ```
- Pour AlmaLinux/RedHat :
  ```bash
  dnf install bash
  ```

⚠️ Certains scripts nécessitent un accès root ou des privilèges ⚠️

## Lancement des scripts

### Script Python
- Exemple d'utilisation :
  ```bash
  python3 test_dns.py -s 1.1.1.1 -f list_name.csv -4 -6 -v -e
  ```

### Script bash
- Donner les permissions d'exécution :
  ```bash
  chmod +x *.sh
  ```

- Lancement du script avec un chemin relatif :
  ```bash
  ./test_internet_v2.sh
  ```

- Lancement du script avec un chemin absolu :
  ```bash
  /chemin/du/fichier.sh
  ```
  
- Lancement du script avec un chemin relatif (accès root) :
  ```bash
  sudo ./test_internet_v2.sh
  ```

- Lancement du script avec un chemin absolu (accès root) :
  ```bash
  sudo /chemin/du/fichier.sh
  ```
