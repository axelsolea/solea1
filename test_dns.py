from logger import Logger
import subprocess
import os
import sys
import re

def init_log_file(file: str) -> Logger:
    log: Logger = Logger("test_dns.log", absolut_path=False)
    log.emptyFile()

    return log

def test_name(name: str, server: str, log: Logger) -> None:
    pattern_a_record: str = r'Address: (\d+\.\d+\.\d+\.\d+)'
    pattern_ptr_record: str = r'(?<=name = )\S+'

    result = subprocess.run(["nslookup", name, server], capture_output=True, text=True)
    output: str = result.stdout
    ip_addr_str: str = ", ".join(re.findall(pattern_a_record, output))
    log.writeFile("NOTICE", f"A [{ip_addr_str}]")

    #check A record that is not empty
    if not re.search(pattern_a_record, output):
        log.writeFile("ERROR", f"no record found for {name}")
        return False

    for ip in re.findall(pattern_a_record, output):
        result = subprocess.run(["nslookup", "-q=PTR", ip, server], capture_output=True, text=True)
        output: str = result.stdout
        list_name: list = re.findall(pattern_ptr_record, output)
        ptr_name_str: str = ", ".join(re.findall(pattern_ptr_record, output))
        log.writeFile("NOTICE", f"Resolving inverse query {ip}")
        log.writeFile("NOTICE", f"PTR[{ptr_name_str[0:len(ptr_name_str) - 1]}]")

        for ptr_name in list_name:
            if ptr_name != name + ".":
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
    current_dir: str = os.getcwd()

    with open(f"{current_dir}/list_name.txt", "r") as file:
        data: str = file.read().split("\n")
    
    #add all name to logfile
    for name in data:
        if name and "#" not in name: # '#' est un début commentaire
            log.writeFile("INFO", f"adding to testing list {name}")
            nb_name += 1
    
    #send query
    for name in data:
        if name and not name.startswith("#"):
            log.writeFile("INFO", f"Resolving {name}")
            if test_name(name, dns_server, log):
                log.writeFile("INFO", f"{name} => OK\n\n")
                nb_success_request += 1
            else:
                log.writeFile("INFO", f"{name} => NOK\n\n")

    #check the number of name is the same as the number of succes request 
    if nb_name == nb_success_request:
        print("0")
    else:
        print("1")
