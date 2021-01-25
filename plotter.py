import matplotlib.pyplot as plt


class Plotter:
    """Signal graph object
    """

    def __init__(self, data2bePlotted):
        self.fig, self.axs = plt.subplots(nrows=2, ncols=2, figsize=(11, 7))
        self.axs[0, 0].set_title('Channel 1')
        self.axs[0, 1].set_title('Channel 1')
        self.fig.tight_layout()

        # self.fig.figsize=(1200,20)
        # self.fig
        self.xdata = []
        self.ydata = []
        self.data2bePlotted = data2bePlotted

    def updateData(self, newData):
        print(newData)
