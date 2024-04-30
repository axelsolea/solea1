import subprocess
import re


class Ping:
    """
    A class for sending ping requests to a specified IP address and retrieving success rate.

    Attributes:
        _ip (str): The IP address to ping.
    """

    def __init__(self, ip: str) -> None:
        """
        Initializes a Ping object with the specified IP address.

        Args:
            ip (str): The IP address to ping.
        """
        self._ip: str = ip

    def send_ping(self, count=1) -> tuple[int,int]:
        """
        Sends ping requests to the specified IP address and returns the success rate and return code.

        Args:
            count (int): Number of ping requests to send (default is 1).

        Returns:
            tuple[int,int]: A tuple containing the success rate (in percentage) and the return code.
        """
        result = subprocess.run(['ping', self._ip, '-c', str(count)], capture_output=True, text=True)
        
        # Extracting the success percentage and returning data
        filter = re.search(r"(\d+)% packet loss", result.stdout)
        if filter:
            return int(filter.group(1)), result.returncode
        else:
            return 100, result.returncode


if __name__ == "__main__":
    ping: Ping = Ping("1.1.1.1")
    ping.send_ping()

