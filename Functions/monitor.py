import requests
from colorama import Fore, Style, init
init(autoreset=True)



header = f"{Fore.YELLOW}[Monitor]{Style.RESET_ALL} "

def isup(url):
    try:
        response = requests.get(url, timeout=5, verify=False, allow_redirects=True)
        print(f"{header}{url} -> {response.status_code} (after redirects: {response.url})")
        return response.status_code < 500
    except requests.RequestException as e:
        print(f"{header}{url} -> EXCEPTION: {e}")
        return False
    