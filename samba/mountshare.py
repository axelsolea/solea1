from errorfilenotfound import ErrorFileNotFound
from permissionerror import PermissionError
from colorama import Fore, Style
import subprocess
import os


class MountShare:
    """
    A class for mounting and unmounting Samba shares.

    This class provides methods to mount and unmount Samba shares on a local system.

    Attributes:
        server (str): The IP address or hostname of the Samba server.
        mount_point (str): The directory where the Samba share will be mounted.

    Methods:
        __init__(self, server: str, mount_point: str) -> None:
            Initializes a new MountShare instance.

        __repr__(self) -> str:
            Returns a string representation of the MountShare object.

        check_mount_point_exist(self) -> bool:
            Checks if the mount point directory exists.

        create_mount_point(self) -> None:
            Creates the mount point directory if it does not exist.

        mount(self, share_name: str, user: str, passwd: str) -> tuple[str, int]:
            Mounts the specified Samba share to the mount point.

        umount(self) -> tuple[str, int]:
            Unmounts the Samba share from the mount point.

    Raises:
        ErrorFileNotFound: If the mount point directory does not exist.
    """

    def __init__(self, server: str, mount_point: str) -> None:
        """
        Initializes a new MountShare instance.

        Args:
            server (str): The IP address or hostname of the Samba server.
            mount_point (str): The directory where the Samba share will be mounted.
        """
        self._server: str = server
        self._mount_point: str = mount_point
        self.create_mount_point()

    def __repr__(self) -> str:
        """
        Returns a string representation of the MountShare object.

        Returns:
            str: A formatted string containing information about the mount point.
        """
        return f"Information du point de montage:\n{'-' * 30}\n{Fore.RED}server : {Fore.GREEN}{self._server}{Style.RESET_ALL}\n{Fore.RED}point de montage : {Fore.GREEN}{self._mount_point}{Style.RESET_ALL}\n{'-' * 30}"

    def check_mount_point_exist(self) -> bool:
        """
        Checks if the mount point directory exists.

        Returns:
            bool: True if the mount point directory exists, False otherwise.
        """
        return os.path.exists(self._mount_point)

    def create_mount_point(self) -> None:
        """
        Creates the mount point directory if it does not exist.
        """
        if not self.check_mount_point_exist():
            os.makedirs(self._mount_point)

    def has_sudo_access(self) -> bool:
        """
        Checks if the user has sudo/root access.

        Returns:
            bool: True if sudo/root access is enabled, False otherwise.
        """
        try:
            subprocess.run(["sudo", "-n", "true"], check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def mount(self, share_name: str, user: str, passwd: str) -> tuple[str, int]:
        """
        Mounts the specified Samba share to the mount point.

        Args:
            share_name (str): The name of the Samba share.
            user (str): The Samba username.
            passwd (str): The Samba password.

        Returns:
            tuple[str, int]: A tuple containing the mount command output and return code.

        Raises:
            ErrorFileNotFound: If the mount point directory does not exist.
            ValueError: If the Samba user does not exist.
        """
        if not self.has_sudo_access():
            raise PermissionError("Sudo/root access is required to mount shares.")

        if not self.check_mount_point_exist():
            raise ErrorFileNotFound(f"le point de montage {self._mount_point} n'éxiste pas dans le système de fichier")

        # Check if Samba user exists
        try:
            subprocess.run(["id", user], check=True)
        except subprocess.CalledProcessError:
            raise ValueError(f"Samba user '{user}' does not exist.")

        # Mount the share
        result = subprocess.run(["sudo", "mount", "-t", "cifs", f"//{self._server}/{share_name}", self._mount_point, "-o", f"username='{user}',password='{passwd}'"],
            capture_output=True,
            text=True
        )

        return result.stdout, result.returncode

    def umount(self) -> tuple[str, int]:
        """
        Unmounts the Samba share from the mount point.

        Returns:
            tuple[str, int]: A tuple containing the umount command output and return code.

        Raises:
            ErrorFileNotFound: If the mount point directory does not exist.
        """
        if not self.has_sudo_access():
            raise PermissionError("Sudo/root access is required to unmount shares.")

        if not self.check_mount_point_exist():
            raise ErrorFileNotFound(f"le point de montage {self._mount_point} n'éxiste pas dans le système de fichier")

        result = subprocess.run(["sudo", "umount", self._mount_point], capture_output=True, text=True)
        return result.stdout, result.returncode


if __name__ == "__main__":
    mountshare: MountShare = MountShare("172.18.0.251", "/tmp/share")
    print(mountshare)

    ##################################################
    ### point de montage avec utilisateur éxistant ###
    ##################################################
    if mountshare.mount("document_solea", "alexandre", "Solea05alexandre"):
        print(f"point de montage monter avec succès !")
    else:
        print(f"point de montage monter failed !")

    if mountshare.umount():
        print("démontage du point de montage '/tmp/share' avec succès ! ")
    else:
        print("démontage du point de montage '/tmp/share' failed !")
    
    ####################################################
    ### point de montage avec utilisateur inéxistant ###
    ####################################################
    if mountshare.mount("document_solea", "azerty", "azerty"):
        print(f"point de montage monter avec succès !")
    else:
        print(f"point de montage monter failed !")

    if mountshare.umount():
        print("démontage du point de montage '/tmp/share' avec succès ! ")
    else:
        print("démontage du point de montage '/tmp/share' failed !")
