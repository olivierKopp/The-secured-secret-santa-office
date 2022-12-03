from tkinter import *
from tkinter import ttk


# Contant

windowTitle = "An Actually Secure Secret Santa"

textLabelIpAddr = "IP Address"
textLabelBlackList = "Black List"
textButtonValidate = "Validate"

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

        entryIpAddr    = ttk.Entry(mainframe, textvariable=self.ipAddr)
        entryBlackList = ttk.Entry(mainframe, textvariable=self.blackList)

        buttonValidate = ttk.Button(mainframe, text=textButtonValidate, command=funcButtonValidate)

        labelIpAddr.grid(column=1, row=1)
        labelBlackList.grid(column=1, row=2)
        entryIpAddr.grid(column=2, row=1)
        entryBlackList.grid(column=2, row=2)
        buttonValidate.grid(column=2, row=5, sticky=E)


# Functions

def funcButtonValidate():
    print("funcButtonValidate()")
                            

# TODO: The following code is only here as a demo
#       It must be removed at some point.

# Main code
root = Tk()
SecretSanta(root)
root.mainloop()
