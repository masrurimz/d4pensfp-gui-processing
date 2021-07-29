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
        self.axs[1, 0].plot(freqs1, ps1)
        self.axs[1, 1].plot(freqs2, ps2)

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def doFFT(self, x, fs=1000, win=None, ref=1):
        """
        Calculate spectrum in dB scale
        Args:
            x: input signal
            fs: sampling frequency
            win: vector containing window samples (same length as x).
                If not provided, then rectangular window is used by default.
            ref: reference value used for dBFS scale. 32768 for int16 and 1 for float
        Returns:
            freq: frequency vector
            s_db: spectrum in dB scale
        """
        N = len(x)  # Length of input sequence
        if win is None:
            win = np.ones(N)
        if len(x) != len(win):
            print('Window Lenght = ', len(win), 'Signal Length = ', len(x))
            raise ValueError('Signal and window must be of the same length')
        x = x * win
        # Calculate real FFT and frequency vector
        sp = np.fft.rfft(x)
        freq = np.arange((N / 2) + 1) / (float(N) / fs)

        # Scale the magnitude of FFT by window and factor of 2,
        # because we are using half of FFT spectrum.
        s_mag = np.abs(sp) * 2 / np.sum(win)

        # Convert to dBFS
        s_dbfs = 20 * np.log10(s_mag/ref)

        if len(freq) > len(s_dbfs):
            freq = freq[:len(s_dbfs)]
        if len(s_dbfs) > len(freq):
            s_dbfs = s_dbfs[:len(freq)]

        return freq, s_dbfs
