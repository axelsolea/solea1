import subprocess

class Dnsclient:
    """
    A simple DNS client class for retrieving DNS records.
    
    Attributes:
        _server (str): The DNS server to query.
        _all_names (set): A set containing all names and IPs tested.
    """

    def __init__(self, server: str):
        """
        Initialize the DNS client with the specified DNS server.

        Args:
            server (str): The DNS server to use for queries.
        """
        self._server: str = server
        self._all_names: set = set()
    
    def get_A_record(self, name: str) -> str|None:
        """
        Retrieve the A record for the specified domain name.

        Args:
            name (str): The domain name to query for.

        Returns:
            str: The A record IP address, or None if an error occurs.
        """
        if not name:
            return None

        self._all_names.add(name)
        try:
            result = subprocess.run(["dig", "-t", "A", name, f"@{self._server}", "+short"], capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            return f"=> exception prise lors de la résolution de {name}(A)"
    
    def get_AAAA_record(self, name: str) -> str|None:
        """
        Retrieve the AAAA record for the specified domain name.

        Args:
            name (str): The domain name to query for.

        Returns:
            str: The AAAA record IP address, or None if an error occurs.
        """
        if not name:
            return None

        self._all_names.add(name)
        try:
            result = subprocess.run(["dig", "-t", "AAAA", name, f"@{self._server}", "+short"], capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            return f"=> exception prise lors de la résolution de {name}(AAAA)"
    

    def get_SRV_record(self, name: str) -> str|None:
        """
        Retrieve the SRV record for the specified domain name.

        Args:
            name (str): The domain name to query for.

        Returns:
            str: The SRV record, or None if an error occurs.
        """
        if not name:
            return None

        self._all_names.add(name)
        try:
            result = subprocess.run(["dig", "-t", "SRV", name, f"@{self._server}", "+short"], capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            return f"=> exception prise lors de la résolution de {name}(SRV)"
    
    def get_MX_record(self, name: str) -> str|None:
        """
        Retrieve the MX record for the specified domain name.

        Args:
            name (str): The domain name to query for.

        Returns:
            str: The MX record, or None if an error occurs.
        """
        if not name:
            return None

        self._all_names.add(name)
        try:
            result = subprocess.run(["dig", "-t", "MX", name, f"@{self._server}", "+short"], capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            return f"=> exception occurred while resolving {name}(MX)"

    def get_PTR_record(self, ip: str) -> str|None:
        """
        Retrieve the PTR record for the specified IP address.

        Args:
            ip (str): The IP address to query for.

        Returns:
            str: The PTR record domain name, or None if an error occurs.
        """
        if not ip:
            return None

        self._all_names.add(ip)
        try:
            result = subprocess.run(["dig", "-x", ip, f"@{self._server}", "+short"], capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            return f"=> exception prise lors de la résolution de {ip}(PTR)"

    def all_tested_names(self) -> set:
        """
        Get a set of all names and IPs tested by this DNS client.

        Returns:
            set: A set containing all tested names and IPs.
        """
        return self._all_names

    def show_names(self) -> None:
        """
        Print all names tested.

        This method prints all the names stored in the '_all_names' attribute of the object.

        Returns:
            None
        """
        print("All names tested:")
        for name in self._all_names:
            print(f"- {name}")

    @property
    def server(self):
        """The server property."""
        return self._server
    @server.setter
    def server(self, value: str):
        self._server = value

