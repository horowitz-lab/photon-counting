#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 14:23:25 2017

@author: Houghton Yonge and Fuming Qiu
"""

#--------------------------------Library Imports------------------------------#

from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer
import numpy as np
import sys
import sr400_GUI
import visa
import time

import os
import datetime

#--------------------------Setting Up GPIB Connectivity-----------------------#

rm = visa.ResourceManager()
instList = rm.list_resources()
print(instList)

GPIBName = ''
for instr in instList:
    if instr.find('GPIB') == 0:
        GPIBName = instr

sr400 = rm.open_resource(GPIBName)
sr400.timeout = 1000

#--------------------------Data File Functionality----------------------------#

"""
This creates a filename in the format yyyy-mm-dd\function\count\description.txt
where \ is used to denote separate sections that are not space-separated.
"""
Date = datetime.date.today().isoformat()
RunCount = 0

def CreateFile(Date, RunCount):
    if RunCount == 0:
        return Date
    else if RunCount >= 1:
        return Date + "_" + str(RunCount)

Folders = ["Data", Date]
Temp = ["Temporary", Date]

mainDir = os.getcwd()
tempDir = os.getcwd()
    

#----------------------------Establishing Variables---------------------------#

class MainApp(sr400_GUI.Ui_Form):

    TimeValList = [0]
    CountsList = [0]
    CountRateList = [0]
    
    TotalAvg = 0
    Samples = 0
    StDev = 0
    StErr = 0
    
    GroupTally = 0
    GroupAvg = []
    StopFlag = 0
    
    StartTime = 0
    DWELL = 2e-3
    
    
    #Counter parameters controlled by GUI
    TimeInt = 3
    NPERIODS = 0
    TSET = 0
    NPERInst = ''
    
    Bases = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    Exponents = ["0",] + Bases + ["10", "11"]
    
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        print('Check 2')
        
        sr400.write('DT ' + (str(self.DWELL)) + '; ' + 'cp2, 1e7')
        
        #button connections to functions
        self.NPERSlider.valueChanged.connect(self.NPERSet)
        self.StartBtn.clicked.connect(self.Start_fxn)
        self.StopBtn.clicked.connect(self.Stop_fxn)
        
        self.graphTimer = QTimer()
        self.graphTimer.setSingleShot(False)
        self.graphTimer.timeout.connect(self.Update)
        
#------------------------GUI-GPIB Connection Functions------------------------#

    def DataDump(self):
        """asks the sr400 for data and reads and returns what is sent"""
        print("In data dump... \n")
        data = sr400.query("ea \r")
        print("Data: ", data)
        return data
        
    def BytesToInt(self, BStr):
        """converts a bytestring to a list of ints"""
        curVal = 0
        #Iterate through bytes to add numbers to dList
        for b in BStr:
            #Ends a # if a carriage return is reached
            if b == 13:
                curVal = 0
            #Otherwise, multiply curVal by 10 & ad the next #.
            #ASCII - 48 is the numerical value.
            else:
                curVal = curVal * 10 + b - 48
        return 0
    
    def TSETtoInt(self, text):
        """converts a string of the form NUMeNUM to an int"""
        return int(text[0]) * 10 ** int(text[2:]) / (1e7)
    
#--------------------------GUI Widget Functions-------------------------------#
            
    def NPERSet(self):
        print('Slider works!')
        NPERIODS = self.NPERSlider.value()
        NPERInst = 'np' + str(NPERIODS)
        print(NPERInst)
        sr400.write(NPERInst)
        
    def TSET_fxn(self):
        TSETText = self.TSETBox.toPlainText()
        print(TSETText)
        assert TSETText[0] in self.Bases, "Base must be a \
            non-zero number!"
        assert TSETText[1] == "e", "Second character must be e for \
            base-exponent notation!"
        assert TSETText[2] in self.Exponents, "Exponent must range \
            from 0 to 11!"
        self.TSET = self.TSETtoInt(TSETText)
        TSETInst = 'cp2, ' + TSETText
        return TSETInst
        
    def Stop_fxn(self):
        """
        self.StopBtn.setEnabled(False)
        print('Stop Button works!')
        self.StopFlag = 1
        self.GroupTally = 0
        """
        sr400.write('cr')
        self.StartBtn.setEnabled(True)
        self.graphTimer.stop()
    
    def Start_fxn(self):
        self.StopBtn.setEnabled(True)
        print('Start Button works!')
        sr400.write('cr; cs')
        self.StartBtn.setEnabled(False)
        
        print("Where?")
        
        self.StartTime = time.clock()
        loopTime = time.clock()
        
        print("Current Time: ", loopTime)
        
        self.graphTimer.start(self.TimeInt * 1000)
        
    def Update(self):
        
        #Most recent photon count
        data = sr400.query("xa \r")
        print("Current Count: ", type(data))
        
        print(self.CountsList[-1])
        self.CountsList.append(int(data))
        print("Added to CountsList!\n")
        print(self.CountsList)
        
        self.TimeValList.append(time.clock() - self.StartTime)
        self.CountRateList.append(self.CountsList[-1] / self.TimeValList[-1])
        
        self.Samples += 1
        self.TotalAvg = np.mean(self.CountsList)
        self.StDev = np.std(self.CountsList)
        self.StErr = self.StDev / np.sqrt(self.Samples)
        
        print("Starting to graph...")
        
        self.Graph.plot(self.TimeValList[1:], self.CountsList[1:],
                        pen = None, symbol = 'o')
        
        self.TimeVL.setText(str(self.TimeValList[-1]))
        self.PhotonVL.setText(str(self.CountsList[-1]))
        self.TotAvgVL.setText(str(self.TotalAvg))
        self.StDevVL.setText(str(self.StDev))
        self.StErrVL.setText(str(self.StErr))

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QWidget()
    form = MainApp(window)
    app.exec_()

main()