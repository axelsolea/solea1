import re
import subprocess

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
            success_rate = int(filter.group(1))
        else:
            # If the packet loss percentage cannot be found, set success rate to -1 to indicate failure
            success_rate = -1

        return success_rate, result.returncode

if __name__ == "__main__":
    ping1 = Ping("1.1.1.1")
    success_rate, return_code = ping1.send_ping()
    print("ping vers 1.1.1.1:")
    print("status:", success_rate)
    print("code de retour:", return_code)

    ping2 = Ping("172.0.18.253")
    success_rate, return_code = ping2.send_ping()
    print("ping vers 172.0.18.253:")
    print("status:", success_rate)
    print("code de retour:", return_code)

