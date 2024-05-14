from ftplib import FTP
import json
import argparse
import sys

##################################################################################
### Auteur: Djetic Alexandre                                                   ###
### Description: ce script permet de sauvegarder plusieurs fichier sur         ###
###     un serveur tftp                                                        ###
##################################################################################


def parser() -> dict:
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--server", help="Il s'agit du serveur tftp")
    parser.add_argument("-f", "--file", help="fichier json source")
    return parser.parse_args()


def main() -> None:
    ###############################
    ### obtiention des argument ###
    ###############################

    args = parser()

    if args.server:
        print("donner un serveur tftp.")
        sys.exit(1)

    if args.file:
        print("donner un fichier ")
        sys.exit(1)

    ############################################
    ### obtiention des données de sauvegarde ###
    ############################################

    data: dict = {}
    with open("config.json", "r") as f:
        data: json.load(f)

    ############################################
    ###       sauvegarde des fichiers        ###
    ############################################

    with FTP("172.18.0.5") as ftp:
        ftp.login()
        print(ftp.dir())
        # création du dossier
        #créer du fichier: put $keys value pour chaque


if __name__ == '__main__':
    main()
