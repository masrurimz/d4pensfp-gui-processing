import numpy as np


class Db:
    """Data management, responsible for handling and dispathcing data
    """

    def __init__(self, total_channel):
        self.total_channel = total_channel
        self.__initilaze_data()

    def __initilaze_data(self):
        """Purge and initialize variable data storage
        """
        self.data = np.empty((0, self.total_channel))

    def add_data(self, data):
        """Add data to storage

        Args:
            data (numpy array[channel:n]): Data to be stored
        """
        self.data = np.concatenate([self.data, data])

    def save_data(self, filepath):
        """Save data to pickles

        Args:
            filepath (string): Folder path + file name
        """
        fullpath = filepath + ".npy"
        with open(fullpath, 'wb') as f:
            np.save(f, self.data)
            print(f'{self.data.shape} data has been saved to {fullpath}')
            self.__initilaze_data()

    def get_plot_data(self, plt_size):
        """Get array of data to be plotted

        Args:
            plt_size (integer): The lenght of data requested to be plotted

        Returns:
            numpy array: Array that requested to be plotted size (total_channel, plt_size)
        """
        return self.data[-plt_size:]
