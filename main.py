from plotter import Plotter
from db import Db
from gui import GUI

if __name__ == '__main__':
  plotter = Plotter(1000)
  data = Db(2)
  window = GUI(plotter)
