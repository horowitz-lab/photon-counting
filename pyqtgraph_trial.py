# -*- coding: utf-8 -*-
"""
Fuming Qiu
display a graph using pyqtgraph and qtpy packages
6/22/2017
"""
import sys.argv
import pyqtgraph as pg
from PyQt5 import QtWidgets
import numpy as np





print(type(w))

plot = pg.PlotWidget()


x = np.random.normal(size=1000)
y = np.random.normal(size=1000)
pg.plot(x, y, pen=None, symbol='o')  ## setting pen=None disables line drawing



def main():
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QWidget()
    
    
    
    
    print(type(MainApp))
    sys.exit(app.exec_())