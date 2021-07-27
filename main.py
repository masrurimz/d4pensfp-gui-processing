from plotter import Plotter
from db import Db
from gui import GUI
from serialHandler import Serial


class Main:
    def __init__(self, channel=2, dataplot=1000):
        self.channel = channel
        self.dataplot = dataplot
        self.plotter = Plotter(self.dataplot)
        self.serial = Serial()
        self.data = Db(self.channel, self.plotter.updateData)
        self.window = GUI(self.plotter, self.data, self.serial)


if __name__ == '__main__':
    Main()
