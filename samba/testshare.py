from colorama import Fore, Style
from filemanager import FileManager
from ping import Ping
from mountshare import MountShare
import sys
import logging
import logging.config
import json
import numpy as np

##########################################################################################################
### Auteur: Djetic Alexandre 
### Description: Cette classe permet de tester un partage et d'exporter les donnée au format dictionnaire
###########################################################################################################


class TestShare:
    """
    Class for testing a share functionality.

    Attributes:
        server (str): The server IP or hostname.
        user (str): The username for authentication.
        passwd (str): The password for authentication.
        mount_point (str): The mount point for the share.
        _total (int): Total number of test steps.
        _cpt (int): Counter for successful test steps.
        _data (dict): Dictionary to store test data.
        _success_rate (float): Success rate of the test.
        _ping (Ping): Instance of Ping class for checking server accessibility.
        _mountshare (MountShare): Instance of MountShare class for mounting shares.
        _logger: Logger instance for logging events.

    Methods:
        __init__(self, server: str, user: str, passwd: str, mount_point: str) -> None:
            Initializes TestShare instance with provided server, user, password, and mount point.

        __repr__(self) -> str:
            Returns a string representation of TestShare instance.

        is_accessible(self) -> bool:
            Checks if the server is accessible.

        create_dir(self, name: str) -> bool:
            Creates a directory with the given name.

        delete_dir(self, name: str) -> bool:
            Deletes the directory with the given name.

        create_file(self, name: str, content="") -> bool:
            Creates a file with the given name and optional content.

        read_file(self, name: str, expect: str = "") -> bool:
            Reads the contents of the file with the given name and compares it with the expected content.

        mount(self, share_name: str) -> bool:
            Mounts the share with the given name.

        umount(self) -> bool:
            Unmounts the share.

        run(self) -> None:
            Runs the test steps including server connectivity check, directory creation, file creation,
            file reading, share mounting, unmounting, and directory deletion. Calculates the success rate.

        export(self) -> dict:
            Exports the test results as a dictionary.

    Usage:
        testshare = TestShare("1.1.1.1", "user", "password", "/mnt/share")
        testshare.run()
        results = testshare.export()
    """

    def __init__(self, server: str, user: str, passwd: str, mount_point: str) -> None:
        self._server: str = server
        self._user: str = user
        self._passwd: str = passwd
        self._mount_point: str = mount_point
        self._total: int = 7
        self._cpt: int = 0
        self._data: list = []
        self._success_rate: float = 0.0
        self._ping: Ping = Ping(server)
        self._mountshare: MountShare = MountShare(server, mount_point)
        self._filemanager: FileManager = FileManager(mount_point)

    def __repr__(self) -> str:
        return f"{Fore.RED}Information du test:{Style.RESET_ALL}\n{'-' * 25 }\n{Fore.RED}serveur{Style.RESET_ALL}: {self._server}\n{Fore.RED}utilisateur{Style.RESET_ALL}: {self._user}\n{Fore.RED}mot de passe{Style.RESET_ALL}: {self._passwd}\n{Fore.RED}point de montage: {Style.RESET_ALL}: {self._mount_point}\n{'-' * 25}"

    def is_accessible(self) -> bool:
        """
        Checks if the server is accessible.
        """
        failed_rate, rcode = self._ping.send_ping()
        return failed_rate == 0 and rcode == 0

    def create_dir(self, name: str = "") -> bool:
        """
        Creates a directory with the given name.
        """
        if not name:
            return self._filemanager.create_dir()
        else: 
            return self._filemanager.create_dir(name)

    def delete_dir(self, name: str = "") -> bool:
        """
        Deletes the directory with the given name.
        """
        if not name:
            return self._filemanager.delete_dir()
        else: 
            return self._filemanager.delete_dir(name)

    def create_file(self, name: str, content="") -> bool:
        """
        Creates a file with the given name and optional content.
        """
        return self._filemanager.create_file(name, content)

    def read_file(self, name: str, expect: str = "") -> bool:
        """
        Reads the contents of the file with the given name and compares it with the expected content.
        """
        return self._filemanager.read_file(name) == expect

    def mount(self, share_name: str) -> bool:
        """
        Mounts the share with the given name.
        """
        output, rcode, stderr = self._mountshare.mount(share_name, self._user, self._passwd)
        return rcode == 0 and stderr == ""

    def umount(self) -> bool:
        """
        Unmounts the share.
        """
        output, rcode, stderr = self._mountshare.umount()
        return rcode == 0 and stderr == ""

    def run(self) -> None:
        """
        Runs the test steps including server connectivity check, directory creation, file creation,
        file reading, share mounting, unmounting, and directory deletion. Calculates the success rate.
        """

        # Connectivité vers le serveur
        if self.is_accessible():
            self._cpt += 1
            self._data.append({"desc": "Test de connection au serveur smb", "status": "OK"})
        else:
            self._data.append({"desc": "Test de connection au serveur smb", "status": "NOK"})

        # création du dossier de partage
        if self.create_dir():
            self._cpt += 1
            self._data.append({"desc": "Création du fichier de partage", "status": "OK"})
        else:
            self._data.append({"desc": "Création du fichier de partage", "status": "NOK"})

        # point de montage de la machine
        if self.mount("solea_document"):
            self._cpt += 1
            self._data.append({"desc": f"Montage du dossier {self._mount_point} au partage de fichier", "status": "OK"})
        else:
            self._data.append({"desc": f"Montage du dossier {self._mount_point} au partage de fichier", "status": "NOK"})

        # Création d'un fichier utilisateur sur le partage
        if self.create_file(f"{self._user}.txt", f"contenue de {self._user}"):
            self._cpt += 1
            self._data.append({"desc": f"Création d'un fichier text {self._user}.txt", "status": "OK"})
        else:
            self._data.append({"desc": f"Création d'un fichier text {self._user}.txt", "status": "NOK"})

        # Lecture du fichier utilisateur sur le partage
        if self.read_file(f"{self._user}.txt", f"contenue de {self._user}"):
            self._cpt += 1
            self._data.append({"desc": f"Lecture d'un fichier text {self._user}.txt avec le contenu: 'contenue de {self._user}'", "status": "OK"})
        else:
            self._data.append({"desc": f"Lecture d'un fichier text {self._user}.txt avec le contenu: 'contenue de {self._user}'", "status": "NOK"})

        # Suppression du point de montage
        if self.umount():
            self._cpt += 1
            self._data.append({"desc": f"Démontage du dossier de partage {self._mount_point}", "status": "OK"})
        else:
            self._data.append({"desc": f"Démontage du dossier de partage {self._mount_point}", "status": "NOK"})

        # Suppression du dossier de partage
        if self.delete_dir():
            self._cpt += 1
            self._data.append({"desc": "suppression du dossier de partage", "status": "OK"})
        else:
            self._data.append({"desc": "suppression du dossier de partage", "status": "NOK"})

        # Calculate success rate
        self._success_rate: int = np.round(self._cpt / self._total, 3) * 100

    def export(self) -> dict:
        """
        Exports the test results as a dictionary.
        """
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
    testshare: TestShare = TestShare("172.18.0.251", "alexandre", "Solea05alexandre", "/tmp/share")
    testshare.run()
    print(testshare.export())

