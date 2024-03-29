from checkdns.csvparser import CsvParser
from checkdns.resolutionname import ResolutionName
from checkdns.dnsresulthandler import DnsResultHandler
import pandas as pd
import sys
import argparse

####################################################################
# Author: Djetic Alexandre
# Date: 15/03/2024
# description: ce script test un server dns en fesant des requètes  
#              sur chaque enregistrement du/des fichier de zone
####################################################################

def parser():
    """
    Parse command line arguments.

    Returns:
        argparse.Namespace: An object containing parsed arguments.
    """
    parser = argparse.ArgumentParser(description="ce script test un serveur dns en réalisant une/des requète(s) dns et leur(s) requète(s) inverse")
    parser.add_argument('-v', '--verbose', help="Définit si il affiche dans la console les informations", const=1, nargs='?', default=0)
    parser.add_argument('-s', '--server', help="Définit l'adresse IP du serveur DNS à tester.")
    parser.add_argument('-f', '--file', help="Définit le fichier CSV source contenant les noms à tester.")
    parser.add_argument('-4', '--v4', help="Réalise des résolutions de noms IPv4.", action='store_true')
    parser.add_argument('-6', '--v6', help="Réalise des résolutions de noms IPv6.", action='store_true')
    parser.add_argument('-e', '--export', help="décide si on veut exporter au format csv les résulats")
    return parser.parse_args()


def main() -> None:
    """
    Main function to run the script.
    """
    args = parser()  # parser, donne les arguments possibles de la commande

    # check que server dns donnée
    if not args.server:
        print("donnée un serveur dns")
        sys.exit(1)

    # Import du fichier source
    if not args.file:
        print("donné un fichier de nom en .csv")
        sys.exit(1)

    # test aucune résolution a faire
    if not args.v4 and not args.v6:
        print("aucune résolution à faire...")
        sys.exit(1)
    
    # obtention des nom à tester
    column_names = ['nom', 'adresse IP', 'adresse IPv6', 'nom inverse']
    csvparser: CsvParser = CsvParser(args.file, column_names)
    data: pd.DataFrame = csvparser.parser()

    # résolutions ipv4
    if args.v4:
        resolution: ResolutionName = ResolutionName(data, args.server, 4)
        resolution.run()
        resolution_result: dict = resolution.export_result()
        handlerresult: DnsResultHandler = DnsResultHandler(resolution_result, "résolution IPv4", int(args.verbose))
        handlerresult.verbose("solea.local")
        print("\n")

    # résolutions
    if args.v6:
        resolution: ResolutionName = ResolutionName(data, args.server, 6)
        resolution.run()
        resolution_result: dict = resolution.export_result()
        handlerresult: DnsResultHandler = DnsResultHandler(resolution_result, "résolution IPv6", int(args.verbose))
        handlerresult.verbose("solea.local")
        print("\n")
    
    sys.exit(0)

if __name__ == "__main__":
    main()
