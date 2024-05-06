import xlsxwriter
from xlsxwriter.workbook import Workbook

class ExportResultXlsx:
    """
    Classe pour exporter des données vers un fichier Excel avec des fonctionnalités supplémentaires.
    """

    def __init__(self, file: str) -> None:
        """
        Initialise un nouvel objet ExportResult.

        Args:
            file (str): Le chemin du fichier Excel dans lequel les données seront exportées.
        """
        self._file: str = file
        self._current_cell: str = "A1"
        self._workbook = xlsxwriter.Workbook(file)
        self._worksheet = self._workbook.add_worksheet()
        self._title_format = self._workbook.add_format({'bold': True, 'font_color': 'red', 'font_size': 16})
        self._gray_background_format = self._workbook.add_format({'bg_color': '#D3D3D3'})
        self._default_style = None

    def set_main_title(self, title: str, cell: str = "") -> None:
        """
        Ajoute un titre principal à la feuille de travail.

        Args:
            title (str): Le titre principal à ajouter.
            cell (str): La cellule dans laquelle ajouter le titre. Par défaut, la première cellule (A1).
        """
        self._add_cell(title, cell=cell, style=self._title_format)
        self._update_current_cell_row()

    def add_column(self, data: list, cell: str = "", apply: list = []) -> None:
        """
        Ajoute une colonne de données à la feuille de travail.

        Args:
            data (list): Les données à ajouter.
            cell (str): La cellule dans laquelle commencer à ajouter les données. Par défaut, la cellule actuelle.
            apply (list): Liste des indices des colonnes auxquelles appliquer le style spécifié. Par défaut, aucune colonne n'a de style personnalisé.
        """
        if not apply:
            for i, item in enumerate(data):
                self._add_cell(item, cell=cell)

        for i, item in enumerate(data):
            if self._check_apply(i, apply):
                self._add_cell(item, cell=self._current_cell, style=self._gray_background_format)
            else:
                self._add_cell(item, cell=cell)

            self._update_current_cell_row()

        self._update_current_cell_column()

    def add_row(self, data: list, cell: str = "", apply: list = []) -> None:
        """
        Ajoute une ligne de données à la feuille de travail.

        Args:
            data (list): Les données à ajouter.
            cell (str): La cellule dans laquelle commencer à ajouter les données. Par défaut, la cellule actuelle.
            apply (list): Liste des indices des colonnes auxquelles appliquer le style spécifié. Par défaut, aucune colonne n'a de style personnalisé.
        """
        if not apply:
            for i, item in enumerate(data):
                self._add_cell(item, cell=cell)

        for i, item in enumerate(data):
            if self._check_apply(i, apply):
                self._add_cell(item, cell=self._current_cell, style=self._gray_background_format)
            else:
                self._add_cell(item, cell=cell)

            self._update_current_cell_column()

    def add_blank_line(self, cell: str = "") -> None:
        """
        Ajoute une ligne vide à la feuille de travail Excel.

        Args:
            cell (str, optional): La cellule dans laquelle ajouter la ligne vide.
                Si non spécifié, la ligne vide sera ajoutée à la cellule courante.
                Par défaut, "".

        Note:
            Si `cell` est spécifié, la ligne vide sera ajoutée à la cellule spécifiée.
            Sinon, la ligne vide sera ajoutée à la cellule courante.

        """
        self._add_cell("", cell=cell)

    def _add_cell(self, data: any, style: any = None, cell: str = "") -> None:
        """
        Ajoute une cellule de données à la feuille de travail.

        Args:
            data (any): Les données à ajouter.
            style (any): Le style des données. Par défaut, aucun style n'est appliqué.
            cell (str): La cellule dans laquelle ajouter les données. Par défaut, la cellule actuelle.
        """
        if not cell:
            self._worksheet.write(self._current_cell, data, style)
            self._update_current_cell_row()
        else:
            self.check_cell(cell)
            self._worksheet.write(cell, data, style)

    def close(self) -> None:
        """
        Ferme le classeur Excel.
        """
        self._workbook.close()

    @staticmethod
    def check_cell(cell: str) -> None:
        """
        Vérifie si la cellule spécifiée est valide.

        Args:
            cell (str): La cellule à vérifier.

        Raises:
            ValueError: Si la cellule spécifiée est vide ou non valide.
        """
        if not cell:
            raise ValueError("La cellule spécifiée est vide...")
        elif not cell[0].isupper():
            raise ValueError("La cellule spécifiée est en dehors des limites ou non valide...")

    def _check_apply(self, index: int, apply_style: list) -> bool:
        """
        Vérifie si la cellule spécifiée est comptée dans le style.

        Args:
            index (int): L'indice de la colonne à vérifier.
            apply_style (list): Liste des indices des colonnes auxquelles appliquer le style spécifié.

        Returns:
            bool: True si la cellule est comptée dans le style, False sinon.
        """
        return index in apply_style

    def _update_current_cell_row(self) -> None:
        """
        Met à jour la cellule actuelle en déplaçant le curseur vers le bas d'une rangée.

        La cellule actuelle est représentée par l'attribut _current_cell de la classe. Cette méthode
        incrémente le chiffre de la cellule actuelle d'une unité, en la faisant passer à la rangée suivante.
        """
        self._current_cell: str = f"{chr(ord(self._current_cell[0]) + 1)}1"

    def  _update_current_cell_column(self) -> None:
        """
        Met à jour la cellule actuelle en déplaçant le curseur vers la droite d'une colonne.

        La cellule actuelle est représentée par l'attribut _current_cell de la classe. Cette méthode
        incrémente la lettre de la cellule actuelle d'une unité, en la faisant passer à la colonne suivante.
        """
        self._current_cell: str = f"{self._current_cell[0]}{int(self._current_cell[1]) + 1}"

    @property
    def workbook(self):
        return self._workbook

    @workbook.setter
    def workbook(self, workbook):
        self._workbook = workbook

