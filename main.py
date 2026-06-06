from tkinter import *
import yaml
from PIL import Image, ImageTk
from colorama import Fore, Style, init
init(autoreset=True)

from Functions import monitor
from Functions import proxmox
from Functions import docker1
from Functions import custom


with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)
window = Tk()

header = f"{Fore.BLUE}[Main]{Style.RESET_ALL} "

# Set images
size = 25
ogX = Image.open('Resources/X.png')
resizedX = ogX.resize((size, size))
photoX = ImageTk.PhotoImage(resizedX)

ogCheck = Image.open('Resources/Check.png')
resizedCheck = ogCheck.resize((size, size))
photoCheck = ImageTk.PhotoImage(resizedCheck)

closeButton = Button(window, text="X", font=('Monospace', 10, 'bold'), command=exit)
closeButton.place(x=5, y=5)

if "title" in data:
    label = Label(window, text=data['title'], font=('Monospace', 20))
    label.pack()

for index in data['widgets']['monitor']:
    # Needed no matter what the service is
    service = data['widgets']['monitor'][index]['service']
    url = data['widgets']['monitor'][index]['url']


    # Healthcheck
    if monitor.isup(url):
        print(f"{header}Service is up")
        label = Label(window, text=index, image=photoCheck, compound=LEFT, font=('Monospace', 15), padx=10)
        label.pack(padx=10, pady=10, anchor=W)

    else:
        print(f"{header}Service is down")
        label = Label(window, text=index, image=photoX, compound=LEFT, font=('Monospace', 15), padx=10)
        label.pack(padx=10, pady=10, anchor=W)
        
        if service == "proxmox":
            # Specific to proxmox
            resourceType = data['widgets']['monitor'][index]['type']
            resourceId = data['widgets']['monitor'][index]['id']

            button = Button(window, text=f"Restart ({resourceType.upper()} {resourceId})", command=lambda rt=resourceType, i=resourceId: proxmox.restart(rt, i))
            button.pack(padx=10, pady=(0, 10), anchor=W)
        elif service == "docker":
            # Specific to docker
            name = data['widgets']['monitor'][index]['name']
            button = Button(window, text=f"Restart (Container {name})", command = lambda n=name: docker1.restart(n))
            button.pack(padx=10, pady=(0, 10), anchor=W)
        elif service == "custom":
            customName = data['widgets']['monitor'][index]['name']
            button = Button(window, text=f"Run custom command ({customName})", command=lambda n=customName: custom.run(n))
            button.pack(padx=10, pady=(0, 10), anchor=W)


# Button grid

buttonFrame = Frame(window)
buttonFrame.columnconfigure(0, weight=1)
buttonFrame.columnconfigure(1, weight=1)
buttonFrame.columnconfigure(2, weight=1)

pveButton = Button(buttonFrame, text="Proxmox", command=proxmox.overview)
pveButton.grid(row=0, column=0)

dockerButton = Button(buttonFrame, text="Docker")
dockerButton.grid(row=0, column=1)

settingsButton = Button(buttonFrame, text="Settings")
settingsButton.grid(row=0, column=2)

buttonFrame.pack(pady=25, fill=X)





#if monitor.isup(url):
#    print("Service is up")
#    label = Label(window, text="Service is up", image=photoCheck, compound=LEFT, padx=25)
#    label.pack()
#else:
#    print("Service is down")
#    label = Label(window, text="Service is down", image=photoX, compound=LEFT, padx=25)
#    label.pack()
#
#button = Button(window, text="Restart LXC 102", command=lambda: proxmox.restart('lxc', 103))
#button.pack()

window.mainloop()