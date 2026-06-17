#!/bin/usr/python

from tkinter import *
import yaml
from PIL import Image, ImageTk
from colorama import Fore, Style, init
init(autoreset=True)

from Functions import proxmox
from Functions import monitor
from Functions import custom
from Functions import docker1

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)
mainWindow = Tk()


# Set images
size = 25
ogX = Image.open('Resources/X.png')
resizedX = ogX.resize((size, size))
photoX = ImageTk.PhotoImage(resizedX)

ogCheck = Image.open('Resources/Check.png')
resizedCheck = ogCheck.resize((size, size))
photoCheck = ImageTk.PhotoImage(resizedCheck)


header = f"{Fore.BLUE}[Main]{Style.RESET_ALL} "


closeButton = Button(mainWindow, text="X", font=('Monospace', 10, 'bold'), command=exit)
closeButton.place(x=5, y=5)

title = Label(mainWindow, text=data['title'], font=('Monospace', 20))
title.pack(padx=50, pady=10)

for index in data['widgets']['monitor']:
    # Needed no matter what the service is
    service = data['widgets']['monitor'][index]['service']
    url = data['widgets']['monitor'][index]['url']


    # Healthcheck
    monitorFrame = Frame(mainWindow)
    if monitor.isup(url):
        print(f"{header}Service is up")
        label = Label(monitorFrame, text=index, image=photoCheck, compound=LEFT, font=('Monospace', 15), padx=10)
        label.pack(padx=10, pady=10, side=LEFT)

    else:
        print(f"{header}Service is down")
        label = Label(monitorFrame, text=index, image=photoX, compound=LEFT, font=('Monospace', 15), padx=10)
        label.pack(padx=10, pady=10, side=LEFT)

    if service == "proxmox":
        infobutton = Button(monitorFrame, text="i", font=('Monospace', 15), command = lambda p = mainWindow, i = index: proxmox.info(p, i))
        infobutton.pack(side=LEFT)
    elif service == "docker":
        infobutton = Button(monitorFrame, text="i", font=('Monospace', 15), command=lambda i=index, p=mainWindow: docker1.info(p, i))
        infobutton.pack(side=LEFT)

    monitorFrame.pack()

# Button grid

buttonFrame = Frame(mainWindow)
buttonFrame.columnconfigure(0, weight=1)
buttonFrame.columnconfigure(1, weight=1)
buttonFrame.columnconfigure(2, weight=1)

pveButton = Button(buttonFrame, text="Proxmox", command=lambda: proxmox.overview(mainWindow))
pveButton.grid(row=0, column=0)

dockerButton = Button(buttonFrame, text="Docker")
dockerButton.grid(row=0, column=1)

settingsButton = Button(buttonFrame, text="Settings")
settingsButton.grid(row=0, column=2)

buttonFrame.pack(pady=25, fill=X)

mainWindow.mainloop()