from colorama import Fore, Style
import xlsxwriter

##########################################################################################################
### Auteur: Djetic Alexandre 
### Description: Cette classe permet d'exporter les données de test au format word 2007+ 
###########################################################################################################

class ParseResult:
    """
    Represents a data parsing result and provides methods for displaying and exporting the data.

    Attributes:
        _data (list[dict]): The list of dictionaries containing parsed data.

    Methods:
        __init__: Initializes ParseResult object with optional data.
        show: Prints the parsed data to the console.
        user_export: Exports parsed data to an Excel file for a specific user.
        export: Exports parsed data to Excel files for all users.
    """

    def __init__(self, data: list[dict] = []) -> None:
        """
        Initializes a ParseResult object.

        Args:
            data (list[dict], optional): The list of dictionaries containing parsed data. Defaults to [].
        """
        self._data: list[dict] = data

    def show(self):
        """
        Prints the parsed data to the console.
        """
        for i, dico in enumerate(self._data):
            print(f"\n{Fore.RED}info général test n°{i + 1}: {Style.RESET_ALL}")
            print("-" * 50)
            print(f"{Fore.RED}serveur{Style.RESET_ALL}: {Fore.GREEN}{dico.get('server', 'NA')}{Style.RESET_ALL}")
            print(f"{Fore.RED}point de montage{Style.RESET_ALL}: {Fore.GREEN}{dico.get('mountpoint', 'NA')}{Style.RESET_ALL}")
            print(f"{Fore.RED}utilisateur{Style.RESET_ALL}: {Fore.GREEN}{dico.get('user', 'NA')}{Style.RESET_ALL}")
            print(f"{Fore.RED}statut{Style.RESET_ALL}: {Fore.GREEN}{dico.get('status', 'NA')}{Style.RESET_ALL}")
            print(f"{Fore.RED}pourcentage de réussite{Style.RESET_ALL}: {Fore.GREEN}{dico.get('success_rate', 'NA')} %{Style.RESET_ALL}")

            j: int = 1
            for step in dico.get("result_step", []):
                print(f"{Fore.RED}étape {j}{Style.RESET_ALL}: {Fore.GREEN}{step['desc']}{Style.RESET_ALL}")
                print(f"- {Fore.RED}status{Style.RESET_ALL}: {Fore.GREEN}{step['status']}{Style.RESET_ALL}")
                j += 1

            print("-" * 50)

    def user_export(self, file: str, data: dict, title: str) -> None:
        """
        Exports parsed data to an Excel file for a specific user.

        Args:
            file (str): The name of the Excel file to export data to.
            data (dict): The dictionary containing parsed data for a specific user.
            title (str): The title of the data being exported.
        """
        # Créer un classeur Excel et ajouter une feuille de travail
        workbook = xlsxwriter.Workbook(file)
        worksheet = workbook.add_worksheet()

        # taille d'une cellule
        worksheet.set_column(f'A:E', 60)

        # Définir le format pour le titre en rouge
        title_format = workbook.add_format({'bold': True, 'font_color': 'red', 'bg_color': '#D3D3D3'})
        gray_background_format = workbook.add_format({'bg_color': '#D3D3D3'})

        # Écrire le titre en rouge
        worksheet.write('A1', title, title_format)
        
        # Écrire du header
        row: int = 2
        worksheet.write(row, 0, 'serveur', gray_background_format)
        worksheet.write(row, 1, data.get("server", 'NA'))

        worksheet.write(row + 1, 0, 'point de montage', gray_background_format)
        worksheet.write(row + 1, 1, data.get("mountpoint", 'NA'))

        worksheet.write(row + 2, 0, 'utilisateur', gray_background_format)
        worksheet.write(row + 2, 1, data.get("user", 'NA'))

        worksheet.write(row + 3, 0, 'statut', gray_background_format)
        worksheet.write(row + 3, 1, data.get("status", 'NA'))

        worksheet.write(row + 4, 0, 'pourcentage de réussite', gray_background_format)
        worksheet.write(row + 4, 1, str(data.get("success_rate", 'NA')) + '%')
        
        # Écrire des détailles de chaque test
        row += 6  # Aller à la prochaine ligne pour le prochain ensemble de données
        worksheet.write(row, 0, "Numéro de test", gray_background_format)
        worksheet.write(row, 1, "Description", gray_background_format)
        worksheet.write(row, 2, "Statut", gray_background_format)

        j: int = 1
        row += 1
        for step in data.get("result_step", []):
            worksheet.write(row, 0, j)
            worksheet.write(row, 1, step.get("desc", 'NA'))
            worksheet.write(row, 2, step.get("status", 'NA'))
            j += 1
            row += 1

        row += 1  # Ajouter une ligne vide entre les enregistrements

        # Fermer le classeur Excel
        workbook.close()
        
    def export(self, prefix: str, title: str) -> None:
        """
        Exports parsed data to Excel files for all users.

        Args:
            prefix (str): The prefix for the Excel file names.
            title (str): The title of the data being exported.
        """
        for dico in self._data:
            self.user_export(f"{prefix}_{dico['user']}.xlsx", dico, title)
            print(f"- {Fore.GREEN}export du résultat de {dico['user']} vers {prefix}_{dico['user']}.xlsx{Style.RESET_ALL}")


if __name__ == "__main__":
    example_data = [
        {
            "server": "192.168.1.100",
            "mountpoint": "/mnt/share",
            "user": "user1",
            "status": "OK",
            "success_rate": 80,
            "result_step": [
                {"step_num": 1, "desc": "Connexion au serveur SMB", "status": "OK"},
                {"step_num": 2, "desc": "Montage du partage", "status": "OK"}
            ]
        },
        {
            "server": "192.168.1.101",
            "mountpoint": "/mnt/share2",
            "user": "user2",
            "status": "NOK",
            "success_rate": 50,
            "result_step": [
                {"step_num": 1, "desc": "Connexion au serveur SMB", "status": "NOK"}
            ]
        }
    ]
    
    parseresult: ParseResult = ParseResult(example_data)
    parseresult.show()
    parseresult.export("resulat", "Résulat du test de partage de fichier")
