import matplotlib.pyplot as plt
import numpy as np


class Plotter:
    """Signal graph object
    """

    def __init__(self, data2bePlotted):
        self.fig, self.axs = plt.subplots(nrows=2, ncols=2, figsize=(11, 7))
        self.ylim = (0, 1000)
        self.axs[0, 0].set_title('Channel 1')
        self.axs[0, 0].set_ylim(self.ylim)
        self.axs[0, 1].set_title('Channel 2')
        self.axs[0, 1].set_ylim(self.ylim)

        # Draw dummy line
        dummy = np.zeros(data2bePlotted)
        self.line1, = self.axs[0, 0].plot(dummy)
        self.line2, = self.axs[0, 1].plot(dummy)
        self.fig.tight_layout()

        # self.fig.figsize=(1200,20)
        # self.fig
        self.xdata = []
        self.ydata = []
        self.data2bePlotted = data2bePlotted

    def updateData(self, newData):
        print(newData)
        self.line1.set_ydata(newData[0])
        self.line2.set_ydata(newData[1])
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
