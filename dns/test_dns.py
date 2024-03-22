from collections import deque
from dnsclient import Dnsclient
import pandas as pd
import sys
import argparse
import logging

# logging
# (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL)

####################################################################
# Author: Djetic Alexandre
# Date: 15/03/2024
# description: ce script test un server dns en fesant des requètes  
#              sur chaque enregistrement du/des fichier de zone
####################################################################

def show_dataframe(df: pd.DataFrame) -> None:
    """
    Display data from the DataFrame of names.

    Args:
        df (pd.DataFrame): The pandas DataFrame containing the data.
    """
    for index, row in df.iterrows():
        print(f"{row['nom']}, {row['adresse IP']}, {row['adresse IPv6']}, {row['nom inverse']}")


def got_nan_serie(serie) -> bool:
    """
    Check if the given series contains any NaN values.

    Args:
        serie (pd.core.series.Series): The pandas Series to check for NaN values.

    Returns:
        bool: True if any NaN value is found, False otherwise.
    """
    for field in serie:
        if pd.isna(field):
            return True

    return False


def test_one_name(serie, dnsclient: Dnsclient, ip_version: int) -> bool:
    """
    Test DNS resolution for a single name against a given DNS client and IP version.

    Args:
        serie (pd.Series): The pandas Series containing the name and address to test.
        dnsclient (Dnsclient): The DNS client object used for DNS resolution.
        ip_version (int): The IP version to test (4 for IPv4, 6 for IPv6).

    Returns:
        bool: True if DNS resolution is successful for all names, False otherwise.
    """
    # If a NaN field appears, don't resolve
    if got_nan_serie(serie):
        return False
    
    if ip_version == 4:
        cli_a_record: str = list(dnsclient.get_A_record(serie["nom"]).split("\n")) # il peut avoir plusieurs résultat dont plusieurs IP, d'ou le split pour avoir un tableau
        cli_ptr_record: str = dnsclient.get_PTR_record(serie["adresse IP"])
        
        #test que les enregistrement sont non vide
        if cli_ptr_record and cli_a_record:
            return cli_ptr_record == f"{serie['nom inverse']}." and serie["adresse IP"] in cli_a_record
    else:
        cli_aaaa_record: str = list(dnsclient.get_AAAA_record(serie["nom"]).split("\n")) # il peut avoir plusieurs résultat dont plusieurs IP, d'ou le split pour avoir un tableau
        cli_ptr_record: str = dnsclient.get_PTR_record(serie["adresse IPv6"])
        
        #test que les enregistrement sont non vide
        if cli_ptr_record and cli_aaaa_record:
            return cli_ptr_record == f"{serie['nom inverse']}." and serie["adresse IPv6"] in cli_aaaa_record


def test_name(df: pd.DataFrame, dnsclient: Dnsclient, ip_version: int) -> tuple:
    """
    Test DNS resolution for names in a DataFrame against a given DNS client and IP version.

    Args:
        df (pd.DataFrame): The pandas DataFrame containing names and addresses to test.
        dnsclient (Dnsclient): The DNS client object used for DNS resolution.
        ip_version (int): The IP version to test (4 for IPv4, 6 for IPv6).

    Returns:
        tuple: A tuple containing count of total records, count of successful resolutions, and a deque of failed requests.
    """
    cpt: int = 0
    cpt_tmp: int = 0
    failed_request: deque = deque()

    for index, row in df.iterrows():
        got_nan: bool = got_nan_serie(row)
        if test_one_name(row, dnsclient, ip_version) and not got_nan:
            cpt += 1
            cpt_tmp += 1
        elif not got_nan: #ne pas afficher les nan ici
            failed_request.append(row["nom"])
            cpt += 1

    return (cpt, cpt_tmp, failed_request)


def check_resolution(args_v: bool, cpt: int, cpt_tmp: int, failed_request: deque) -> bool:
    """
    Check if resolution is successful based on command line arguments and resolution counts.

    Args:
        args_v (bool): The flag indicating whether to show verbose output.
        cpt (int): The count of total records.
        cpt_tmp (int): The count of successful resolutions.
        failed_request (deque): A deque containing failed requests.

    Returns:
        bool: True if resolution is successful, False otherwise.
    """
    if args_v and cpt == cpt_tmp:
        return True
    elif args_v and cpt != cpt_tmp:
        return False


def extract_data(file: str) -> pd.DataFrame:
    """
    Extract data from a CSV file into a pandas DataFrame.

    Args:
        file (str): The path to the CSV file.

    Returns:
        pd.DataFrame: The DataFrame containing the extracted data.
    """
    try: 
        data: pd.DataFrame = pd.read_csv(f"{file}", header = 0, delimiter = ',')
    except FileNotFoundError as e:
        print(f"Le fichier source n'a pas été trouvé...")
        sys.exit(1)
    except Exception as e:
        print(f"Une erreur non supportée est survenue, quitter...\n{e}")
        sys.exit(1)

    return data

def export_data_csv(data: pd.DataFrame, failed_request: deque, ip_version: int, file_export: str) -> None:
    resolution_name: list = []
    resolution_name_ok: list = [] #OK ou NOK
    resolution_ptr: list = []
    resolution_ptr_ok: list = [] #OK ou NOK

    for index, row in data.iterrows():
        if row["nom"] in failed_request:

        else:
        #itérer sur les data, si dans

        if row["nom_inverse"] in failed_request:

        else:
        #itérer sur les data, si dans

    
    #export to csv
    resultat_resolution_name: df.DataFrame = df.DataFrame({"nom": resolution_name, "test": resolution_name_ok})
    resultat_resolution_ptr: df.DataFrame = df.DataFrame({"nom inverse": resolution_name, "test": resolution_name_ok})
    resultat_resolution_name.to_csv("", sep=",", index=False, encoding="utf-8")
    resultat_resolution_ptr.to_csv("", sep=",", index=False, encoding="utf-8")


def resolution_mode_debug(data: pd.DataFrame, args, file_export: str = "") -> None:
    """
    Résout les noms de domaine en adresses IPv4 et/ou IPv6 selon les options fournies.

    Args:
        data (pd.DataFrame): Le DataFrame contenant les données à tester.
        args (any): Les arguments passés au programme.

    Returns:
        None

    Cette fonction effectue la résolution des noms de domaine en adresses IPv4 et/ou IPv6
    en utilisant un client DNS spécifié dans les arguments. Elle vérifie ensuite si toutes
    les résolutions demandées ont été effectuées avec succès et affiche un message approprié.
    """
    # Résolution des noms en IPv4
    if args.v4:
        dnsclient: Dnsclient = Dnsclient(args.server)
        cpt_v4, cpt_tmp_v4, failed_request_v4 = test_name(data, dnsclient, 4)

    # Résolution des noms en IPv6
    if args.v6:
        dnsclient: Dnsclient = Dnsclient(args.server)
        cpt_v6, cpt_tmp_v6, failed_request_v6 = test_name(data, dnsclient, 6)
    
    # vérification résolution de tout les noms en ipv4
    if args.v4 and check_resolution(args.v4, cpt_v4, cpt_tmp_v4, failed_request_v4):
        print("toutes les résolutions en ipv4 ont été résolue ! ")
    elif args.v4:
        print(f"tout les résolutions en ipv4 n'ont pas été résolue ! ")
        print(f"voici le/les enregistrement(s) ipv4 non validée: {', '.join(failed_request_v4)}")
    
    # vérification résolution de tout les noms en ipv6
    if args.v6 and check_resolution(args.v6, cpt_v6, cpt_tmp_v6, failed_request_v6):
        print("toutes les résolutions en ipv6 ont été résolue ! ")
    elif args.v6:
        print(f"tout les résolutions en ipv6 n'ont pas été résolue ! ")
        print(f"voici le/les enregistrement(s) ipv6 non validée: {', '.join(failed_request_v6)}")

def resolution_mode_prod(data: pd.DataFrame, args, file_export: str = "") -> None:
    """
    Résout les noms de domaine en adresses IPv4 et/ou IPv6 selon les options fournies.

    Args:
        data (pd.DataFrame): Le DataFrame contenant les données à tester.
        args (any): Les arguments passés au programme.

    Returns:
        None

    Cette fonction effectue la résolution des noms de domaine en adresses IPv4 et/ou IPv6
    en utilisant un client DNS spécifié dans les arguments. Elle vérifie ensuite si toutes
    les résolutions demandées ont été effectuées avec succès et affiche un message approprié.

    pass
    """
    # Résolution des noms en IPv4
    if args.v4:
        dnsclient: Dnsclient = Dnsclient(args.server)
        cpt_v4, cpt_tmp_v4, failed_request_v4 = test_name(data, dnsclient, 4)

    # Résolution des noms en IPv6
    if args.v6:
        dnsclient: Dnsclient = Dnsclient(args.server)
        cpt_v6, cpt_tmp_v6, failed_request_v6 = test_name(data, dnsclient, 6)

    # vérification résolution de tout les noms en ipv4
    if args.v4 and check_resolution(args.v4, cpt_v4, cpt_tmp_v4, failed_request_v4):
        print("toutes les résolutions en ipv4 ont été résolue ! ")
        export_data_csv(data, failed_request_v4, 4)
    elif args.v4:
        print(f"tout les résolutions en ipv4 n'ont pas été résolue ! ")
        export_data_csv(data, failed_request_v4, 4)
    
    # vérification résolution de tout les noms en ipv6
    if args.v6 and check_resolution(args.v6, cpt_v6, cpt_tmp_v6, failed_request_v6):
        print("toutes les résolutions en ipv6 ont été résolue ! ")
        export_data_csv(data, failed_request_v6, 6)
    elif args.v6:
        print(f"tout les résolutions en ipv6 n'ont pas été résolue ! ")
        export_data_csv(data, failed_request_v6, 6)



def parser():
    """
    Parse command line arguments.

    Returns:
        argparse.Namespace: An object containing parsed arguments.
    """
    parser = argparse.ArgumentParser(description = "ce script test un serveur dns en réalisant une/des requète(s) dns et leur(s) requète(s) inverse")
    parser.add_argument('-m', '--mode', help = "Définit le mode de lancement du test.", default="prod")
    parser.add_argument('-s', '--server', help = "Définit l'adresse IP du serveur DNS à tester.")
    parser.add_argument('-f', '--file', help = "Définit le fichier CSV source contenant les noms à tester.")
    parser.add_argument('-4', '--v4', help = "Réalise des résolutions de noms IPv4.",  action = 'store_true')
    parser.add_argument('-6', '--v6', help = "Réalise des résolutions de noms IPv6.", action = 'store_true')
    parser.add_argument('-e', '--export', help = "décide si on veut exporter au format csv les résulats")
    return parser.parse_args()


def main() -> None:
    """
    Main function to run the script.
    """
    args = parser() #parser, donne les arguments possibles de la commande
    
    # check que server dns donnée
    if not args.server:
        print("donnée un serveur dns")
        sys.exit(1)

    # Import du fichier source
    if not args.file:
        print("donné un fichier de nom en .csv")
        sys.exit(1)
    
    #test aucune résolution a faire
    if not args.v4 and not args.v6:
        print("aucune résolution à faire...")
        sys.exit(1)

    #mode de lancement prod/debug
    if args.mode == "prod":
        data: pd.DataFrame = extract_data(args.file) #obtention des noms à tester
    else:
        data: pd.DataFrame = extract_data(args.file) #obtention des noms à tester
        resolution_mode_debug(data, args)

if __name__ == "__main__":
    main()
