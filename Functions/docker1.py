import docker
import yaml
from colorama import Fore, Style, init
init(autoreset=True)

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

header = f"{Fore.MAGENTA}[Docker]{Style.RESET_ALL} "

def restart(name):
    username = data['docker']['user']
    host = data['docker']['host']

    print(f"{header}{username}")
    print(f"{header}{host}")
    print(f"{header}{username}@{host}")


    # Set up docker connection
    client = docker.DockerClient(base_url=f"ssh://{username}@{host}")
    containers = client.containers.list(all=True)

    container = client.containers.get(name)
    print(f"{header}Restarting {name}...")
    container.restart()
    print(f"{header}Done")