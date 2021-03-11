from tkinter import *
import tkinter as tk
import tkinter.messagebox as tkMessageBox


import numpy as np
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure


from plotter import Plotter
from db import Db
# from mining import *

cnt = 0


def helloCallBack():
    tkMessageBox.showinfo("Hello Python", "Hello World")


def callbackData():
    global cnt
    cnt += 100
    return dummyData(cnt)


def dummyData(n):
    print("Data generated with n=", n)
    row = np.arange(n, n+1000)
    return np.concatenate([row, row]).reshape(2, 1000)


class GUI(Frame):
    def __init__(self, plotter):
        Frame.__init__(self)
        self.plotter = plotter
        self.master = tk.Tk()
        self.figure = plotter.fig

    def initWindow(self):
        self.master.geometry('1300x700')
        self.master.title("EMG Real Time Plot")
        self.initGraph()
        self.initControl()
        self.master.mainloop()

    def initGraph(self):
        canvas = FigureCanvasTkAgg(self.figure, master=self.master)
        canvas.get_tk_widget().grid(row=0, column=0, rowspan=6)

    def initControl(self):
        lbConnection = tk.Label(self.master, text="Connection Status").grid(
            row=0, column=1, sticky=tk.NSEW, padx=5, pady=5)
        btConnection = tk.Button(self.master, text="Connect").grid(
            row=1, column=1, sticky=tk.NSEW, padx=5, pady=2)
        lbFileName = tk.Label(self.master, text="File Name").grid(
            row=2, column=1, sticky=tk.NSEW, padx=2, pady=2)
        etFileName = tk.Entry(self.master, text="").grid(
            row=3, column=1, sticky=tk.NSEW, padx=2, pady=2)
        btSave = tk.Button(self.master, text="Save").grid(
            row=4, column=1, sticky=tk.NSEW, padx=2, pady=2)
        btQuit = tk.Button(master=self.master, text="Quit", command=self.master.quit).grid(
            row=5, column=1, sticky=tk.NSEW, padx=3, pady=3)
        btUpdate = tk.Button(master=self.master, text="Update", command=lambda: self.plotter.updateData(callbackData())).grid(
            row=6, column=1, sticky=tk.NSEW, padx=3, pady=3)

window = GUI(Plotter(1000))
window.initWindow()
