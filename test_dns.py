from logger import Logger
import subprocess
import os
import sys
import re

def init_log_file(file: str) -> Logger:
    """
    Initialize a new Logger object for logging DNS test results.

    Args:
        file (str): The file name to use for the log.

    Returns:
        Logger: A Logger object for logging.
    """
    log: Logger = Logger(file, absolut_path=False)
    log.emptyFile()
    return log

def get_a_record_name(name: str, server: str) -> list:
    """
    Get the A record name from a DNS server.

    Args:
        name (str): The name to query.
        server (str): The DNS server to query.

    Returns:
        list: List of IP addresses.
    """
    pattern_a_record: str = r'Address: (\d+\.\d+\.\d+\.\d+)'
    result = subprocess.run(["nslookup", name, server], capture_output=True, text=True)
    output: str = result.stdout
    return re.findall(pattern_a_record, output)

def get_ptr_record_name(ip: str, server: str) -> list:
    """
    Get the PTR record name from an IP address.

    Args:
        ip (str): The IP address to query.
        server (str): The DNS server to query.

    Returns:
        list: List of PTR records.
    """
    pattern_ptr_record: str = r'(?<=name = )\S+'
    result = subprocess.run(["nslookup", "-q=PTR", ip, server], capture_output=True, text=True)
    output: str = result.stdout
    return re.findall(pattern_ptr_record, output)

def compare_a_ptr_record(name: str, ptr_list_name: list) -> bool:
    """
    Compare a name to a list of PTR records.

    Args:
        name (str): The name to compare.
        ptr_list_name (list): List of PTR records.

    Returns:
        bool: True if all PTR records match the name, False otherwise.
    """
    for ptr_name in ptr_list_name:
        if ptr_name != name + ".":
            return False
    return True

def test_name(name: str, server: str, log: Logger) -> bool:
    """
    Test a DNS name by checking its A and PTR records.

    Args:
        name (str): The DNS name to test.
        server (str): The DNS server to query.
        log (Logger): Logger object for logging results.

    Returns:
        bool: True if the test passes, False otherwise.
    """
    ip_addr: list = get_a_record_name(name, server)
    ip_addr_str: str = ", ".join(ip_addr)

    if not ip_addr_str: 
        log.writeFile("ERROR", f"no record found for {name}")
        return False
    else:
        log.writeFile("NOTICE", f"A [{ip_addr_str}]")

    for ip in ip_addr:
        list_name: list = get_ptr_record_name(ip, server)
        ptr_name_str: str = ", ".join(list_name)
        log.writeFile("NOTICE", f"Resolving inverse query {ip}")
        log.writeFile("NOTICE", f"PTR[{ptr_name_str[0:len(ptr_name_str) - 1]}]")
        
        if not compare_a_ptr_record(name, list_name):
            return False

    return True
        
if __name__ == "__main__":
    current_dir: str = os.getcwd()
    nb_name: int = 0
    nb_success_request: int = 0

    with open(f"{current_dir}/list_name.txt", "r") as file:
        data: str = file.read().split("\n")

    log: Logger = init_log_file("dns_test.log")
    dns_server: str = sys.argv[1]

    for name in data:
        if name and "#" not in name:
            log.writeFile("INFO", f"adding to testing list {name}")
            nb_name += 1
    
    for name in data:
        if name and not name.startswith("#"):
            log.writeFile("INFO", f"Resolving {name}")
            if test_name(name, dns_server, log):
                log.writeFile("INFO", f"{name} => OK\n\n")
                nb_success_request += 1
            else:
                log.writeFile("INFO", f"{name} => NOK\n\n")

    if nb_name == nb_success_request:
        sys.exit(0)
    else:
        sys.exit(1)
