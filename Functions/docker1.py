import docker
import yaml
from colorama import Fore, Style, init
from tkinter import *
import webbrowser
from datetime import datetime, timezone
init(autoreset=True)

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

header = f"{Fore.MAGENTA}[Docker]{Style.RESET_ALL} "

# Connection
user = data['docker']['user']
host = data['docker']['host']

client = docker.DockerClient(base_url=f"ssh://{user}@{host}", use_ssh_client=True)

def restart(name):
    container = client.containers.get(name)
    container.restart()
    print(f"{header}Restarted: {name}")
def stop(name):
    container = client.containers.get(name)
    container.stop()
    print(f"{header}Stopped: {name}")
def start(name):
    container = client.containers.get(name)
    container.start()
    print(f"{header}Started: {name}")


def info(parent, name):
    container = client.containers.get(data['widgets']['monitor'][name]['name'])
    attrs = container.attrs

    # Ports
    ports = {}
    for container_port, bindings in (attrs["NetworkSettings"]["Ports"] or {}).items():
        if bindings:
            ports[container_port] = [f"{b['HostIp']}:{b['HostPort']}" for b in bindings]
        else:
            ports[container_port] = None  # exposed but not published
    
    port_numbers = [int(port.split('/')[0]) for port in ports]

    # Uptime
    started_at_str = attrs["State"].get("StartedAt", "")
    uptime = None
    if started_at_str and attrs["State"]["Running"]:
        started_at = datetime.fromisoformat(started_at_str.replace("Z", "+00:00"))
        uptime = str(datetime.now(timezone.utc) - started_at).split(".")[0]  # trim microseconds
    
    raw = container.stats(stream=False)

    # CPU %
    cpu_delta   = raw["cpu_stats"]["cpu_usage"]["total_usage"] \
                - raw["precpu_stats"]["cpu_usage"]["total_usage"]
    system_delta = raw["cpu_stats"]["system_cpu_usage"] \
                 - raw["precpu_stats"]["system_cpu_usage"]
    num_cpus    = raw["cpu_stats"].get("online_cpus") \
                or len(raw["cpu_stats"]["cpu_usage"].get("percpu_usage", [1]))
    cpu_pct = (cpu_delta / system_delta) * num_cpus * 100.0 if system_delta > 0 else 0.0

    # Memory
    mem       = raw["memory_stats"]
    mem_used  = mem["usage"] - mem.get("stats", {}).get("cache", 0)
    mem_limit = mem["limit"]
    mem_pct   = (mem_used / mem_limit) * 100.0 if mem_limit > 0 else 0.0

    monitorWin = Toplevel(parent)
    title = Label(monitorWin, text=name, font=('Monospace', 20))
    title.pack(padx=10, pady=5)

    grid = Frame(monitorWin)
    grid.columnconfigure(0, weight=1)
    grid.columnconfigure(1, weight=1)

    # Buttons
    buttons = Frame(grid)

    label = Label(buttons, text="Controls", font=('Monospace', 15))
    label.pack(pady=5)

    restartButton = Button(buttons, text="Restart", font=('Monospace', 12), command=lambda n = data['widgets']['monitor'][name]['name']: restart(n), width=15)
    restartButton.pack(pady=5)

    startButton = Button(buttons, text="Start", font=('Monospace', 12), command = lambda n = data['widgets']['monitor'][name]['name']: start(n), width=15)
    startButton.pack(pady=5)

    stopButton = Button(buttons, text="Stop", font=('Monospace', 12), command = lambda n = data['widgets']['monitor'][name]['name']: stop(n), width=15)
    stopButton.pack(pady=5)

    consoleButton = Button(buttons, text="Open Console", font=('Monospace', 12), command = lambda: webbrowser.open_new(data['widgets']['monitor'][name]['url']), width=15)
    consoleButton.pack(pady=5)

    buttons.grid(column=0, row=0)




    # Info
    info = Frame(grid)
    label = Label(info, text=f"Info\n({data['widgets']['monitor'][name]['name']})", font=('Monospace', 15))
    label.pack()

    # image
    #print(f"{header}Image: {attrs['Config']['Image']}")
    Label(info, text=f"Image: {attrs['Config']['Image']}").pack()
    # Status
    #print(f"{header}Status: {attrs['State']['Status']}")
    Label(info, text=f"Status: {attrs['State']['Status']}").pack()
    # Ports
    #print(f"{header}Ports: {port_numbers}")
    Label(info, text="Ports:").pack()
    for i in port_numbers:
        Label(info, text=i).pack()
    # Uptime
    #print(f"{header}Uptime: {uptime}")
    Label(info, text=f"Uptime: {uptime}").pack()
    # CPU
    #print(f"{header}CPU: {cpu_pct}")
    Label(info, text=f"CPU: {round(cpu_pct, 2)}%").pack()
    # Memory
    #print(f"{header}RAM: {mem_pct}")
    Label(info, text=f"Memory: {round(mem_pct, 2)}%").pack()



    info.grid(column=1, row=0)

    grid.pack(fill=X)