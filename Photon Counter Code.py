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
    timeValsList = [0]
    countsList = [0]
    countRateList = [0]
    TotalAvg = 0
    numSamples = 0
    StDev = 0
    StErr = 0
    
    StopFlag = 0
    
    DWELL = 2e-3
    
    #Counter parameters controlled by GUI
    timeInterval = 3
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
        ser.write(self.enc('xa \r'))        
        data = ser.read(1000)
        
        print("data", data)
        
        return data
        
    def BytesToInt(self, BStr):
        """converts a bytestring to an ints"""
        curVal = 0
        #Iterate through bytes to convert the number
        for byte in BStr:
            #returns the number at carriage return
            if byte == 13:
                return curVal
            #Otherwise, multiply curVal by 10 & add the next #.
            #ASCII - 48 is the numerical value.
            else:
                curVal = curVal * 10 + byte - 48
        
        print("failed for some reason")
        return 0
    
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
        ser.write(self.enc(self.TSET_fxn() + 'cr; cs \r'))
        
        print("where")
        
        #get the current time, variable of how long to wait for data
        startTime = time.clock()
        loopTime = time.clock()
        
        print("curTime" , loopTime)
        
        while 1:
            #if not yet at next interval
            if (time.clock() - loopTime) < self.timeInterval: 
                #query for other button
                a=1
                a+=1
                
            #take new data
            else:
                #get the current count value and store the additional counts
                ser.write(self.enc("xa \r"))
                curCount = self.BytesToInt(ser.read(15)) #12 is arbitrary
                
                print("curCount", curCount)
                
                self.countsList.append(curCount - self.countsList[-1])
                print(self.countsList[-1])
                print(self.countsList)
                
                #get elapsed time and add it to time list, add to rate list
                self.timeValsList.append(time.clock() - startTime)
                self.countRateList.append(self.countsList[-1] / 
                                          self.timeValsList[-1])
                
                #increment numSamples, calculate average, st dev and st error
                self.numSamples += 1
                self.TotalAvg = np.mean(self.countsList)
                self.StDev = np.std(self.countsList)
                self.StErr = self.StDev / np.sqrt(self.numSamples)
                
                #graph newest vals, ignore the first (0,0) pair
                print("starting to graph")
                
                self.Graph.plot(self.timeValsList[1:], self.countRateList[1:], 
                                pen = None, symbol = 'o')
                time.sleep(0.01)                
                #write new data to file ###############################################
                
                
                #reset current time as loopTime to prepare for next iteration
                loopTime = time.clock()
                self.Update()
                
    def Update(self):
        self.TimeVL.setText(str(self.timeValsList[-1]))
        self.PhotonVL.setText(str(self.countsList[-1])) ########################################
        self.TotAvgVL.setText(str(self.TotalAvg))
        self.StDevVL.setText(str(self.StDev))
        self.StErrVL.setText(str(self.StErr))

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QWidget()
    form = MainApp(window)
    app.exec_()

main()