from .wrongverboselevel import WrongVerboseLevel
from colorama import Fore, Style
import numpy as np
import xlsxwriter

class DnsResultHandler:
    """
    Class to handle DNS result data.

    Attributes:
        _data (dict): Dictionary containing DNS result data.
        _verbose (int): Verbosity level (0, 1, or 2).
        _title (str): Title for the DNS result data.

    Methods:
        check_verbose_level(): Check if the verbosity level is valid.
    """

    def __init__(self, data: dict, title: str, verbose: int = 0) -> None:
        """
        Initializes DnsResultHandler object.

        Args:
            data (dict): Dictionary containing DNS result data.
            title (str): Title for the DNS result data.
            verbose (int, optional): Verbosity level (0, 1, or 2). Defaults to 0.
        """
        # Vérification du niveau de verbosité
        self.check_verbose_level(verbose)
        self._verbose: int = verbose
    
        #propriété
        self._data: dict = data
        self._title: str = title
    
    def check_verbose_level(self, verbose: int) -> None:
        """
        Check if the verbosity level is valid.

        Args:
            verbose (int): Verbosity level.

        Raises:
            WrongVerboseLevel: If verbosity level is invalid.
        """
        if verbose not in [0, 1, 2]:
            raise WrongVerboseLevel("Donner une version de verbose valide 0, 1 ou 2")

    def verbose(self, zone: str) -> None:
        match self._verbose:
            case 1:
                self.verbose_level_1(zone)
            case 2:
                self.verbose_level_2(zone)
            case _:
                pass

    def verbose_level_1(self, zone: str) -> None:
        """
        Display the results of DNS resolution tests.
        """
        print(f"\n{Fore.RED}informations générale de Résolution{Style.RESET_ALL}: ")
        print("-" * 3)
        print(f"Résolution DNS: {Fore.RED}{zone}{Style.RESET_ALL}")
        print(f"Version: {Fore.RED}{self._data['version']}{Style.RESET_ALL}")
        print(f"Status: {Fore.RED}{'Success' if self._data['status'] else 'Failure'}{Style.RESET_ALL}")
        print(f"Success Rate: {Fore.RED}{self._data['success_rate']:0.2f}%{Style.RESET_ALL}")
        print("-" * 3)

        print(f"\ninformations sur les Résolutions: ")
        print("-" * 3, end='')

        print("\nSuccessful Resolutions:")
        for success in self._data['full_success']:
            print(f"  - {Fore.RED}{success[0]}{Style.RESET_ALL} : {Fore.GREEN}{success[1]}{Style.RESET_ALL} <> obtenue: {Fore.GREEN}{success[2]}{Style.RESET_ALL}, status: {Fore.RED}{success[3]}{Style.RESET_ALL}")

        print("\nFailed Resolutions:")
        for failed in self._data['full_failed_name']:
            print(f"  - {Fore.RED}{failed[0]}{Style.RESET_ALL} : {Fore.GREEN}{failed[1]}{Style.RESET_ALL} <> obtenue: {Fore.BLUE}{failed[2]}{Style.RESET_ALL}, status: {Fore.RED}{failed[3]}{Style.RESET_ALL}")
        print("-" * 3)


    def verbose_level_2(self, zone: str) -> None:
        """
        Display the results of DNS resolution tests.
        """
        print(f"\n{Fore.RED}informations générale de Résolution{Style.RESET_ALL}: ")
        print("-" * 3)
        print(f"Résolution DNS: {Fore.RED}{zone}{Style.RESET_ALL}")
        print(f"Version: {Fore.RED}{self._data['version']}{Style.RESET_ALL}")
        print(f"Status: {Fore.RED}{'Success' if self._data['status'] else 'Failure'}{Style.RESET_ALL}")
        print(f"Success Rate: {Fore.RED}{self._data['success_rate']:0.2f}%{Style.RESET_ALL}")
        print("-" * 3)

        print(f"\ninformations sur les Résolutions: ")
        print("-" * 3, end='')

        print("\nSuccessful Resolutions:")
        for success in self._data['full_success']:
            print(f"  - {Fore.RED}{success[0]}{Style.RESET_ALL} : {Fore.GREEN}{success[1]}{Style.RESET_ALL} <> obtenue: {Fore.GREEN}{success[2]}{Style.RESET_ALL}, status: {Fore.RED}{success[3]}{Style.RESET_ALL}")

        print("\nFailed Resolutions:")
        for failed in self._data['full_failed_name']:
            print(f"  - {Fore.RED}{failed[0]}{Style.RESET_ALL} : {Fore.GREEN}{failed[1]}{Style.RESET_ALL} <> obtenue: {Fore.BLUE}{failed[2]}{Style.RESET_ALL}, status: {Fore.RED}{failed[3]}{Style.RESET_ALL}")
        print("-" * 3)
        
        print(f"\ndétail des resolutions: ")
        print("-" * 3, end='')

        print("\nsuccess Name Resolutions:")
        for success_name in self._data['success_name_record']:
            print(f"  - {Fore.RED}{success_name[0]}{Style.RESET_ALL} : {Fore.GREEN}{success_name[1]}{Style.RESET_ALL} <> obtenue: {Fore.GREEN}{success_name[2]}{Style.RESET_ALL}")

        print("\nFailed Name Resolutions:")
        for failed_name in self._data['failed_name_record']:
            print(f"  - {Fore.RED}{failed_name[0]}{Style.RESET_ALL} : {Fore.GREEN}{failed_name[1]}{Style.RESET_ALL} <> obtenue: {Fore.BLUE}{failed_name[2]}{Style.RESET_ALL}")

        print("\nSuccessful PTR Resolutions:")
        for success_ptr in self._data['success_ptr_record']:
            print(f"  - {Fore.RED}{success_ptr[0]}{Style.RESET_ALL} : {Fore.GREEN}{success_ptr[1]}{Style.RESET_ALL} <> obtenue: {Fore.GREEN}{success_ptr[2]}{Style.RESET_ALL}")

        print("\nFailed PTR Resolutions:")
        for failed_ptr in self._data['failed_ptr_record']:
            print(f"  - {Fore.RED}{failed_ptr[0]}{Style.RESET_ALL} : {Fore.GREEN}{failed_ptr[1]}{Style.RESET_ALL} <> obtenue: {Fore.BLUE}{failed_ptr[2]}{Style.RESET_ALL}")

        print("-" * 3)
    
    def parse_data(self) -> dict:
        """Parse data from self._data["full_success"] and self._data["full_failed_name"].

        Returns a tuple containing two dictionaries:
        - The first dictionary contains parsed data with keys 'nom', 'adresses IP', 'nom inverse', and 'status'.
        - The second dictionary contains parsed data with keys 'nom', 'adresses IP', 'nom inverse', and 'status'.

        Returns:
            tuple[dict, dict]: A tuple containing two dictionaries with parsed data.
        """
        datas = {
            "nom": [], 
            "adresses IP": [],
            "nom inverse": [],
            "status": []
        }
        
        # Extracting data from self._data["full_success"] and self._data["full_failed_name"]
        for data in self._data["full_success"]:
            datas["nom"].append(data[0])
            datas["adresses IP"].append(data[1])
            datas["nom inverse"].append(data[2])
            datas["status"].append(data[3])

        for data in self._data["full_failed_name"]:
            datas["nom"].append(data[0])
            datas["adresses IP"].append(data[1])
            datas["nom inverse"].append(data[2])
            datas["status"].append(data[3])

        return datas

    
    def export(self, prefix: str, title: str) -> None:
        """Export the data to a CSV file.
        
        This function exports the data stored in the object to a CSV file.
        The exported data includes version, status, success rate, full success,
        full failed name, success name record, failed name record, success PTR record,
        and failed PTR record.

        Args:
            file (str): The file path where the CSV file should be saved.
            title (str): The title to include in the CSV file.

        Returns:
            None
        """
        # Créer un classeur Excel et ajouter une feuille de travail
        workbook = xlsxwriter.Workbook(f"{prefix}_{self._data.get('version', 'NA')}.xlsx")
        worksheet = workbook.add_worksheet()

        # espace minimum par cellule
        worksheet.set_column(f'A:E', 60)

        # Définir le format pour le titre en rouge
        title_format = workbook.add_format({'bg_color': '#D3D3D3', 'bold': True, 'font_color': 'red', 'font_size': 16})
        sub_title_format = workbook.add_format({'bold': True, 'font_color': 'red', 'font_size': 14})
        gray_background_format = workbook.add_format({'bg_color': '#D3D3D3', 'font_color': 'red'})

        # Écrire le titre en rouge
        worksheet.write('A1', title, title_format)

        # Écrire du header
        row: int = 2
        worksheet.write(row, 0, 'version', gray_background_format)
        worksheet.write(row, 1, self._data.get("version", 'NA'))

        worksheet.write(row + 1, 0, 'statut', gray_background_format)
        worksheet.write(row + 1, 1, 'Success' if self._data.get('status', False) else 'Failure')

        worksheet.write(row + 2, 0, 'pourcentage de réussite', gray_background_format)
        worksheet.write(row + 2, 1, f"{np.round(self._data.get('success_rate', 'NA'), 2)} %")
        
        # obention des données au bon format
        datas = self.parse_data()

        # Écrire des détailles de chaque test
        row += 5  # Aller à la prochaine ligne pour le prochain ensemble de donné
        worksheet.write(row, 0, 'nom', gray_background_format)
        worksheet.write(row, 1, 'adresses', gray_background_format)
        worksheet.write(row, 2, 'status', gray_background_format)
        
        row += 1 # Aller à la prochaine ligne pour le prochain ensemble de donné
        for i in range(len(datas["nom"])):
            worksheet.write(row + i, 0, datas['nom'][i])
            worksheet.write(row + i, 1, datas['adresses IP'][i])
            worksheet.write(row + i, 2, datas['status'][i])

        # name record detail
        row += len(datas["nom"]) + 1
        worksheet.write(row, 0, "Résulat de résolution de nom ayant fonctionné : ", sub_title_format)
        worksheet.write(row + 1, 0, 'nom', gray_background_format)
        worksheet.write(row + 1, 1, 'adresse IP attendue', gray_background_format)
        worksheet.write(row + 1, 2, 'address IP obtenue', gray_background_format)
        
        row += 3 # Aller à la prochaine ligne pour le prochain ensemble de donné
        for i in range(len(self._data['success_name_record'])):
            worksheet.write(row + i, 0, self._data['success_name_record'][i][0])
            worksheet.write(row + i, 1, self._data['success_name_record'][i][1])
            worksheet.write(row + i, 2, ",".join(self._data['success_name_record'][i][2]))
        
        row += len(self._data['success_name_record']) + 1
        worksheet.write(row, 0, "Résulat de résolution de nom ayant échoué : ", sub_title_format)
        worksheet.write(row + 1, 0, 'nom', gray_background_format)
        worksheet.write(row + 1, 1, 'adresse IP attendue', gray_background_format)
        worksheet.write(row + 1, 2, 'address IP obtenue', gray_background_format)

        row += 3 # Aller à la prochaine ligne pour le prochain ensemble de donné
        for i in range(len(self._data['failed_name_record'])):
            worksheet.write(row + i, 0, self._data['failed_name_record'][i][0])
            worksheet.write(row + i, 1, self._data['failed_name_record'][i][1])
            worksheet.write(row + i, 2, ",".join(self._data['failed_name_record'][i][2]))
        
        row += len(self._data['failed_name_record']) + 1
        
        worksheet.write(row, 0, "Résulat de résolution inverse ayant fonctionnée : ", sub_title_format)

        worksheet.write(row + 1, 0, 'adresses IP', gray_background_format)
        worksheet.write(row + 1, 1, 'nom attendue', gray_background_format)
        worksheet.write(row + 1, 2, 'nom obtenue', gray_background_format)
        
        row += 3
        for i in range(len(self._data['success_ptr_record'])):
            worksheet.write(row + i, 0, self._data['success_ptr_record'][i][0])
            worksheet.write(row + i, 1, self._data['success_ptr_record'][i][1])
            worksheet.write(row + i, 2, self._data['success_ptr_record'][i][2])
        
        row += len(self._data['success_ptr_record']) + 1
        worksheet.write(row, 0, "Résulat de résolution inverse ayant échoué : ", sub_title_format)
        worksheet.write(row + 1, 0, 'adresses IP', gray_background_format)
        worksheet.write(row + 1 , 1, 'nom attendue', gray_background_format)
        worksheet.write(row + 1, 2, 'nom obtenue', gray_background_format)

        row += 1
        for i in range(len(self._data['failed_ptr_record'])):
            worksheet.write(row + i, 0, self._data['failed_ptr_record'][i][0])
            worksheet.write(row + i, 1, self._data['failed_ptr_record'][i][1])
            worksheet.write(row + i, 2, self._data['failed_ptr_record'][i][2])
    

        # Fermer le classeur Excel
        workbook.close()
        print(f"export des résultats vers {prefix}_{self._data.get('version', 'NA')}.xlsx")

