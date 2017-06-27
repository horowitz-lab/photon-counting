# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sr400_GUI.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph import PlotWidget
import numpy as np

class Ui_Form(QtWidgets.QWidget):
    _x = []
    _y = []

    def __init__(self, Form):
        super().__init__()
        self.setupUi(Form)

    def setData(self):
        self._x = np.random.normal(size=100)
        self._y = np.random.normal(size=100)
        
    def setupUi(self, Form):
        #some toy data
        self.setData()
        
        Form.setObjectName("Form")
        Form.resize(674, 275)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.TSETForm = QtWidgets.QSplitter(Form)
        self.TSETForm.setOrientation(QtCore.Qt.Horizontal)
        self.TSETForm.setObjectName("TSETForm")
        self.TSETLabel = QtWidgets.QLabel(self.TSETForm)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(False)
        font.setWeight(50)
        self.TSETLabel.setFont(font)
        self.TSETLabel.setObjectName("TSETLabel")
        self.TSETBox = QtWidgets.QTextEdit(self.TSETForm)
        self.TSETBox.setObjectName("TSETBox")
        self.gridLayout.addWidget(self.TSETForm, 0, 0, 1, 1)
        self.TimeForm = QtWidgets.QSplitter(Form)
        self.TimeForm.setOrientation(QtCore.Qt.Horizontal)
        self.TimeForm.setObjectName("TimeForm")
        self.TimeLabel = QtWidgets.QLabel(self.TimeForm)
        font = QtGui.QFont()
        font.setPointSize(21)
        self.TimeLabel.setFont(font)
        self.TimeLabel.setObjectName("TimeLabel")
        self.TimeVL = QtWidgets.QLabel(self.TimeForm)
        font = QtGui.QFont()
        font.setPointSize(21)
        self.TimeVL.setFont(font)
        self.TimeVL.setObjectName("TimeVL")
        self.gridLayout.addWidget(self.TimeForm, 0, 1, 1, 2)
        self.NPERForm = QtWidgets.QSplitter(Form)
        self.NPERForm.setOrientation(QtCore.Qt.Horizontal)
        self.NPERForm.setObjectName("NPERForm")
        self.NPERLabel = QtWidgets.QLabel(self.NPERForm)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(False)
        font.setWeight(50)
        self.NPERLabel.setFont(font)
        self.NPERLabel.setObjectName("NPERLabel")
        self.NPERSlider = QtWidgets.QSlider(self.NPERForm)
        self.NPERSlider.setMinimum(1)
        self.NPERSlider.setMaximum(2000)
        self.NPERSlider.setProperty("value", 1)
        self.NPERSlider.setOrientation(QtCore.Qt.Horizontal)
        self.NPERSlider.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.NPERSlider.setTickInterval(100)
        self.NPERSlider.setObjectName("NPERSlider")
        self.NPERVL = QtWidgets.QLabel(self.NPERForm)
        font = QtGui.QFont()
        font.setPointSize(21)
        self.NPERVL.setFont(font)
        self.NPERVL.setObjectName("NPERVL")
        self.gridLayout.addWidget(self.NPERForm, 1, 0, 1, 1)
        self.PhotonForm = QtWidgets.QSplitter(Form)
        self.PhotonForm.setOrientation(QtCore.Qt.Horizontal)
        self.PhotonForm.setObjectName("PhotonForm")
        self.PhotonLabel = QtWidgets.QLabel(self.PhotonForm)
        font = QtGui.QFont()
        font.setPointSize(21)
        self.PhotonLabel.setFont(font)
        self.PhotonLabel.setObjectName("PhotonLabel")
        self.PhotonVL = QtWidgets.QLabel(self.PhotonForm)
        font = QtGui.QFont()
        font.setPointSize(21)
        self.PhotonVL.setFont(font)
        self.PhotonVL.setObjectName("PhotonVL")
        self.gridLayout.addWidget(self.PhotonForm, 1, 1, 1, 1)
        self.StDevForm = QtWidgets.QSplitter(Form)
        self.StDevForm.setOrientation(QtCore.Qt.Horizontal)
        self.StDevForm.setObjectName("StDevForm")
        self.StDevLabel = QtWidgets.QLabel(self.StDevForm)
        font = QtGui.QFont()
        font.setPointSize(21)
        self.StDevLabel.setFont(font)
        self.StDevLabel.setObjectName("StDevLabel")
        self.StDevVL = QtWidgets.QLabel(self.StDevForm)
        font = QtGui.QFont()
        font.setPointSize(21)
        self.StDevVL.setFont(font)
        self.StDevVL.setObjectName("StDevVL")
        self.gridLayout.addWidget(self.StDevForm, 1, 2, 1, 1)
        self.BtnForm = QtWidgets.QSplitter(Form)
        self.BtnForm.setOrientation(QtCore.Qt.Horizontal)
        self.BtnForm.setObjectName("BtnForm")
        self.StartBtn = QtWidgets.QPushButton(self.BtnForm)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.StartBtn.setFont(font)
        self.StartBtn.setObjectName("StartBtn")
        self.StopBtn = QtWidgets.QPushButton(self.BtnForm)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.StopBtn.setFont(font)
        self.StopBtn.setObjectName("StopBtn")
        self.gridLayout.addWidget(self.BtnForm, 2, 0, 1, 1)
        self.TotAvgForm = QtWidgets.QSplitter(Form)
        self.TotAvgForm.setOrientation(QtCore.Qt.Horizontal)
        self.TotAvgForm.setObjectName("TotAvgForm")
        self.TotAvgLabel = QtWidgets.QLabel(self.TotAvgForm)
        font = QtGui.QFont()
        font.setPointSize(21)
        self.TotAvgLabel.setFont(font)
        self.TotAvgLabel.setObjectName("TotAvgLabel")
        self.TotAvgVL = QtWidgets.QLabel(self.TotAvgForm)
        font = QtGui.QFont()
        font.setPointSize(21)
        self.TotAvgVL.setFont(font)
        self.TotAvgVL.setObjectName("TotAvgVL")
        self.gridLayout.addWidget(self.TotAvgForm, 2, 1, 1, 1)
        self.StErrForm = QtWidgets.QSplitter(Form)
        self.StErrForm.setOrientation(QtCore.Qt.Horizontal)
        self.StErrForm.setObjectName("StErrForm")
        self.StErrLabel = QtWidgets.QLabel(self.StErrForm)
        font = QtGui.QFont()
        font.setPointSize(21)
        self.StErrLabel.setFont(font)
        self.StErrLabel.setObjectName("StErrLabel")
        self.StErrVL = QtWidgets.QLabel(self.StErrForm)
        font = QtGui.QFont()
        font.setPointSize(21)
        self.StErrVL.setFont(font)
        self.StErrVL.setObjectName("StErrVL")
        self.gridLayout.addWidget(self.StErrForm, 2, 2, 1, 1)
        self.Graph = PlotWidget(Form)
        self.Graph.setObjectName("Graph")
        self.gridLayout.addWidget(self.Graph, 3, 0, 1, 3)
        self.Graph.plot(self._x, self._y, pen = None, symbol = 'o')

        self.retranslateUi(Form)
        self.NPERSlider.valueChanged['int'].connect(self.NPERVL.setNum)
        QtCore.QMetaObject.connectSlotsByName(Form)
        
        Form.show()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.TSETLabel.setText(_translate("Form", "Duration of Time Bins (s)"))
        self.TSETBox.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'.Lucida Grande UI\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'.SF NS Text\';\">1</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'.SF NS Text\';\"><br /></p></body></html>"))
        self.TimeLabel.setText(_translate("Form", "Time (s)"))
        self.TimeVL.setText(_translate("Form", "0"))
        self.NPERLabel.setText(_translate("Form", "# of Bins"))
        self.NPERVL.setText(_translate("Form", "0"))
        self.PhotonLabel.setText(_translate("Form", "Photons"))
        self.PhotonVL.setText(_translate("Form", "0"))
        self.StDevLabel.setText(_translate("Form", "St. Dev"))
        self.StDevVL.setText(_translate("Form", "0"))
        self.StartBtn.setText(_translate("Form", "START"))
        self.StopBtn.setText(_translate("Form", "STOP"))
        self.TotAvgLabel.setText(_translate("Form", "Total Average"))
        self.TotAvgVL.setText(_translate("Form", "0"))
        self.StErrLabel.setText(_translate("Form", "St. Err"))
        self.StErrVL.setText(_translate("Form", "0"))

"""
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
"""
