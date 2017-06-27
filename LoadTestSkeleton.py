#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 16:33:03 2017

@author: pguest
"""

import sys
from PyQt5 import *

qtCreatorFile = "LoadTest.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MainApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())