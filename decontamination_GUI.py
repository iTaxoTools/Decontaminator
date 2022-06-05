##### Version 1.0 ######
#### David Leiße #######
##### david.leisse@uni-bielefeld.de #####

import decontamination as dc

import os
from tkinter import *
from tkinter import simpledialog, messagebox
from tkinter import filedialog

root = Tk()
root.directory = ""

def loadDirectory():
    """
    Defining input directory
    """
    initialdir = os.getcwd() 
    root.directory = filedialog.askdirectory(initialdir = initialdir, title="Select output folder")
    output.insert(END, "Inputdirectory: " + str(root.directory).split("/")[-1] + "\n")

def Run():
    """
    Running devontamination script
    """
    dc.__Main__(("--dir " + root.directory))
    output.insert(END, "Run complete. Check input directory.\n")

root.title("TaxoInflationAnalyzer")
output = Text(root, width = 90, height = 10, bd = 3, pady=1)
output.grid(row=0,column=0,columnspan=9)
Label(root).grid(row=1, columnspan= 9)
Button(root, text="Input folder",width=10, height=3, command=lambda: loadDirectory()).grid(column=0,row=1)
Button(root, text="Run", width=10, height=3, command=lambda: Run()).grid(column=1, row=1)
Button(root, text="Quit",width=10, height=3, command=root.destroy).grid(column=2, row=1)

mainloop()
