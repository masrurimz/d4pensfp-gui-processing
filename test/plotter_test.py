import unittest
import numpy as np

import sys
sys.path.insert(1, 'D:/Documents/Kuliah/Project Akhir/Progress3/GUI')


class TestPlotterMethods(unittest.TestCase):
    def setUp(self):
        from plotter import Plotter
        self.plt = Plotter(1000)
