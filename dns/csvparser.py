import pandas as pd
import sys

class CsvParser:
    """
    Classe pour parser un fichier CSV et afficher ses données.

    Args:
        file (str): Chemin d'accès au fichier CSV.
        column_names (list): Liste des noms de colonnes du fichier CSV.

    Attributes:
        _file (str): Chemin d'accès au fichier CSV.
        _column_names (list): Liste des noms de colonnes du fichier CSV.

    Methods:
        parser(): Lit le fichier CSV et retourne les données sous forme de DataFrame.
        show(): Affiche les données du fichier CSV en utilisant les noms de colonnes spécifiés.
    """

    def __init__(self, file: str, column_names: list):
        """
        Initialise un objet Csvparser.

        Args:
            file (str): Chemin d'accès au fichier CSV.
            column_names (list): Liste des noms de colonnes du fichier CSV.
        """
        self._file: str = file
        self._column_names: list = column_names

    def parser(self) -> pd.DataFrame:
        """
        Lit le fichier CSV et retourne les données sous forme de DataFrame.

        Returns:
            pd.DataFrame: Les données du fichier CSV.
        """
        try: 
            data: pd.DataFrame = pd.read_csv(self._file, header=0, delimiter=',')
        except FileNotFoundError as e:
            print("Le fichier source n'a pas été trouvé...")
            sys.exit(1)
        except Exception as e:
            print(f"Une erreur non supportée est survenue, quitter...\n{e}")
            sys.exit(1)
        
        return data
        
    def show(self, title: str) -> None:
        """
        Affiche les données du fichier CSV en utilisant les noms de colonnes spécifiés.
        """
        print(title)
        for row in self.parser():
            print('| '.join([str(row[column]) for column in self._column_names]))
    
    @classmethod
    def export(cls, df: pd.DataFrame, file: str) -> None:
        """
        Exporte un DataFrame pandas vers un fichier CSV.

        Args:
            df (pd.DataFrame): Le DataFrame à exporter.
            file (str): Chemin d'accès du fichier CSV de destination.
        """
        try:
            df.to_csv(file, index=False, encoding='utf-8', sep=',')
            print(f"Exportation réussie vers '{file}'")
        except Exception as e:
            print(f"Une erreur est survenue lors de l'exportation : {e}")
    
    @property
    def file(self):
        """The file property."""
        return self._file
    @file.setter
    def file(self, value: str):
        self._file = value

    @property
    def column_names(self):
        """The column_names property."""
        return self._column_names
    @column_names.setter
    def column_names(self, value):
        self._column_names = value
