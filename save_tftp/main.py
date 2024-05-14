import json
import argparse
import sys
import os
import tftpy

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

    client = tftpy.TftpClient(server, port)

    for filename, filepath in files.items():
        if not os.path.isfile(filepath):
            print(f"Erreur: le fichier {filepath} n'a pas été trouvé sur le système local.")
            continue

        remote_path = f"{dir_name}/{filename}"
        try:
            client.upload(remote_path, filepath)
            print(f"Fichier {filename} téléchargé avec succès sur {remote_path}.")
        except Exception as e:
            print(f"Erreur lors du téléchargement de {filename}: {e}")

if __name__ == '__main__':
    main()
