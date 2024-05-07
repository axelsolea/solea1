import argparse
from extractname import ExtractName
from testshare import TestShare
from parseresult import ParseResult
import pandas as pd

def parse_arguments():
    parser = argparse.ArgumentParser(description='Test SMB server and users.')
    parser.add_argument('-s', '--server', type=str, help='SMB server IP address')
    parser.add_argument('-l', '--list', type=str, help='Path to CSV file containing user list')
    return parser.parse_args()

def main():
    args = parse_arguments()

    if not args.server:
        print("Error: Please provide the SMB server IP address using -s or --server option.")
        return

    if not args.list:
        print("Error: Please provide the path to the CSV file containing user list using -l or --list option.")
        return

    ################################################################
    ###       extraction de tout les utilisateurs                ###
    ################################################################
    extractname: ExtractName = ExtractName(args.list)
    data: pd.DataFrame = extractname.get_users_list()

    ################################################################
    ###              test sur chaque utilisateurs                ###
    ################################################################
    test_data: list[dict] = []

    for i, rows in data.iterrows():
        testshare: TestShare = TestShare(args.server, rows["utilisateur"], rows["mot de passe"], "/tmp/share")
        print(testshare)
        testshare.run()
        test_data.append(testshare.export())

    # parse the result
    parseresult: ParseResult = ParseResult(test_data)
    parseresult.show()
    parseresult.export("resulat", "Résulat du test de partage de fichier")


if __name__ == "__main__":
    main()

