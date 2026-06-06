from proxmoxer import ProxmoxAPI
from tkinter import *
import yaml
import time
from colorama import Fore, Style, init
from PIL import Image, ImageTk
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

def restart(resourceType, resourceId):


    if resourceType.lower() == "vm":
        vm_status = proxmox.nodes(node).qemu(resourceId).status.current.get()
        if vm_status.get('status') == 'running':
            print(f'{header}Restarting VM {str(resourceId)}')
            proxmox.nodes(node).qemu(resourceId).status.stop.post()
            print(f'{header}Waiting for shutdown...')
            time.sleep(10)
            proxmox.nodes(node).qemu(resourceId).status.start.post()
            print(f'{header}Done')
        elif vm_status.get('status') == 'stopped':
            print(f'{header}Starting vm {resourceId}...')
            proxmox.nodes(node).qemu(resourceId).status.start.post()
            print(f'{header}Done')


    if resourceType.lower() == "lxc":
        lxcStatus = proxmox.nodes(node).lxc(resourceId).status.current.get()
        if lxcStatus.get('status') == 'running':
            print(f'{header}Restarting LXC {str(resourceId)}')
            proxmox.nodes(node).lxc(resourceId).status.stop.post()
            print(f'{header}Waiting for shutdown...')
            time.sleep(10)
            proxmox.nodes(node).lxc(resourceId).status.start.post()
            print(f'{header}Done')
        elif lxcStatus.get('status') == 'stopped':
            print(f'{header}Starting LXC {str(resourceId)}...')
            proxmox.nodes(node).lxc(resourceId).status.start.post()
            print(f'{header}Done')

def overview():
    window = Tk()
    window.mainloop

    closeButton = Button(window, text='X', command=window.destroy)
    closeButton.place(x=5, y=5)
    title = Label(window, text="Proxmox", font=('Monospace', 20))
    title.pack(padx=10, pady=10)


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

