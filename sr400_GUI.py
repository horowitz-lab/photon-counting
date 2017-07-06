# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SR400_GUI.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

#need these imports
from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph import PlotWidget
#need these imports

class Ui_Form(object):
    ##### not pyuic code start ###################################
    _timeList = []
    
    def __init__(self, Form):
        super().__init__()
        self.setupUi(Form)
        
    ######## not pyuic code end ########################
    
    
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(824, 630)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        
        self.TSETLabel = QtWidgets.QLabel(Form)
        self.TSETLabel.setMinimumSize(QtCore.QSize(0, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(False)
        font.setWeight(50)
        self.TSETLabel.setFont(font)
        self.TSETLabel.setObjectName("TSETLabel")
        self.gridLayout.addWidget(self.TSETLabel, 1, 0, 1, 3)
        
        self.TSETBox = QtWidgets.QTextEdit(Form)
        self.TSETBox.setMinimumSize(QtCore.QSize(71, 31))
        self.TSETBox.setMaximumSize(QtCore.QSize(71, 31))
        self.TSETBox.setObjectName("TSETBox")
        self.gridLayout.addWidget(self.TSETBox, 1, 3, 1, 1)
        
        self.PhotonForm = QtWidgets.QSplitter(Form)
        self.PhotonForm.setMinimumSize(QtCore.QSize(131, 31))
        self.PhotonForm.setOrientation(QtCore.Qt.Horizontal)
        self.PhotonForm.setObjectName("PhotonForm")
        self.PhotonLabel = QtWidgets.QLabel(self.PhotonForm)
        self.PhotonLabel.setMinimumSize(QtCore.QSize(91, 31))
        self.PhotonLabel.setMaximumSize(QtCore.QSize(101, 41))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.PhotonLabel.setFont(font)
        self.PhotonLabel.setObjectName("PhotonLabel")
        self.PhotonVL = QtWidgets.QLabel(self.PhotonForm)
        self.PhotonVL.setMinimumSize(QtCore.QSize(23, 31))
        self.PhotonVL.setMaximumSize(QtCore.QSize(16777215, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.PhotonVL.setFont(font)
        self.PhotonVL.setObjectName("PhotonVL")
        self.gridLayout.addWidget(self.PhotonForm, 1, 4, 1, 1)
        self.TotAvgForm = QtWidgets.QSplitter(Form)
        self.TotAvgForm.setMinimumSize(QtCore.QSize(181, 31))
        self.TotAvgForm.setOrientation(QtCore.Qt.Horizontal)
        self.TotAvgForm.setObjectName("TotAvgForm")
        self.TotAvgLabel = QtWidgets.QLabel(self.TotAvgForm)
        self.TotAvgLabel.setMinimumSize(QtCore.QSize(151, 31))
        self.TotAvgLabel.setMaximumSize(QtCore.QSize(175, 41))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.TotAvgLabel.setFont(font)
        self.TotAvgLabel.setObjectName("TotAvgLabel")
        self.TotAvgVL = QtWidgets.QLabel(self.TotAvgForm)
        self.TotAvgVL.setMinimumSize(QtCore.QSize(19, 31))
        self.TotAvgVL.setMaximumSize(QtCore.QSize(16777215, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.TotAvgVL.setFont(font)
        self.TotAvgVL.setObjectName("TotAvgVL")
        self.gridLayout.addWidget(self.TotAvgForm, 1, 5, 1, 2)
        self.BtnForm = QtWidgets.QGridLayout()
        self.BtnForm.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.BtnForm.setObjectName("BtnForm")
        self.StartBtn = QtWidgets.QPushButton(Form)
        self.StartBtn.setMinimumSize(QtCore.QSize(91, 51))
        self.StartBtn.setMaximumSize(QtCore.QSize(91, 51))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.StartBtn.setFont(font)
        self.StartBtn.setObjectName("StartBtn")
        self.BtnForm.addWidget(self.StartBtn, 0, 0, 1, 1)
        self.StopBtn = QtWidgets.QPushButton(Form)
        self.StopBtn.setMinimumSize(QtCore.QSize(91, 51))
        self.StopBtn.setMaximumSize(QtCore.QSize(91, 51))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.StopBtn.setFont(font)
        self.StopBtn.setObjectName("StopBtn")
        self.BtnForm.addWidget(self.StopBtn, 0, 1, 1, 1)
        self.gridLayout.addLayout(self.BtnForm, 2, 0, 1, 2)
        self.splitter_3 = QtWidgets.QSplitter(Form)
        self.splitter_3.setMinimumSize(QtCore.QSize(121, 31))
        self.splitter_3.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_3.setObjectName("splitter_3")
        self.TimeLabel = QtWidgets.QLabel(self.splitter_3)
        self.TimeLabel.setMinimumSize(QtCore.QSize(91, 31))
        self.TimeLabel.setMaximumSize(QtCore.QSize(105, 41))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.TimeLabel.setFont(font)
        self.TimeLabel.setObjectName("TimeLabel")
        self.TimeVL = QtWidgets.QLabel(self.splitter_3)
        self.TimeVL.setMinimumSize(QtCore.QSize(19, 31))
        self.TimeVL.setMaximumSize(QtCore.QSize(16777215, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.TimeVL.setFont(font)
        self.TimeVL.setObjectName("TimeVL")
        self.gridLayout.addWidget(self.splitter_3, 2, 2, 1, 2)
        self.splitter_2 = QtWidgets.QSplitter(Form)
        self.splitter_2.setMinimumSize(QtCore.QSize(121, 31))
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.StDevLabel = QtWidgets.QLabel(self.splitter_2)
        self.StDevLabel.setMinimumSize(QtCore.QSize(81, 31))
        self.StDevLabel.setMaximumSize(QtCore.QSize(91, 41))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.StDevLabel.setFont(font)
        self.StDevLabel.setObjectName("StDevLabel")
        self.StDevVL = QtWidgets.QLabel(self.splitter_2)
        self.StDevVL.setMinimumSize(QtCore.QSize(19, 31))
        self.StDevVL.setMaximumSize(QtCore.QSize(16777215, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.StDevVL.setFont(font)
        self.StDevVL.setObjectName("StDevVL")
        self.gridLayout.addWidget(self.splitter_2, 2, 4, 1, 1)
        self.splitter = QtWidgets.QSplitter(Form)
        self.splitter.setMinimumSize(QtCore.QSize(111, 31))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.StErrLabel = QtWidgets.QLabel(self.splitter)
        self.StErrLabel.setMinimumSize(QtCore.QSize(71, 31))
        self.StErrLabel.setMaximumSize(QtCore.QSize(81, 41))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.StErrLabel.setFont(font)
        self.StErrLabel.setObjectName("StErrLabel")
        self.StErrVL = QtWidgets.QLabel(self.splitter)
        self.StErrVL.setMinimumSize(QtCore.QSize(21, 31))
        self.StErrVL.setMaximumSize(QtCore.QSize(16777215, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.StErrVL.setFont(font)
        self.StErrVL.setObjectName("StErrVL")
        self.gridLayout.addWidget(self.splitter, 2, 5, 1, 1)
        
        #countrate graph
        self.rvtGraph = PlotWidget(Form, title = "Rate v Time", labels = 
                                   {"left" : "Rate (Counts/Second)", 
                                    "bottom" : "Time (seconds)"})
        self.rvtGraph.setObjectName("rvtGraph")
        self.rvtGraph.setXRange(0, 20)
        self.gridLayout.addWidget(self.rvtGraph, 3, 0, 1, 7)
        
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        
        
        ########### also extra#################################################
        Form.show()
        
        ######################## end extra #################


    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.TSETLabel.setText(_translate("Form", "Set Time Interval (s)"))
        self.TSETBox.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'.SF NS Text\'; font-size:13pt;\">1e6</span></p></body></html>"))
        self.PhotonLabel.setText(_translate("Form", "Photons"))
        self.PhotonVL.setText(_translate("Form", "0"))
        self.TotAvgLabel.setText(_translate("Form", "Total Average"))
        self.TotAvgVL.setText(_translate("Form", "0"))
        self.StartBtn.setText(_translate("Form", "START"))
        self.StopBtn.setText(_translate("Form", "STOP"))
        self.TimeLabel.setText(_translate("Form", "Time (s)"))
        self.TimeVL.setText(_translate("Form", "0"))
        self.StDevLabel.setText(_translate("Form", "St. Dev"))
        self.StDevVL.setText(_translate("Form", "0"))
        self.StErrLabel.setText(_translate("Form", "St. Err"))
        self.StErrVL.setText(_translate("Form", "0"))

