import unittest
import numpy as np

import sys
sys.path.insert(1, 'D:/Documents/Kuliah/Project Akhir/Progress3/GUI')

class TestDbMethods(unittest.TestCase):
    def setUp(self):
        from db import Db
        self.Db = Db

        self.total_channel = 2
        self.total_data = 1000

        self.db = self.Db(self.total_channel)
        data = np.arange(self.total_data *
                         2).reshape((self.total_data, self.total_channel))
        self.db.add_data(data)

    def test_init_Storage(self):
        """Test Data Initialization
        """
        self.db = self.Db(self.total_channel)
        self.assertEqual(self.db.data.shape, (0, self.total_channel),
                         'Data should have size (0, 2)')

    def test_add_data(self):
        """Test add data does it add the added data size
        """
        self.assertEqual(self.db.data.shape, (1000, self.total_channel),
                         'Data should have size (1000,2)')

    def test_get_plot_data(self):
        """Test to retrieve data to be plotted
        """
        plot_size = 500

        data_plotted = self.db.get_plot_data(plot_size)
        self.assertEqual(data_plotted.shape, (plot_size, self.total_channel))

    def test_save_data(self):
        """Test saving buffered data
        Function should save data to files.npy and clear cached data
        """
        file_path = "test/test"
        self.db.save_data(file_path)

        from os import path, remove
        file_path_exetension = file_path + ".npy"
        res = path.exists(file_path_exetension)
        self.assertTrue(res, "Npy test/test.npy should exist")

        if res: remove(file_path_exetension)
        res = path.exists(file_path_exetension)
        self.assertFalse(res, "Npy test/test.npy should not exist")


    def test_save_data_clear_buffer(self):
        """Test save data purge cache
        """        
        self.test_save_data()

        self.assertEqual(self.db.data.shape, (0, self.total_channel),
                         'Data should have size (0, 2) after saving')
        

if __name__ == '__main__':
    unittest.main()
