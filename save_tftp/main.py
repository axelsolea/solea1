import json
import argparse
import sys
import os
import subprocess
from subprocess import PIPE
import logging
from systemd.journal import JournalHandler

##################################################################################
### Auteur: Djetic Alexandre                                                   ###
### Description: ce script permet de sauvegarder plusieurs fichiers sur        ###
###     un serveur TFTP                                                        ###
##################################################################################

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Script pour sauvegarder des fichiers sur un serveur TFTP")
    parser.add_argument("-s", "--server", required=True, help="Adresse du serveur TFTP")
    parser.add_argument("-p", "--port", type=int, default=69, help="Port du serveur TFTP (par défaut 69)")
    parser.add_argument("-f", "--file", required=True, help="Chemin du fichier JSON source")
    return parser.parse_args()

def main() -> None:
    ####################################
    ###  log de lancement du script ####
    ####################################
    
    log = logging.getLogger('demo')
    log.addHandler(JournalHandler())
    log.setLevel(logging.INFO)
    log.info("lancement du script ")

    ###############################
    ### obtention des arguments ###
    ###############################

    args = parse_args()
    server = args.server
    port = args.port
    json_file = args.file

    ############################################
    ### obtention des données de sauvegarde  ###
    ############################################

    try:
        with open(json_file, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Erreur: le fichier {json_file} n'a pas été trouvé.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Erreur: le fichier {json_file} n'est pas un fichier JSON valide.")
        sys.exit(1)

    dir_name = data.get("dir")
    files = data.get("files", {})

    if not dir_name or not files:
        print("Erreur: les données JSON ne contiennent pas les informations nécessaires.")
        sys.exit(1)

    ############################################
    ###       sauvegarde des fichiers        ###
    ############################################

    for filename, filepath in files.items():
        if not os.path.isfile(filepath):
            print(f"Erreur: le fichier {filepath} n'a pas été trouvé sur le système local.")
            continue

        remote_path = f"{dir_name}/{filename}"
        try:
            command = f"echo 'put {filepath} {remote_path}' | tftp {server}"
            result = subprocess.run(command, shell=True, stdout=PIPE, stderr=PIPE, universal_newlines=True)

            print(f"Commande exécutée: `echo 'put {filepath} {remote_path}' | tftp {server} > /dev/null`")
            if result.returncode == 0:
                print(f"Fichier {filename} téléchargé avec succès sur {remote_path}.")
            else:
                print(f"Erreur lors du téléchargement de {filename} sur {remote_path}. Détails : {result.stderr}")
        except Exception as e:
            print(f"Erreur lors du téléchargement de {filename}: {e}")

if __name__ == '__main__':
    main()
