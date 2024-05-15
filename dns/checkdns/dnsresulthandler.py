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
    
        # Propriétés
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
            raise WrongVerboseLevel("Donner une valeur de verbosité valide: 0, 1 ou 2")

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
        print(f"\n{Fore.RED}Informations générales de résolution{Style.RESET_ALL}: ")
        print("-" * 30)
        print(f"Résolution DNS: {Fore.RED}{zone}{Style.RESET_ALL}")
        print(f"Version: {Fore.RED}{self._data['version']}{Style.RESET_ALL}")
        print(f"Statut: {Fore.RED}{'Succès' if self._data['status'] else 'Échec'}{Style.RESET_ALL}")
        print(f"Taux de réussite: {Fore.RED}{self._data['success_rate']:0.2f}%{Style.RESET_ALL}")
        print("-" * 30)

        print(f"\nInformations sur les résolutions: ")
        print("-" * 30, end='')

        print("\nRésolu avec succès:")
        for success in self._data['full_success']:
            print(f"  - {Fore.RED}{success[0]}{Style.RESET_ALL} : {Fore.GREEN}{success[1]}{Style.RESET_ALL} <> obtenue: {Fore.GREEN}{success[2]}{Style.RESET_ALL}, statut: {Fore.RED}{success[3]}{Style.RESET_ALL}")

        print("\nRésolutions échouées:")
        if not self._data['full_failed_name']:
            print(f"- {Fore.RED} Aucune résolution n'a échoué ! {Style.RESET_ALL}") 
        else:
            for failed in self._data['full_failed_name']:
                print(f"  - {Fore.RED}{failed[0]}{Style.RESET_ALL} : {Fore.GREEN}{failed[1]}{Style.RESET_ALL} <> obtenue: {Fore.BLUE}{failed[2]}{Style.RESET_ALL}, statut: {Fore.RED}{failed[3]}{Style.RESETALL}")
        print("-" * 30)

    def verbose_level_2(self, zone: str) -> None:
        """
        Display the results of DNS resolution tests.
        """
        print(f"\n{Fore.RED}Informations générales de résolution{Style.RESET_ALL}: ")
        print("-" * 30)
        print(f"Résolution DNS: {Fore.RED}{zone}{Style.RESET_ALL}")
        print(f"Version: {Fore.RED}{self._data['version']}{Style.RESETALL}")
        print(f"Statut: {Fore.RED}{'Succès' if self._data['status'] else 'Échec'}{Style.RESETALL}")
        print(f"Taux de réussite: {Fore.RED}{self._data['success_rate']:0.2f}%{Style.RESETALL}")
        print("-" * 30)

        print(f"\nInformations sur les résolutions: ")
        print("-" * 30, end='')

        print("\nRésolu avec succès:")
        for success in self._data['full_success']:
            print(f"  - {Fore.RED}{success[0]}{Style.RESETALL} : {Fore.GREEN}{success[1]}{Style.RESETALL} <> obtenue: {Fore.GREEN}{success[2]}{Style.RESETALL}, statut: {Fore.RED}{success[3]}{Style.RESETALL}")

        print("\nRésolutions échouées:")
        if not self._data['full_failed_name']:
            print(f"- {Fore.RED} Aucune résolution n'a échoué ! {Style.RESETALL}") 
        else:
            for failed in self._data['full_failed_name']:
                print(f"  - {Fore.RED}{failed[0]}{Style.RESETALL} : {Fore.GREEN}{failed[1]}{Style.RESETALL} <> obtenue: {Fore.BLUE}{failed[2]}{Style.RESETALL}, statut: {Fore.RED}{failed[3]}{Style.RESETALL}")
        print("-" * 30)
        
        print(f"\nDétails des résolutions: ")
        print("-" * 30, end='')

        print("\nRésolution de noms avec succès:")
        if not self._data['success_name_record']:
            print(f"- {Fore.RED} Aucune résolution d'enregistrement de type A ou AAAA n'a été un succès ! {Style.RESETALL}")
        else:
            for success_name in self._data['success_name_record']:
                print(f"  - {Fore.RED}{success_name[0]}{Style.RESETALL} : {Fore.GREEN}{success_name[1]}{Style.RESETALL} <> obtenue: {Fore.GREEN}{success_name[2]}{Style.RESETALL}")

        print("\nRésolution de noms ayant échoué: ")
        if not self._data['failed_name_record']:
            print(f"- {Fore.RED} Aucune résolution d'enregistrement de type A ou AAAA n'a échoué ! {Style.RESETALL}")
        else:
            for failed_name in self._data['failed_name_record']:
                print(f"  - {Fore.RED}{failed_name[0]}{Style.RESETALL} : {Fore.GREEN}{failed_name[1]}{Style.RESETALL} <> obtenue: {Fore.BLUE}{failed_name[2]}{Style.RESETALL}")
        
        print("\nRésolution inverse avec succès:")
        if not self._data['success_ptr_record']:
            print(f"- {Fore.RED} Aucune résolution d'enregistrement de type PTR n'a été un succès ! {Style.RESETALL}")
        else:
            for success_ptr in self._data['success_ptr_record']:
                print(f"  - {Fore.RED}{success_ptr[0]}{Style.RESETALL} : {Fore.GREEN}{success_ptr[1]}{Style.RESETALL} <> obtenue: {Fore.GREEN}{success_ptr[2]}{Style.RESETALL}")
        
        print("\nRésolution inverse ayant échoué: ")
        if not self._data['failed_ptr_record']:
            print(f"- {Fore.RED} Aucune résolution d'enregistrement de type PTR n'a échoué ! {Style.RESETALL}")
        else:
            for failed_ptr in self._data['failed_ptr_record']:
                print(f"  - {Fore.RED}{failed_ptr[0]}{Style.RESETALL} : {Fore.GREEN}{failed_ptr[1]}{Style.RESETALL} <> obtenue: {Fore.BLUE}{failed_ptr[2]}{Style.RESETALL}")
        print("-" * 30)

    def parse_data(self) -> dict:
        """Parse data from self._data["full_success"] and self._data["full_failed_name"].

        Returns a tuple containing two dictionaries:
        - The first dictionary contains parsed data with keys 'nom', 'adresses IP', 'nom inverse', and 'statut'.
        - The second dictionary contains parsed data with keys 'nom', 'adresses IP', 'nom inverse', and 'statut'.

        Returns:
            tuple[dict, dict]: A tuple containing two dictionaries with parsed data.
        """
        datas = {
            "nom": [], 
            "adresses IP": [],
            "nom inverse": [],
            "statut": []
        }
        
        # Extracting data from self._data["full_success"] and self._data["full_failed_name"]
        for data in self._data["full_success"]:
            datas["nom"].append(data[0])
            datas["adresses IP"].append(data[1])
            datas["nom inverse"].append(data[2])
            datas["statut"].append(data[3])

        for data in self._data["full_failed_name"]:
            datas["nom"].append(data[0])
            datas["adresses IP"].append(data[1])
            datas["nom inverse"].append(data[2])
            datas["statut"].append(data[3])

        return datas

    def export(self, prefix: str, title: str) -> None:
        """Export the data to a CSV file.
        
        This function exports the data stored in the object to a CSV file.
        The exported data includes version, status, success rate, full success,
        full failed name, success name record, failed name record, success PTR record,
        and failed PTR record.

        Args:
            prefix (str): The file path prefix where the CSV file should be saved.
            title (str): The title to include in the CSV file.

        Returns:
            None
        """
        # Créer un classeur Excel et ajouter une feuille de travail
        workbook = xlsxwriter.Workbook(f"{prefix}_{self._data.get('version', 'NA')}.xlsx")
        worksheet = workbook.add_worksheet()

        # Espace minimum par cellule
        worksheet.set_column(f'A:E', 60)

        # Définir le format pour le titre en rouge
        title_format = workbook.add_format({'bg_color': '#D3D3D3', 'bold': True, 'font_color': 'red', 'font_size': 16})
        sub_title_format = workbook.add_format({'bold': True, 'font_color': 'red', 'font_size': 14})
        gray_background_format = workbook.add_format({'bg_color': '#D3D3D3', 'font_color': 'red'})

        # Écrire le titre en rouge
        worksheet.write('A1', title, title_format)

        # Écrire le header
        row: int = 2
        worksheet.write(row, 0, 'version', gray_background_format)
        worksheet.write(row, 1, self._data.get("version", 'NA'))

        worksheet.write(row + 1, 0, 'statut', gray_background_format)
        worksheet.write(row + 1, 1, 'Succès' if self._data.get('status', False) else 'Échec')

        worksheet.write(row + 2, 0, 'pourcentage de réussite', gray_background_format)
        worksheet.write(row + 2, 1, f"{np.round(self._data.get('success_rate', 'NA'), 2)} %")
        
        # Obtention des données au bon format
        datas = self.parse_data()

        # Écrire des détails de chaque test
        row += 5  # Aller à la prochaine ligne pour le prochain ensemble de données
        worksheet.write(row, 0, 'nom', gray_background_format)
        worksheet.write(row, 1, 'adresses', gray_background_format)
        worksheet.write(row, 2, 'statut', gray_background_format)
        
        row += 1 # Aller à la prochaine ligne pour le prochain ensemble de données
        for i in range(len(datas["nom"])):
            worksheet.write(row + i, 0, datas['nom'][i])
            worksheet.write(row + i, 1, datas['adresses IP'][i])
            worksheet.write(row + i, 2, datas['statut'][i])

        # Name record detail
        row += len(datas["nom"]) + 1
        worksheet.write(row, 0, "Résultat de résolution de nom ayant fonctionné : ", sub_title_format)
        worksheet.write(row + 1, 0, 'nom', gray_background_format)
        worksheet.write(row + 1, 1, 'adresse IP attendue', gray_background_format)
        worksheet.write(row + 1, 2, 'adresse IP obtenue', gray_background_format)
        
        row += 2 # Aller à la prochaine ligne pour le prochain ensemble de données
        for i in range(len(self._data['success_name_record'])):
            worksheet.write(row + i, 0, self._data['success_name_record'][i][0])
            worksheet.write(row + i, 1, self._data['success_name_record'][i][1])
            worksheet.write(row + i, 2, ",".join(self._data['success_name_record'][i][2]))
        
        row += len(self._data['success_name_record']) + 1
        worksheet.write(row, 0, "Résultat de résolution de nom ayant échoué : ", sub_title_format)
        worksheet.write(row + 1, 0, 'nom', gray_background_format)
        worksheet.write(row + 1, 1, 'adresse IP attendue', gray_background_format)
        worksheet.write(row + 1, 2, 'adresse IP obtenue', gray_background_format)

        row += 2 # Aller à la prochaine ligne pour le prochain ensemble de données
        for i in range(len(self._data['failed_name_record'])):
            worksheet.write(row + i, 0, self._data['failed_name_record'][i][0])
            worksheet.write(row + i, 1, self._data['failed_name_record'][i][1])
            worksheet.write(row + i, 2, ",".join(self._data['failed_name_record'][i][2]))
        
        row += len(self._data['failed_name_record']) + 1
        
        worksheet.write(row, 0, "Résultat de résolution inverse ayant fonctionné : ", sub_title_format)

        worksheet.write(row + 1, 0, 'adresses IP', gray_background_format)
        worksheet.write(row + 1, 1, 'nom attendu', gray_background_format)
        worksheet.write(row + 1, 2, 'nom obtenu', gray_background_format)
        
        row += 2
        for i in range(len(self._data['success_ptr_record'])):
            worksheet.write(row + i, 0, self._data['success_ptr_record'][i][0])
            worksheet.write(row + i, 1, self._data['success_ptr_record'][i][1])
            worksheet.write(row + i, 2, self._data['success_ptr_record'][i][2])
        
        row += len(self._data['success_ptr_record']) + 1
        worksheet.write(row, 0, "Résultat de résolution inverse ayant échoué : ", sub_title_format)
        worksheet.write(row + 1, 0, 'adresses IP', gray_background_format)
        worksheet.write(row + 1 , 1, 'nom attendu', gray_background_format)
        worksheet.write(row + 1, 2, 'nom obtenu', gray_background_format)

        row += 2
        for i in range(len(self._data['failed_ptr_record'])):
            worksheet.write(row + i, 0, self._data['failed_ptr_record'][i][0])
            worksheet.write(row + i, 1, self._data['failed_ptr_record'][i][1])
            worksheet.write(row + i, 2, self._data['failed_ptr_record'][i][2])
    

        # Fermer le classeur Excel
        workbook.close()
        print(f"Export des résultats vers {prefix}_{self._data.get('version', 'NA')}.xlsx")
