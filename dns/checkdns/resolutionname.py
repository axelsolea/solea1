import pandas as pd
from .dnsclient import Dnsclient
from .wrongipversion import WrongIpVersion

class ResolutionName:
    """
    Class to perform DNS resolution tests for name and PTR records.

    Attributes:
        _data (pd.DataFrame): DataFrame containing DNS resolution data.
        _ipv (int): IP version (4 or 6).
        _server (str): DNS server address.
        _dnsclient (Dnsclient): DNS client object.
        _success_request (list): List of successful DNS resolution requests.
        _failed_request (list): List of failed DNS resolution requests.
        _success_name_request (list): List of successful name record requests.
        _failed_name_request (list): List of failed name record requests.
        _success_ptr_request (list): List of successful PTR record requests.
        _failed_ptr_request (list): List of failed PTR record requests.
        _total_resolution (int): Total number of resolution attempts.
        _cpt (int): Counter for successful resolutions.
        _status (bool): Overall status of resolution process.
    """

    def __init__(self, data: pd.DataFrame, server: str, ipv: int) -> None:
        """
        Initializes ResolutionName object.

        Args:
            data (pd.DataFrame): DataFrame containing DNS resolution data.
            server (str): DNS server address.
            ipv (int): IP version (4 or 6).
        """
        # Vérification de la version d'IP
        self.check_ip_version(ipv)
        self._ipv: int = ipv

        # propriété
        self._data: pd.DataFrame = data
        self._server: str = server
        self._dnsclient: Dnsclient = Dnsclient(server)
        self._success_request: list = []
        self._failed_request: list = []
        self._success_name_request: list = []
        self._failed_name_request: list = []
        self._success_ptr_request: list = []
        self._failed_ptr_request: list = []
        self._total_resolution: int = 0
        self._cpt: int = 0
        self._status: bool = False

    def check_ip_version(self, ipv: int) -> WrongIpVersion|None:
        """
        Check if the IP version is valid (4 or 6).

        Args:
            ipv (int): IP version.

        Returns:
            WrongIpVersion: If IP version is invalid.
        """
        if ipv not in [4, 6]:
            return WrongIpVersion("Donner une IP de version valide: 4 ou 6")
    
    def test_name_record(self, name: str, ip: str) -> bool:
        """
        Test DNS resolution for name records (A or AAAA).

        Args:
            name (str): Hostname to resolve.
            ip (str): IP address associated with the hostname.

        Returns:
            bool: True if resolution successful, False otherwise.
        """
        if self._ipv == 4:
            cli_a_record: list = list(self._dnsclient.get_A_record(name).split("\n"))

            if len(cli_a_record) == 0:
                self._failed_name_request.append(f"{name} -> expected ip: {ip}, got: ''")
                return False

            if ip in cli_a_record:
                self._success_name_request.append(f"{name} -> expected ip: {ip}, got: {','.join(cli_a_record)}")
                return True
            else:
                self._failed_name_request.append(f"{name} -> expected ip: {ip}, got: {','.join(cli_a_record)}")
                return False

        elif self._ipv == 6:
            cli_aaaa_record: list = list(self._dnsclient.get_AAAA_record(name).split("\n"))

            if len(cli_aaaa_record) == 0:
                self._failed_name_request.append(f"{name} -> expected ip: {ip}, got: ''")
                return False

            if ip in cli_aaaa_record:
                self._success_name_request.append(f"{name} -> expected ip: {ip}, got: {','.join(cli_aaaa_record)}")
                return True
            else:
                self._failed_name_request.append(f"{name} -> expected ip: {ip}, got: {','.join(cli_aaaa_record)}")
                return False
        else:
            return False

    def test_ptr_record(self, ip: str, name: str) -> bool:
        """
        Test DNS resolution for PTR records.

        Args:
            ip (str): IP address to resolve.
            name (str): Expected hostname.

        Returns:
            bool: True if resolution successful, False otherwise.
        """
        cli_ptr_record: str = self._dnsclient.get_PTR_record(ip)
        
        if cli_ptr_record == "":
            self._failed_ptr_request.append(f"{ip} -> expected ptr name: {name}, got: ''")
            return False

        if f"{name}." == cli_ptr_record:
            self._success_ptr_request.append(f"{ip} -> expected ptr name: {name}, got: {cli_ptr_record}")
            return True
        else:
            self._failed_ptr_request.append(f"{ip} -> expected ptr name: {name}, got: {cli_ptr_record}")
            return False

    def test_name(self, name: str, ip: str, expect_ptr_name: str) -> bool:
        """
        Test DNS resolution for name and associated PTR record.

        Args:
            name (str): Hostname to resolve.
            ip (str): IP address associated with the hostname.
            expect_ptr_name (str): Expected PTR record name.

        Returns:
            bool: True if both name and PTR resolutions successful, False otherwise.
        """
        cpt: int = 0

        if self.test_name_record(name, ip):
            cpt += 1

        if self.test_ptr_record(ip, expect_ptr_name):
            cpt += 1
        
        self._cpt += 1
        return cpt == 2

    def run(self) -> None:
        """
        Execute DNS resolution tests for each entry in the DataFrame.
        """
        if self._ipv == 4:
            index_IP: int = 1
        elif self._ipv == 6:
            index_IP: int = 2

        for index, row in self._data.iterrows():
            self._total_resolution += 1
            
            if self.test_name(row.iloc[0],row.iloc[index_IP] , row.iloc[3]):
                self._success_request.append((row.iloc[0], row.iloc[index_IP], row.iloc[3], "OK"))
            else:
                self._failed_request.append((row.iloc[0], row.iloc[index_IP], row.iloc[3], "NOK"))

    def export_result(self) -> dict:
        """
        Export the results of DNS resolution tests.

        Returns:
            dict: Dictionary containing test results.
        """
        self._status = self._total_resolution == self._cpt

        return {
            "version": self._ipv,
            "status": self._status,
            "success_rate": (self._cpt / self._total_resolution) * 100,
            "full_success": self._success_request,
            "full_failed_name": self._failed_request,
            "success_name_record": self._success_name_request,
            "failed_name_record": self._failed_name_request,
            "success_ptr_record": self._success_ptr_request,
            "failed_ptr_record": self._failed_ptr_request
        }
