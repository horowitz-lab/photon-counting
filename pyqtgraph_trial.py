# -*- coding: utf-8 -*-
"""
Fuming Qiu
display a graph using pyqtgraph and qtpy packages
6/22/2017
"""

import pyqtgraph as pg
from PyQt5 import QtGui
import numpy as np


app = QtGui.QApplication([])
w = QtGui.QWidget()

print(type(w))

plot = pg.PlotWidget()


x = np.random.normal(size=1000)
y = np.random.normal(size=1000)
pg.plot(x, y, pen=None, symbol='o')  ## setting pen=None disables line drawing

w.show()
app.exec_()