import docker
import yaml
from colorama import Fore, Style, init
from tkinter import *
init(autoreset=True)

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

header = f"{Fore.MAGENTA}[Docker]{Style.RESET_ALL} "

def restart(name):
    username = data['docker']['user']
    host = data['docker']['host']

    # Set up docker connection
    client = docker.DockerClient(base_url=f"ssh://{username}@{host}")
    containers = client.containers.list(all=True)

    container = client.containers.get(name)
    print(f"{header}Restarting {name}...")
    container.restart()
    print(f"{header}Done")

def info(parent, name):
    contName = data['widgets']['monitor'][name]['name']
    dockerWin = Toplevel(parent)

    title = Label(dockerWin, text=contName, font=('Monospace', 15))
    title.pack(padx=10, pady=5)

    restartButton = Button(dockerWin, text="Restart", command = lambda n=contName: restart(n))
    restartButton.pack(padx=10, pady=5)