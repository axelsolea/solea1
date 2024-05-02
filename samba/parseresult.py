from colorama import Fore, Style


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

            for step in dico.get("result_step", []):
                print(f"{Fore.RED}étape {step['step_num']}{Style.RESET_ALL}: {Fore.GREEN}{step['desc']}{Style.RESET_ALL}")
                print(f"- {Fore.RED}status{Style.RESET_ALL}: {Fore.GREEN}{step['status']}{Style.RESET_ALL}")

            print("-" * 50)

    def export(self):
        raise NotImplementedError("la fonctionnalité d'export n'est pas encore implémenter")


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
    parseresult.export()
