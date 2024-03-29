from .wrongverboselevel import WrongVerboseLevel
#from .csvparser import CsvParser
import csv

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
        print(f"\ninformations générale de Résolution: ")
        print("-" * 3)
        print(f"Résolution DNS: {zone}")
        print(f"Version: {self._data['version']}")
        print(f"Status: {'Success' if self._data['status'] else 'Failure'}")
        print(f"Success Rate: {self._data['success_rate']:0.2f}%")
        print("-" * 3, end='')

        print(f"\ninformations sur les Résolutions: ")
        print("-" * 3, end='')

        print("\nSuccessful Resolutions:")
        for success in self._data['full_success']:
            print(f"  - Name: {success[0]}, IP: {success[1]}, Expected PTR: {success[2]}, status: {success[3]}")

        print("\nFailed Resolutions:")
        for success in self._data['full_failed_name']:
            print(f"  - Name: {success[0]}, IP: {success[1]}, Expected PTR: {success[2]}, status: {success[3]}")
        print("-" * 3)


    def verbose_level_2(self, zone: str) -> None:
        """
        Display the results of DNS resolution tests.
        """
        print(f"\ninformations générale de Résolution: ")
        print("-" * 3)
        print(f"Résolution DNS: {zone}")
        print(f"Version: {self._data['version']}")
        print(f"Status: {'Success' if self._data['status'] else 'Failure'}")
        print(f"Success Rate: {self._data['success_rate']:0.2f}%")
        print("-" * 3)

        print(f"\ninformations sur les Résolutions: ")
        print("-" * 3, end='')

        print("\nSuccessful Resolutions:")
        for success in self._data['full_success']:
            print(f"  - Name: {success[0]}, IP: {success[1]}, Expected PTR: {success[2]}, status: {success[3]}")

        print("\nFailed Resolutions:")
        for success in self._data['full_failed_name']:
            print(f"  - Name: {success[0]}, IP: {success[1]}, Expected PTR: {success[2]}, status: {success[3]}")
        print("-" * 3)
        
        print(f"\ndétail des resolutions: ")
        print("-" * 3, end='')

        print("\nsuccess Name Resolutions:")
        for failed_name in self._data['success_name_record']:
            print(f"  - Failed Name: {failed_name}")

        print("\nFailed Name Resolutions:")
        for failed_name in self._data['failed_name_record']:
            print(f"  - Failed Name: {failed_name}")

        print("\nSuccessful PTR Resolutions:")
        for success_ptr in self._data['success_ptr_record']:
            print(f"  - IP: {success_ptr}")

        print("\nFailed PTR Resolutions:")
        for failed_ptr in self._data['failed_ptr_record']:
            print(f"  - Failed IP: {failed_ptr}")

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

    
    def export(self, file: str, title: str) -> None:
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
        headers = {
            "title": title, 
            "version": self._data["version"],
            "status": self._data["status"],
            "success_rate": self._data["success_rate"]
        }

        datas = self.parse_data()
        
        if file == "resultat_resolution_csv":
            file: str = f"{file}_{self._data['version']}.csv"

        # Writing to CSV file
        with open(file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write headers
            writer.writerow(["Attribute", "Value"])
            for key, value in headers.items():
                writer.writerow([key, value])

            writer.writerow([]) # Separator

            # Write data headers
            writer.writerow(list(datas.keys())) # Data header
            rows = zip(*datas.values())
            writer.writerows(rows) # Data rows
