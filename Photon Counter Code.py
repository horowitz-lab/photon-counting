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

############# com port ##################################
comPort = 'COM7'
print('Check 1')
ser = serial.Serial(comPort, timeout = 0.5)

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
    
    Bases = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    Exponents = ["0",] + Bases + ["10", "11"]
    
    def __init__(self, parent=None):
        """inits the parent class, sets dwell time, and sets gui functions"""
        super(self.__class__, self).__init__(parent)
        print('Check 2')
        
        ser.write(self.enc('DT ' + str(self.DWELL) + ';'))
        
        #button connections to functions
        self.NPERSlider.valueChanged.connect(self.NPERSet)
        self.StartBtn.clicked.connect(self.Start_fxn)
        self.StopBtn.clicked.connect(self.Stop_fxn)
        
        #create a new file and properly name it #####################################
        
        
        
        
#----------------------GUI-Serial Connection Functions------------------------#

    def enc(self, str):
        """returns the ascii version of strings"""
        return str.encode('ascii')
        
    def DataDump(self):
        """asks the sr400 for data and reads and returns what is sent"""
        print("in data dump")
        ser.write(self.enc('ea \r'))        
        data = ser.read(1000)
        
        print("data", data)
        
        return data
        
    def BytesToList(self, BStr):
        """converts a bytestring to a list of ints"""
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
    
    def TSETtoInt(self, text):
        """converts a string of the form NUMeNUM to an int of seconds"""
        return int(text[0]) * 10 ** int(text[2:]) / (1e7)
#--------------------------GUI Widget Functions-------------------------------#
            
    def NPERSet(self):
        """sets the number of data counts per time bin using the slider"""
        print('Slider works!')
        self.NPERIODS = self.NPERSlider.value()
        NPERInst = 'np' + str(self.NPERIODS) + ' \r'
        print(NPERInst)
        ser.write(self.enc(NPERInst))
        
        
    def TSET_fxn(self):
        """sets the duration of a single data count in an instance variable
           and returns the string corresponding to that command on the sr400"""
        TSETText = self.TSETBox.toPlainText()
        print(TSETText)
        
        assert TSETText[0] in self.Bases, "Base must be a \
            non-zero number!"
        assert TSETText[1] == "e", "Second character must be e for \
            base-exponent notation!"
        assert TSETText[2] in self.Exponents, "Exponent must range \
            from 0 to 11!"
        
        #converts textbox string to int, creates and returns sr400 instruction
        self.TSET = self.TSETtoInt(TSETText)
        TSETInst = 'cp2, ' + TSETText + '; '
        return TSETInst
        
    def Stop_fxn(self):
        """sets gui to stop counting and sends a reset command to sr400"""
        self.StopBtn.setEnabled(False)
        print('Stop Button works!')
        self.StopFlag = 1
        self.GroupTally = 0
        ser.write(self.enc('cr \r'))
        self.StartBtn.setEnabled(True)
    
    def Start_fxn(self):
        """sends sr400 commands to set count parameters and gets data"""
        self.StopBtn.setEnabled(True)
        print('Start Button works!')
        
        self.StartBtn.setEnabled(False)
        #ser.write(self.enc(self.TSET_fxn() + ' \r'))
        ser.write(self.enc(self.TSET_fxn() + 'cr; FA \r'))
        
        print("where")
        
        #get the current time, variable of how long to wait for data
        curTime = time.clock()
        dataTime = self.NPERIODS * (self.TSET + self.DWELL)
        
        
        print("curTime" , curTime)
        print("dataTime" , dataTime)
        
        while (time.clock() - curTime) < dataTime:
            #query for other button
            a=1
            a+=1
        
        print("even more")
        
        #get new data, store it
        data = self.DataDump()
        
        print("data dump???")
        
        dataList = self.BytesToList(data)
        print(dataList)
        
        self.GroupTally += 1
        self.timeVal = self.GroupTally * dataTime
        self.GroupAvg.append(np.mean(dataList))
        self.TotalAvg = np.mean(self.GroupAvg)
        self.StDev = np.std(self.GroupAvg)
        self.StErr = self.StDev / np.sqrt(self.GroupTally)
        
        #graph newest vals and add values to 
        print("starting to graph")
        
        self.Graph.plot([self.timeVal], [self.GroupAvg[-1] / dataTime], 
                        pen = None, symbol = 'o')
        self._timeList.append(self.timeVal)
        
        #write new data to file ###############################################
        
        self.Update()
        print(self.GroupAvg)
            
    def Update(self):
        self.TimeVL.setText(str(self.timeVal))
        self.PhotonVL.setText(str(self.GroupAvg[-1])) ########################################
        self.TotAvgVL.setText(str(self.TotalAvg))
        self.StDevVL.setText(str(self.StDev))
        self.StErrVL.setText(str(self.StErr))

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QWidget()
    form = MainApp(window)
    app.exec_()

main()