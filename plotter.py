import matplotlib.pyplot as plt
import numpy as np


class Plotter:
    """Signal graph object
    """

    def __init__(self, data2bePlotted):
        self.fig, self.axs = plt.subplots(nrows=2, ncols=2, figsize=(11, 7))
        self.ylim = (-3000, 3000)
        self.axs[0, 0].set_title('Channel 1')
        self.axs[0, 0].set_ylim(self.ylim)
        self.axs[0, 0].set_xlim(0, 100)
        self.axs[0, 1].set_title('Channel 2')
        self.axs[0, 1].set_ylim(self.ylim)
        self.axs[0, 1].set_xlim(0, 100)

        # Draw dummy line
        self.ydata = np.full((2, data2bePlotted), 0)
        self.lineCh1d, = self.axs[0, 0].plot(self.ydata[0])
        self.lineCh2d, = self.axs[0, 1].plot(self.ydata[1])
        self.fig.tight_layout()

    def updateData(self, newData: np.ndarray):
        data = newData.reshape(2, 1000)
        self.lineCh1d.set_ydata(data[0])
        self.lineCh2d.set_ydata(data[1])

        freqs1, ps1 = self.doFFT(data[0])
        freqs2, ps2 = self.doFFT(data[1])

        self.axs[1, 0].clear()
        self.axs[1, 1].clear()
        self.axs[1, 0].semilogy(freqs1, ps1)
        self.axs[1, 1].semilogy(freqs2, ps2)

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def doFFT(self, data):
        time_step = 1/1000
        ps = np.abs(np.fft.rfft(data))**2
        freqs = np.fft.rfftfreq(data.size, d=time_step)
        idx = np.argsort(freqs)

        return freqs[idx], ps[idx]
