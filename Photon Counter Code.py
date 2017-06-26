#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 14:23:25 2017

@author: Houghton Yonge and Fuming Qiu
"""

#--------------------------------Library Imports------------------------------#

"""IMPORT STATEMENTS GO HERE"""
import numpy as np

#------------------------------------GUI Setup--------------------------------#

"""GUI SETUP/DISPLAY GOES HERE"""

#------------------------------List of Widgets--------------------------------#

"""
7 QLabels:
    1. TSETLabel ("Duration of Time Bins")
    2. NPERLabel ("# of Periods")
    3. TimeLabel ("Time")
    4. GLabel ("Average Photon Count")
    5. TotLabel ("Overall Average Count")
    6. StDevLabel ("St. Dev")
    7. StErrLabel ("St. Err")
    
1 QSlider:
    NPerSlider
        Assigns new value to NPERIODS
            
6 QTextEdits:
    1. TSETBox
        Displays TSET <---> Assigns new value to TSET
    2. TimeBox
        Displays Time
    3. GBox
        Displays GroupAvg
    4. TotBox
        Displays TotAvg
    5. StDevBox
        Displays StDev
    6. StErrBox
        Displays StErr

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

GroupTally = 0

Time = 0

GroupAvg = []
TotalAvg = 0
StDev = 0
StErr = 0

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

#occurs within StartFXN        
def Update():
    self.TimeVal.setText(str(Time))
    self.GVal.setText(str(GroupAvg[NTally]))
    self.TotVal.setText(str(TotalAvg))
    self.StDevVal.setText(str(StDev))
    self.StErrVal.setText(str(StErr))
    
#self.StopBtn.clicked.connect(StopFXN)
def Stop_fxn():
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