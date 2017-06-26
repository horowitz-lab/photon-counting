#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 14:23:25 2017

@author: Houghton Yonge and Fuming Qiu
"""

#--------------------------------Library Imports------------------------------#

"""IMPORT STATEMENTS GO HERE"""
from QtPy import QtGui
import numpy as np
import sys
import SR400_GUI

class MainApp(QtGui.QMainWindow, SR400_GUI.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        self.setupUi(self)
        
def main():
    app = QtGui.QApplication(sys.argv)
    form = MainApp
    form.show()
    app.exec_()
    
if __name__ == '__main__':
    main()    
#------------------------------------GUI Setup--------------------------------#

"""GUI SETUP/DISPLAY GOES HERE"""

#------------------------------List of Widgets--------------------------------#

"""
13 QLabels:
    
    7 text labels:
    
        1. TSETLabel ("Duration of Time Bins")
        2. NPERLabel ("# of Periods")
        3. TimeLabel ("Time")
        4. GLabel ("Average Photon Count")
        5. TotLabel ("Overall Average Count")
        6. StDevLabel ("St. Dev")
        7. StErrLabel ("St. Err")
    
    6 Value Labels (VL)
    
        1. NPerVL
        2. TimeVL
        3. PhotonVL
        4. TotAvgVL
        5. StDevVL
        6. StErrVL
    
1 QSlider:
    NPerSlider
        Assigns new value to NPERIODS
            
1 QTextEdit:
    TSETBox
        Displays TSET <---> Assigns new value to TSET


2 QPushButtons:
    1. StartBtn
        Disables itself (state = DISABLED?)
        Starts data collection
            self.StartBtn.clicked.connect(StartFXN)
    2. StopBtn
        Stops data collection
            Updates data readings & variable values
            Adds latest data from group of NPERIODS observations to QTGraph
        Reenables StartBtn
            self.StopBtn.clicked.connect(StopFXN)
    
1 QTGraph
"""

#-----------------------Establishing Global(?) Variables----------------------#

GroupAvg = []
StopFlag = 0

"""Add entries to GroupAvg
for i in range(0, 10):
    GroupAvg.append(i)
    print(GroupAvg[i])
"""

ser = serial.Serial('COM#', 9600, serial.EIGHTBITS, seria.PARITY_EVEN, 
                    serial.STOPBITS_ONE, 2)

#Counter parameters controlled by GUI
NPERIODS = 0
TSET = 0
NPERInst = ''
TSETInst = ''

DWELL = '2e-3'

#-------------------------------Fuming's Functions----------------------------#

def enc(str):
    return str.encode('ascii')

def DataDump():
    ser.write(enc('ea \r'))
    data = ser.read(1000)
    return data

def BytesToList(BStr):
    dList = []
    curVal = 0
    #Iterate through bytes to add numbers to dList
    for b in BStr:
        #Ends a # if a carriage return is reached
        if b == 13:
            dList.append(curVal)
            curVal = 0
        #Otherwise, multiply curVal by 10 & add the next #.
        #ASCII - 48 is the numerical value.
        else:
            curVal = curVal * 10 + b - 48
    return dList

#----------------------------GUI Widget Functions-----------------------------#

#self.TSETBox.textchanged.connect(TSET_fxn)
def TSET_fxn():
    TSET = TSETBox.toPlainText()
    TSETInst = 'cp2, ' + TSET + '; '

#self.NPerSlider.valueChanged.connect(NPERSet)
def NPERSet():
    NPERIODS = NPERSlider.value()
    NPERInst= 'np' + str(NPERIODS) + '; '

#occurs within Start_fxn        
def Update():
    self.TimeVal.setText(str(Time))
    self.GVal.setText(str(GroupAvg[NTally]))
    self.TotVal.setText(str(TotalAvg))
    self.StDevVal.setText(str(StDev))
    self.StErrVal.setText(str(StErr))
    
#self.StopBtn.clicked.connect(StopFXN)
def Stop_fxn():
    StopFlag = 1
    ser.write(enc('cr \r'))
    StartBtn.setEnabled(True)

#-----------------------The Infinite Data Collection Loop---------------------#

def Start_fxn():
    StartBtn.setEnabled(False)
    ser.write(enc(TSETInst + '; ' 
                  + NPERInst + '; ' 
                  + 'dt ' + DWELL + '; '
                  + 'cr; cs \r'))
    while StopFlag == 0:
        time.sleep(6)
        data = DataDump()
        dataList = BytesToList(data)
        NTally = NTally + 1
        Time = NTally * (NPERIODS * (TSET + DWELL))
        GroupAvg.append(np.mean(dataList))
        TotalAvg = np.mean(GroupAvg)
        StDev = np.sd(GroupAvg)
        StErr = StDev/sqrt(NTally)
        Update()
        #plot data function goes here

print(GroupAvg)