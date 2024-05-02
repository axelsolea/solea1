from colorama import Fore, Style
from iofile import IoFile
from ping import Ping
from mountshare import MountShare
import sys
import logging
import logging.config
import json
import numpy as np

class TestShare:

    def __init__(self, server: str, user: str, passwd: str, mount_point: str) -> None:
        self._server: str = server
        self._user: str = user
        self._passwd: str = passwd
        self._mount_point: str = mount_point
        self._total: int = 5
        self._cpt: int = 0
        self._data: dict = {}
        self._success_rate: float = 0.0
        self._ping: Ping = Ping(server)
        self._mountshare: MountShare = MountShare(server, mount_point)

        if not IoFile.check_exist('logging_config.json'):
            print("logging_config.json cannot exist or not readable")
            sys.exit(1)

        with open('logging_config.json', 'r') as f:
            config: dict = json.load(f)

        logging.config.dictConfig(config)
        self._logger = logging.getLogger(__name__)

    def __repr__(self) -> str:
        return f"{Fore.RED}Information du test:{Style.RESET_ALL}\n{'-' * 25 }\n{Fore.RED}server{Style.RESET_ALL}: {self._server}\n{Fore.RED}utilisateur{Style.RESET_ALL}: {self._user}\n{Fore.RED}mot de passe{Style.RESET_ALL}: {self._passwd}\n{Fore.RED}point de montage: {Style.RESET_ALL}: {self._mount_point}\n{'-' * 25}"
    
    def is_accessible(self) -> bool:
        failed_rate, rcode = self._ping.send_ping()
        return failed_rate == 0 and rcode == 0

    def create_dir(self, name: str) -> bool:
        return IoFile.create_dir(name)

    def delete_dir(self, name: str) -> bool:
        return IoFile.delete_dir(name)

    def create_file(self, name: str, content="") -> bool:
        return IoFile.create_file(name, content)

    def read_file(self, name: str, expect: str = "") -> bool:
        return IoFile.read_file(name) == expect
    
    def mount(self, share_name: str) -> bool:
        output, rcode = self._mountshare.mount(share_name, self._user, self._passwd)
        return rcode == 0

    def umount(self) -> bool:
        output, rcode = self._mountshare.umount()
        return rcode == 0

    def reset_test_data(self) -> None:
        self._data: dict = {}
    
    def run(self) -> None:
        # Connectivité vers le serveur
        if self.is_accessible():
            self._cpt += 1
            self._logger.info("connection to serveur smb...")
        else:
            self._logger.error("impossible to ping the server smb...")

        # création du dossier de partage
        if self.create_dir(self._mount_point):
            self._cpt += 1
            self._logger.info("share directory is created...")
        else:
            self._logger.error("share directory can't be created...")

        # point de montage de la machine
        if self.mount("solea_document"):
            self._cpt += 1
            self._logger.info(f"mount the directory {self._mount_point} to the share file... OK")
        else:
            self._logger.info(f"mount the directory {self._mount_point} to the share file... NOK")

        # Création d'une fichier utilisateur sur le partage
        if self.create_file(f"{self._user}.txt", f"contenue de {self._user}"):
            self._cpt += 1
            self._logger.info(f"création d'un fichier text {self._user}.txt ... OK")
        else:
            self._logger.info(f"création d'un fichier text {self._user}.txt ... NOK")

        # Lecture du fichier utilisateur sur le partage
        if self.read_file(f"{self._user}.txt", f"contenue de {self._user}"):
            self._cpt += 1
            self._logger.info(f"lecture d'un fichier text {self._user}.txt avec le contenue: 'contenue de {self._user}'... OK")
        else:
            self._logger.info(f"lecture d'un fichier text {self._user}.txt avec le contenue: 'contenue de {self._user}'... NOK")

        # Suppression du point de montage
        if self.umount():
            self._cpt += 1
            self._logger.info("unmount the directory from the share file... OK")
        else:
            self._logger.error("unmount the directory from the share file... NOK")

        # Suppression du dossier de partage
        if self.delete_dir(self._mount_point):
            self._cpt += 1
            self._logger.info("delete the share directory... OK")
        else:
            self._logger.error("delete the share directory... NOK")

        self.success_rate: int = np.round(self._cpt / self._total, 3)

    def export(self) -> dict:
        return {
            "user": self._user,
            "password": self._passwd,
            "server": self._server,
            "mountpoint": self._mount_point,
            "status": "OK" if self._cpt == self._total else "NOK",
            "success_rate": self._success_rate,
            "result_step": self._data
        }


if __name__ == "__main__":
    testshare: TestShare = TestShare("1.1.1.1", "alexandre", "Solea05alexandre", "/tmp")
    print(testshare)
    testshare.is_accessible()

