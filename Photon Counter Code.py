#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 14:23:25 2017

@author: Houghton Yonge and Fuming Qiu
"""

#--------------------------------Library Imports------------------------------#

from PyQt5 import QtWidgets
import numpy as np
import sys
import sr400_GUI
import serial
import time

"""
#############com port##################################
comPort = 'COM5'

print('Check 1')
ser = serial.Serial(comPort, timeout = 2)"""


class MainApp(sr400_GUI.Ui_Form):
    #-------------------Establishing Variables--------------------------------#
    timeVal = 0
    TotalAvg = 0
    StDev = 0
    StErr = 0
    
    GroupTally = 0
    GroupAvg = []
    StopFlag = 0
    
    DWELL = 2e-3
    
    #Counter parameters controlled by GUI
    NPERIODS = 0
    TSET = 0
    NPERInst = ''
    TSETInst = ''
    
    Bases = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    Exponents = ["0",] + Bases + ["10", "11"]
    
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        print('Check 2')
        
        #button connections to functions
        self.NPERSlider.valueChanged.connect(self.NPERSet)
        self.StartBtn.clicked.connect(self.Start_fxn)
        self.StopBtn.clicked.connect(self.Stop_fxn)
        self.TSETBox.textChanged.connect(self.TSET_fxn)
#----------------------GUI-Serial Connection Functions------------------------#

    def enc(self, str):
        return str.encode('ascii')
        
    def DataDump(self):
        ser.write(self.enc('ea \r'))
        data = ser.read(1000)
        return data
        
    def BytesToList(self, BStr):
        dList = []
        curVal = 0
        #Iterate through bytes to add numbers to dList
        for b in BStr:
            #Ends a # if a carriage return is reached
            if b == 13:
                dList.append(curVal)
                curVal = 0
            #Otherwise, multiply curVal by 10 & ad the next #.
            #ASCII - 48 is the numerical value.
            else:
                curVal = curVal * 10 + b - 48
        return dList
    
#--------------------------GUI Widget Functions-------------------------------#
            
    def NPERSet(self):
        print('Slider works!')
        NPERIODS = self.NPERSlider.value()
        NPERInst = 'np' + str(NPERIODS) + ' \r'
        print(NPERInst)
        ser.write(self.enc(NPERInst))
        
        
    def TSET_fxn(self):
        print('Text box works!')
        TSETText = self.TSETBox.toPlainText()
        assert TSETText[0] in self.Bases, "Base must be a \
            non-zero number!"
        assert TSETText[1] == "e", "Second character must be e for \
            base-exponent notation!"
        assert TSETText[2] in self.Exponents, "Exponent must range \
            from 0 to 11!"
        self.TSET = int(TSETText)
        TSETInst = 'cp2, ' + TSETText + ' \r'
        ser.write(self.enc(TSETInst))
        
    def Stop_fxn(self):
        self.StopBtn.setEnabled(False)
        print('Stop Button works!')
        self.StopFlag = 1
        self.GroupTally = 0
        ser.write(self.enc('cr \r'))
        self.StartBtn.setEnabled(True)
    
    def Start_fxn(self):
        self.StopBtn.setEnabled(True)
        print('Start Button works!')
        
        #making start do new random graph data
        self.setData()
        self.Graph.plot(self._x, self._y, pen = None, symbol = 'o')
        self.StartBtn.setEnabled(False)
        ser.write(self.enc(str(self.DWELL) + '; cr; cs \r'))
        while self.StopFlag == 0:
            time.sleep(6)
            data = self.DataDump()
            dataList = self.BytesToList(data)
            self.GroupTally += 1
            self.timeVal = self.GroupTally * (
                           self.NPERIODS * (self.TSET + self.DWELL))
            self.GroupAvg.append(np.mean(dataList))
            self.TotalAvg = np.mean(self.GroupAvg)
            self.StDev = np.std(self.GroupAvg)
            self.StErr = self.StDev / np.sqrt(self.GroupTally)
            self.Graph.plot(self._x, self._y, pen = None, symbol = 'o')
            self.Update()
            print(self.GroupAvg)
            
    def Update(self):
        self.TimeVL.setText(str(self.timeVal))
        self.PhotonVL.setText(str(self.GroupAvg[self.GroupTally])) ########################################
        self.TotAvgVL.setText(str(self.TotalAvg))
        self.StDevVL.setText(str(self.StDev))
        self.StErrVL.setText(str(self.StErr))

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QWidget()
    form = MainApp(window)
    app.exec_()

main()