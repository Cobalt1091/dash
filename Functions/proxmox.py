from proxmoxer import ProxmoxAPI
from tkinter import *
import yaml
import time
from colorama import Fore, Style, init
from PIL import Image, ImageTk
import webbrowser
init(autoreset=True)

# https://pve.proxmox.com/pve-docs/api-viewer


header = f"{Fore.GREEN}[Proxmox]{Style.RESET_ALL} "

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

proxmox = ProxmoxAPI(
    data['proxmox']['host'], #PVE HOST (IP)
    user=data['proxmox']['user'], # PVE Username
    password=data['proxmox']['pass'], # PVE Password
    verify_ssl=False
)


node = data['proxmox']['node']

def restart(name):
    resourceType = data['widgets']['monitor'][name]['type']
    resourceId = data['widgets']['monitor'][name]['id']

    if resourceType.lower() == "vm":
        print(f'{header}Restarting VM {str(resourceId)}')
        proxmox.nodes(node).qemu(resourceId).status.stop.post()
        print(f'{header}Waiting for shutdown...')
        time.sleep(10)
        proxmox.nodes(node).qemu(resourceId).status.start.post()
        print(f'{header}Done')

    if resourceType.lower() == "lxc":
        print(f'{header}Restarting LXC {str(resourceId)}')
        proxmox.nodes(node).lxc(resourceId).status.stop.post()
        print(f'{header}Waiting for shutdown...')
        time.sleep(10)
        proxmox.nodes(node).lxc(resourceId).status.start.post()
        print(f'{header}Done')


def start(name):
    resourceType = data['widgets']['monitor'][name]['type']
    resourceId = data['widgets']['monitor'][name]['id']

    if resourceType.lower() == "vm":
        print(f'{header}Starting VM {str(resourceId)}')
        proxmox.nodes(node).qemu(resourceId).status.start.post()
        print(f'{header}Done')

    if resourceType.lower() == "lxc":
        print(f'{header}Starting LXC {str(resourceId)}')
        proxmox.nodes(node).lxc(resourceId).status.start.post()
        print(f'{header}Done')

def stop(name):
    resourceType = data['widgets']['monitor'][name]['type']
    resourceId = data['widgets']['monitor'][name]['id']

    if resourceType.lower() == "vm":
        print(f'{header}Stopping VM {str(resourceId)}')
        proxmox.nodes(node).qemu(resourceId).status.stop.post()
        print(f'{header}Done')

    if resourceType.lower() == "lxc":
        print(f'{header}Stopping LXC {str(resourceId)}')
        proxmox.nodes(node).lxc(resourceId).status.stop.post()
        print(f'{header}Done')


def overview(parent):
    window = Toplevel(parent)
    window.mainloop

    closeButton = Button(window, text='X', command=window.destroy)
    closeButton.place(x=5, y=5)
    title = Label(window, text="Proxmox", font=('Monospace', 20))
    title.pack(padx=10, pady=10)

    url = f"https://{data['proxmox']['host']}:8006/#v1:0:=node%2F{data['proxmox']['node']}:4:=jsconsole::::::"
    print(f"{header} URL: {url}")

    consoleButton = Button(window, text='Open Console', font=('Monospace', 15), command=lambda: webbrowser.open_new(url))
    consoleButton.pack()


    infoFrame = Frame(window)
    infoFrame.columnconfigure(0, weight=1)
    infoFrame.columnconfigure(1, weight=1)


    info = proxmox.nodes(node).disks.list.get()
    disks = Frame(infoFrame)
    diskLabel = Label(disks, text="Disks", font=('Monospace', 18))
    diskLabel.pack()
    for disk in info:

        label = Label(disks, text=disk['devpath'], font=('Monospace', 15))
        label.pack()

        size = Label(disks, text=f"Type: {disk['used']}\nSize: {round(disk['size']/1000000000)} GB")
        size.pack()

        if disk['health'] == "PASSED":
            statusLabel = Label(disks, text="Disk passed check")
            statusLabel.pack(pady=(0, 15))

    disks.grid(row=0, column=0, padx=15, pady=15, sticky=N)

    # Node Info

    nodeFrame = Frame(infoFrame)
    nodeLabel = Label(nodeFrame, text="Node", font=('Monospace', 18))
    nodeLabel.pack()
    name = Label(nodeFrame, text=f"Name: {node}")
    name.pack()

    nodeStatus = proxmox.nodes(node).status.get()
    memory = Label(nodeFrame, text=f"Memory:\n Used: {round((nodeStatus.get('memory')['used'])/1000000000, 2)} GB, Available: {round((nodeStatus.get('memory')['available'])/1000000000, 2)}")
    memory.pack()

    cpuLabel = Label(nodeFrame, text=f"CPU Usage: {nodeStatus.get('cpu'):.2%}")
    cpuLabel.pack()




    nodeFrame.grid(row=0, column=1, padx=15, pady=15, sticky=N)

    infoFrame.pack(fill=X)



def info(parent, name):
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

    restartButton = Button(buttons, text="Restart", font=('Monospace', 12), command=lambda n = name: restart(n), width=15)
    restartButton.pack(pady=5)

    startButton = Button(buttons, text="Start", font=('Monospace', 12), command = lambda n = name: start(n), width=15)
    startButton.pack(pady=5)

    stopButton = Button(buttons, text="Stop", font=('Monospace', 12), command = lambda n = name: stop(n), width=15)
    stopButton.pack(pady=5)
    if data['widgets']['monitor'][name]['type'] == "lxc":
        url = f"https://{data['proxmox']['host']}:8006/#v1:0:=lxc%2F{data['widgets']['monitor'][name]['id']}:4::::::=consolejs:"
    elif data['widgets']['monitor'][name]['type'] == "vm":
        url = f"https://{data['proxmox']['host']}:8006/#v1:0:=qemu%2F{data['widgets']['monitor'][name]['id']}:4::::::=consolejs:"
    else:
        print(f'{header} ERROR: Could not properly generate url for console')


    print(f"{header}URL for console: {url}")
    browserButton = Button(buttons, text="Open Console", font=('Monospace', 12), command = lambda: webbrowser.open(url), width=15)
    browserButton.pack(pady=5)

    buttons.grid(column=0, row=0)


    # Def needed info
    resourceId = data['widgets']['monitor'][name]['id']
    resourceType = data['widgets']['monitor'][name]['type']
    
    if resourceType == "lxc":
        status = proxmox.nodes(node).lxc(resourceId).status.current.get()
    elif resourceType == "vm":
        status = proxmox.nodes(node).qemu(resourceId).status.current.get()


    # Info
    info = Frame(grid)
    label = Label(info, text=f"Info\n({status.get('name')})", font=('Monospace', 15))
    label.pack()

    # Uptime
    #print(f"{header}{round((status.get('uptime'))/360, 2)} Hrs")
    Label(info, text=f"Uptime: {round((status.get('uptime'))/3600, 2)} Hrs").pack()
    # Memory
    #print(f"{header}{(status.get('mem'))/1000000} MB")
    Label(info, text=f"Memory: {round((status.get('mem'))/1000000, 2)} MB").pack()
    # CPU
    #print(f"{header}{status.get('cpu')}")
    Label(info, text=f"CPU: {status.get('cpu'):.1%}").pack()
    # Storage
    #print(f"{header}{status.get('disk')}")
    Label(info, text=f"Disk: {round((status.get('disk'))/1000000000, 2)} GB").pack()

    info.grid(column=1, row=0)

    grid.pack(fill=X)