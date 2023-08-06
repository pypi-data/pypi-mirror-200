import requests
import time
import socket

def is_port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def find_open_port() -> int:
    with socket.socket() as s:
        s.bind(('', 0))            
        return s.getsockname()[1] 

HEALTHCHECK_TIMEOUT = 10
HEALTHCHECK_INTERVAL = 2

def wait_for_healthcheck(address): 
    start = time.time()
    while start + HEALTHCHECK_TIMEOUT > time.time(): 
        try:
            res = requests.get(address + "/healthcheck")
            if res.status_code == 418:
                return 
        except: 
            time.sleep(HEALTHCHECK_INTERVAL)
    raise TimeoutError()
