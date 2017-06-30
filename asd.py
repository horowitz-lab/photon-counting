# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'asd.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):   
    
    def __init__(self):
        print("start")
    
    def start(self):
        """prints 1 forever"""
        self.stopBtn.clicked.
        print(type(self.stopBtn.clicked))
    
    def stop(self):
        """change start text to green"""
        self.startBtn.setStyleSheet("background-color: red")
    
        
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.stopBtn = QtWidgets.QPushButton(Dialog)
        self.stopBtn.setGeometry(QtCore.QRect(240, 240, 113, 32))
        self.stopBtn.setObjectName("stopBtn")
        self.startBtn = QtWidgets.QPushButton(Dialog)
        self.startBtn.setGeometry(QtCore.QRect(70, 240, 113, 32))
        self.startBtn.setObjectName("startBtn")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        
        self.startBtn.clicked.connect(self.start)
        self.stopBtn.clicked.connect(self.stop)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.stopBtn.setText(_translate("Dialog", "stop"))
        self.startBtn.setText(_translate("Dialog", "start"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    app.exec_()

