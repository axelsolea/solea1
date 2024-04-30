import pandas as pd
from colorama import Fore, Style

class ExtractName:
    """
    This class provides methods to extract and display user data from a CSV file.
    
    Attributes:
        _data (pd.DataFrame): DataFrame to store the extracted user data.
        _file (str): File path of the CSV file.
        _status (int): Status indicator (-1 for uninitialized).
    """

    def __init__(self, file: str) -> None:
        """
        Initializes an instance of ExtractName with the given file path.
        
        Args:
            file (str): File path of the CSV file.
        """
        self._data: pd.DataFrame = pd.DataFrame([])
        self._file: str = file
        self._status: int = -1
    
    def get_users_list(self) -> pd.DataFrame:
        """
        Reads the CSV file and returns a DataFrame containing user data.
        
        Returns:
            pd.DataFrame: DataFrame containing user data.
        
        Raises:
            Exception: If the file does not exist, permission is denied, 
                       or an IO error occurs while reading the file.
        """
        try:
            self._data: pd.DataFrame = pd.read_csv(self._file, delimiter=",", header=1)
            return pd.read_csv(self._file, delimiter=",", header=1)
        except FileNotFoundError as e:
            raise Exception(f"The file does not exist")
        except PermissionError as e:
            raise Exception(f"The current user can't read the file {self._file}")
        except IOError as e:
            raise Exception(f"The file cannot be read...\n{e}")
        except TypeError as e:
            raise Exception(f"The file is not of string type...\n{e}")
    
    def show_data(self) -> None:
        """
        Displays the extracted user data with formatted output.
        
        Prints:
            Usernames, passwords, and groups with corresponding titles in red color,
            and actual data in green color.
        """
        # Update the data to display
        self.get_users_list()

        # Display usernames
        print(f"{Fore.RED}utilisateur:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{self._data['utilisateur'].to_string(index=False)}{Style.RESET_ALL}")
        
        # Display passwords
        print(f"{Fore.RED}mot de passe:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{self._data['mot de passe'].to_string(index=False)}{Style.RESET_ALL}")
        
        # Display groups
        print(f"{Fore.RED}groupe:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{self._data['groupe'].to_string(index=False)}{Style.RESET_ALL}")

if __name__ == "__main__":
    extractname: ExtractName = ExtractName("list_users.csv")
    data: pd.DataFrame = extractname.get_users_list()
    extractname.show_data()

