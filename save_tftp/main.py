from ftplib import FTP
import json
import argparse
import sys
import os

##################################################################################
### Auteur: Djetic Alexandre                                                   ###
### Description: ce script permet de sauvegarder plusieurs fichiers sur        ###
###     un serveur FTP                                                         ###
##################################################################################

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Script pour sauvegarder des fichiers sur un serveur FTP")
    parser.add_argument("-s", "--server", required=True, help="Adresse du serveur FTP")
    parser.add_argument("-f", "--file", required=True, help="Chemin du fichier JSON source")
    return parser.parse_args()

def main() -> None:
    ###############################
    ### obtention des arguments ###
    ###############################

    args = parse_args()

    server = args.server
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

    try:
        with FTP(server) as ftp:
            ftp.login()
            ftp.cwd('/')  # Aller à la racine du serveur FTP
            if dir_name not in ftp.nlst():
                ftp.mkd(dir_name)  # Créer le répertoire s'il n'existe pas

            ftp.cwd(dir_name)  # Aller dans le répertoire

            for filename, filepath in files.items():
                if not os.path.isfile(filepath):
                    print(f"Erreur: le fichier {filepath} n'a pas été trouvé sur le système local.")
                    continue

                with open(filepath, "rb") as file:
                    ftp.storbinary(f"STOR {filename}", file)
                    print(f"Fichier {filename} téléchargé avec succès.")

    except Exception as e:
        print(f"Erreur: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
