from colorama import Fore, Style
import xlsxwriter

class ParseResult:

    def __init__(self, data: list[dict] = []) -> None:
        self._data: list[dict] = data

    def show(self):
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

        # Créer un classeur Excel et ajouter une feuille de travail
        workbook = xlsxwriter.Workbook(file)
        worksheet = workbook.add_worksheet()

        # taille d'une cellule
        worksheet.set_column(f'A:E', 60)

        # Définir le format pour le titre en rouge
        title_format = workbook.add_format({'bold': True, 'font_color': 'red'})
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
        worksheet.write(row, 0, "numéro de test", gray_background_format)
        worksheet.write(row, 1, "description", gray_background_format)
        worksheet.write(row, 2, "status", gray_background_format)

        row += 1

        for step in data.get("result_step", []):
            worksheet.write(row, 0, str(step.get("step_num", 'NA')))
            worksheet.write(row, 1, step.get("desc", 'NA'))
            worksheet.write(row, 2, step.get("status", 'NA'))
            row += 1

        row += 1  # Ajouter une ligne vide entre les enregistrements

        # Fermer le classeur Excel
        workbook.close()
        
    def export(self, prefix: str, title: str) -> None:
        for dico in self._data:
            self.user_export(f"{prefix}_{dico['user']}.xlsx", dico, title)    


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
