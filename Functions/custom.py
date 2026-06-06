import yaml
import paramiko
from colorama import Fore, Style, init
init(autoreset=True)


with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

header = f"{Fore.RED}[custom]{Style.RESET_ALL} "

def run(name):
    host = data['custom'][name]['host']
    user = data['custom'][name]['user']
    passwd = data['custom'][name]['password']
    command = data['custom'][name]['command']
    print(f"{header}{host}")
    print(f"{header}{user}")
    print(f"{header}{passwd}")
    print(f"{header}{command}")
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect(host, username=user, password=str(passwd))
    stdin, stdout, stderr = ssh.exec_command(command)

    print(f'{header}Output: {stdout.read().decode()}')

    print(f'{header}Errors: {stderr.read().decode()}')

    ssh.close()

