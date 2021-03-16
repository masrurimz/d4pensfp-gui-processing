from tkinter import *
import tkinter as tk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
class GUI(Frame):
    def __init__(self, plotter):
        Frame.__init__(self)
        self.plotter = plotter
        self.master = tk.Tk()
        self.figure = plotter.fig
        self.startUp()

    def startUp(self):
        self.master.geometry('1300x700')
        self.master.title("EMG Real Time Plot")
        self.initComponent()
        self.configureLayout()
        self.master.mainloop()

    def initComponent(self):
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.master)
        self.lbConnection = tk.Label(self.master, text="Connection Status")
        self.btConnection = tk.Button(self.master, text="Connect")
        self.lbFileName = tk.Label(self.master, text="File Name")
        self.etFileName = tk.Entry(self.master, text="")
        self.btSave = tk.Button(self.master, text="Save")
        self.btQuit = tk.Button(master=self.master, text="Quit", command=self.master.quit)

    def configureLayout(self):
        self.canvas.get_tk_widget().grid(row=0, column=0, rowspan=6)
        self.lbConnection.grid(row=0, column=1, sticky=tk.NSEW, padx=5, pady=5)
        self.btConnection.grid(row=1, column=1, sticky=tk.NSEW, padx=5, pady=2)
        self.lbFileName.grid(row=2, column=1, sticky=tk.NSEW, padx=2, pady=2)
        self.etFileName.grid(row=3, column=1, sticky=tk.NSEW, padx=2, pady=2)
        self.btSave.grid(row=4, column=1, sticky=tk.NSEW, padx=2, pady=2)
        self.btQuit.grid(row=5, column=1, sticky=tk.NSEW, padx=3, pady=3)
