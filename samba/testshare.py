from colorama import Fore, Style
from ping import Ping
from mountshare import MountShare


class TestShare:

    def __init__(self, server: str, user: str, passwd: str, mount_point: str) -> None:
        self._server: str = server
        self._user: str = user
        self._passwd: str = passwd
        self._mount_point: str = mount_point
        self._ping: Ping = Ping(server)
        self._mountshare: MountShare = MountShare(server, mount_point)

    def __repr__(self) -> str:
        return f"{Fore.RED}Information du test:{Style.RESET_ALL}\n{'-' * 25 }\n{Fore.RED}server{Style.RESET_ALL}: {self._server}\n{Fore.RED}utilisateur{Style.RESET_ALL}: {self._user}\n{Fore.RED}mot de passe{Style.RESET_ALL}: {self._passwd}\n{Fore.RED}point de montage: {Style.RESET_ALL}: {self._mount_point}\n{'-' * 25}"
    
    def is_accessible(self) -> bool:
        failed_rate, rcode = self._ping.send_ping()
        return failed_rate == 0 and rcode == 0
    
    def create_dir(self, name: str) -> bool:
        pass

    def create_file(self, name: str) -> bool:
        pass
    
    def mount(self, share_name: str) -> bool:
        output, rcode = self._mountshare.mount(share_name, self._user, self._passwd)
        return rcode == 0

    def umount(self) -> bool:
        output, rcode = self._mountshare.umount()
        return rcode == 0

    def export(self) -> dict:
        pass


if __name__ == "__main__":
    testshare: TestShare = TestShare("1.1.1.1", "alexandre", "Solea05alexandre", "/tmp")
    print(testshare)
    testshare.is_accessible()

