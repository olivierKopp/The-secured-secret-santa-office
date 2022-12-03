from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk

from ipaddress import ip_address

# Contant

windowTitle = "An Actually Secure Secret Santa"

textButtonValidate = "Validate"
textLabelIpAddr = "IP Address"
textLabelBlackList = "Black List"
textLabelVictim = "You will give a present to Adel!"

padyButtonValidate = '40 0'
padyLabelVictim = '40 0'

# Global



# Classes

class SecretSanta:
    def __init__(self, root):
        # Instance attributes
        self.ipAddr    = StringVar()
        self.blackList = StringVar()
        
        root.title(windowTitle)

        mainframe = ttk.Frame(root, padding="5 5 10 10")
        mainframe.grid(column=0, row=0, sticky="nesw")
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        labelIpAddr    = ttk.Label(mainframe, text=textLabelIpAddr)
        labelBlackList = ttk.Label(mainframe, text=textLabelBlackList)
        labelVictim    = ttk.Label(mainframe, text=textLabelVictim)

        entryIpAddr    = ttk.Entry(mainframe, textvariable=self.ipAddr)
        entryBlackList = ttk.Entry(mainframe, textvariable=self.blackList)

        buttonValidate = ttk.Button(mainframe, text=textButtonValidate, command=self.funcButtonValidate)

        labelIpAddr.grid(column=1, row=1)
        labelBlackList.grid(column=1, row=2)
        labelVictim.grid(column=1, columnspan=2, row=4, pady=padyLabelVictim)
        entryIpAddr.grid(column=2, row=1)
        entryBlackList.grid(column=2, row=2)
        buttonValidate.grid(column=2, row=5, pady=padyButtonValidate, sticky=E)



    def parseIpAddrList(self, rawIpAddr: str) -> list[str]:
        print("Called: parseIpAddrList()")

        ipAddrs = []

        noSpaces = "".join(rawIpAddr.split())
        for rawIp in noSpaces.split(','):
            try:
                ipAddrs.append(ip_address(rawIp))
            except ValueError:
                print("Error: Failed to parse IP, check your input!")
                return []

        return ipAddrs


    def funcButtonValidate(self, *args):
        print("Called: funcButtonValidate()")
        print(self.parseIpAddrList(self.ipAddr.get()))
        print(self.blackList.get())


        

# TODO: The following code is only here as a demo
#       It must be removed at some point.

# Main code
root = ThemedTk(theme="arc")
SecretSanta(root)
root.mainloop()
