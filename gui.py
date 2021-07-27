from tkinter import *
import tkinter as tk
import numpy as np

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

cnt = 0


def callbackData():
    global cnt
    cnt += 1
    cnt += 100
    return dummyData(cnt)


time = np.arange(0, 10, 0.001)
amplitude = (2000 * np.sin(time)) + 2000


def dummyData(n):
    print("Data generated with n=", n)
    time = np.arange(n, n+1, 0.001)
    row = (2000 * np.sin(time)) + 2000
    # row = np.arange(n, n+1000)
    return np.concatenate([row, row]).reshape(1000, 2)


class GUI(Frame):
    def __init__(self, plotter, db, serial):
        Frame.__init__(self)
        self.plotter = plotter
        self.db = db
        self.serial = serial
        self.master = tk.Tk()
        self.figure = plotter.fig
        self.port = StringVar(self.master)
        self.portList = []
        self.startUp()

    def startUp(self):
        self.master.geometry('1800x1000')
        self.master.title("EMG Real Time Plot")
        self.initComponent()
        self.configureLayout()
        self.master.mainloop()
        self.port.set("Monday")

    def initComponent(self):
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.master)
        self.lbGesture = tk.Label(self.master, text="Detected Gesture")
        self.txtGesture = tk.Label(self.master, text="Gesture A, B, C")
        self.lbAction = tk.Label(self.master, text="Detected Action")
        self.txtAction = tk.Label(self.master, text="Action A, B, C")
        self.lbConnectionStats = tk.Label(self.master, text="Status Koneksi")
        self.txtConnectionStats = tk.Label(
            self.master, text="Connected Disconnect")
        self.btConnection = tk.Button(self.master, text="Connect/Disconnect")
        self.lbPort = tk.Label(self.master, text="Daftar Port")
        self.optPortList = tk.OptionMenu(
            self.master, self.port, *self.portList)
        self.btPortScan = tk.Button(
            self.master, text="Scan", command=self.updatePortList)
        self.lbTransmissionStats = tk.Label(
            self.master, text="Status Transmisi")
        self.txtTransmissionStats = tk.Label(
            self.master, text="Receiving/Stop")
        self.btTransmissionStats = tk.Button(
            self.master, text="Start/Stop Receiving")
        self.lbFileName = tk.Label(self.master, text="File Name")
        self.inptFileName = tk.Entry(self.master, text="")
        self.inptFileIndex = tk.Entry(self.master, text="")
        self.txtFileStats = tk.Label(self.master, text="Saving")
        self.btFileSave = tk.Button(self.master, text="Save Data")
        self.btQuit = tk.Button(
            master=self.master, text="Quit", command=self.master.quit)
        self.btUpdate = tk.Button(master=self.master, text="Update",
                                  command=lambda: self.db.add_data(callbackData()))

    def configureLayout(self):
        self.lbGesture.grid(row=1, column=0, columnspan=10)
        self.txtGesture.grid(row=2, column=0, columnspan=10)
        self.lbAction.grid(row=1, column=11, columnspan=10)
        self.txtAction.grid(row=2, column=11, columnspan=10)

        self.canvas.get_tk_widget().grid(row=3, column=1, rowspan=13, columnspan=20)
        self.lbConnectionStats.grid(row=1, column=21, columnspan=5)
        self.txtConnectionStats.grid(row=2, column=21, columnspan=5)
        self.btConnection.grid(row=3, column=21, columnspan=5, sticky='we')
        self.lbPort.grid(row=4, column=21, columnspan=5)
        self.optPortList.grid(row=5, column=21, columnspan=3, sticky='we')
        self.btPortScan.grid(row=5, column=24, columnspan=2, sticky='we')
        self.lbTransmissionStats.grid(row=6, column=21, columnspan=5)
        self.txtTransmissionStats.grid(row=7, column=21, columnspan=5)
        self.btTransmissionStats.grid(
            row=8, column=21, columnspan=5, sticky='we')
        self.lbFileName.grid(row=10, column=21, columnspan=5)
        self.inptFileName.grid(
            row=11, column=21, columnspan=3)
        self.inptFileIndex.grid(
            row=11, column=24, columnspan=2)
        self.txtFileStats.grid(
            row=12, column=21, columnspan=5)
        self.btFileSave.grid(row=13, column=21, columnspan=5, sticky='we')
        self.btQuit.grid(row=14, column=21, columnspan=5, sticky='we')
        self.btUpdate.grid(row=15, column=21, columnspan=5, sticky='we')

    def configureFunctional(self):
        self.btPortScan.configure(command=lambda: self.serial.scanAllPort())
        listPort = self.serial.scanAllPort()
        print(listPort)

    def updatePortList(self):
        self.portList = self.serial.scanAllPort()
        menu = self.optPortList["menu"]
        menu.delete(0, "end")
        for string in self.portList:
            menu.add_command(label=string,
                             command=lambda value=string: self.port.set(value))
