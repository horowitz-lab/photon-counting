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
import datetime
import os

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
                          
                           #__Defining Variables__#
global temp



#This line formats the categories of the data for a text file.
Header = "Time (s),Total Counts,Rate (counts/s)\n\n"

Handle = ""         #Stores a name to use for saved files from current session
FileName = ""       #For the SAVED data file

#L = long, S = short
DateL = datetime.date.today().isoformat()      # = yyyy-mm-dd
DateS = DateL[2:3] + DateL[5:6] + DateL[8:9]   # = y[2:3]mmdd

TimeL = str(datetime.datetime.now().time())
TimeS = TimeL[0:8]

saveDir = DateL + "_" + TimeS + "_SavedData"  #The directory FileName goes in
os.makedirs(saveDir)
os.chdir(saveDir)

#This function is called by Update().
def AddData(time, count, rate):
    DataString = (str(time) + "," +
                  str(count) + "," +
                  str(rate) + "\n")
    #file = open(tempFileName, "w+")
    temp.write(DataString)
    print("\nSuccessfully added new data!\n")
    print(temp.readlines())  #FT
    #file.close()

#This function is called by Stop_fxn().

def FileSave(RunCount):             
    #read_op = open(tempFileName, "r")
    
    #readlines() is used rather than read() because it will read the entirety
    #of the file if no parameter is given to it, whereas read() would just read
    #the file starting at the end of the last operation on it (right after the
    #last character was written to it).
                                                               
    #FullData = read_op.readlines()
    temp.close()
    print("Here is your file: \n\n")
    print(open(tempFileName).read())
    
    #Done to ensure temp can be properly accessed and deleted now that it
    #isn't necessary anymore.
    print("\nYour file has been successfully saved!")

#----------------------------Establishing Variables---------------------------#

class MainApp(sr400_GUI.Ui_Form):
    #lists and variables
    TimeValList = [0]
    CountsList = [0]
    CountRateList = []
    
    TotalAvg = 0
    Samples = 0
    StDev = 0
    StErr = 0
    
    RunCount = 0      #Tallies number of measurement periods in current session
    
    #Counter parameters controlled by GUI
    TimeInt = 3
    NPERIODS = 0
    TSET = 0
    NPERInst = ''
    
    Bases = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    Exponents = ["0",] + Bases + ["10", "11"]
    
    currentTime = 0
    currentCount = 0
    
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        print('Check 2')
        
        #setup SR400 to do 1 super long count
        sr400.write('cp2, 9e11')
        
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
        FileSave(self.RunCount)
        
        #reset data variables
        self.TimeValList = [0]
        self.CountsList = [0]
        self.CountRateList = []
        
        #clear graphs
        self.cvtGraph.clear()
        self.rvtGraph.clear()
        
        
        
    def Start_fxn(self):
        """starts the data collection and sets a reference time"""
        #enable/disable buttons
        self.StopBtn.setEnabled(True)
        self.StartBtn.setEnabled(False)
        
        #start the counter and get the reference time
        sr400.write('cr; cs')
        self.startTime = time.clock()
        
        self.FileSetup()
        
        #starts the QTimer to start repeatedly emit its signal
        self.graphTimer.start(self.TimeInt * 1000)
    
    def FileSetup(self):
        TimeL = str(datetime.datetime.now().time())
        TimeS = TimeL[0:8]
        self.RunCount += 1
        print("Run #", self.RunCount)
        global tempFileName 
        tempFileName = (DateS + "_Data_" + TimeS + ".csv")
        global temp
        temp = open(tempFileName, "w+")
        temp.write(Header)
    
    def Update(self):
        """gets current count and updates instance variables"""
        #get and append most recent count, time data
        data = sr400.query("xa \r")
        currentTime = self.TimeValList[-1] + self.TimeInt
        currentCount = int(data)
        
        self.TimeValList.append(currentTime)
        self.CountsList.append(currentCount)
        
        
        print("counts and time list")
        print(self.CountsList)
        
        
        #add new countrate
        self.CountRateList.append((self.CountsList[-1] - self.CountsList[-2])/ 
                                  (self.TimeValList[-1] - self.TimeValList[-2]))
        print(self.CountRateList, '\n')
        
        
        self.Samples += 1
        self.TotalAvg = np.mean(self.CountsList)
        self.StDev = np.std(self.CountsList)
        self.StErr = self.StDev / np.sqrt(self.Samples)
        
        print("Starting to graph...")
        
        #graph counts vs time and count rate vs time: ignore first rate point
        self.cvtGraph.plot(self.TimeValList, self.CountsList,
                           pen = (1, 1), symbol = 'o')
        if len(self.CountRateList) > 1:
            self.rvtGraph.plot(self.TimeValList[2:], self.CountRateList[1:],
                               pen = (1, 1), symbol = 'o')
        

        
        self.TimeVL.setText(str(self.TimeValList[-1]))
        self.PhotonVL.setText(str(self.CountsList[-1] - self.CountsList[-2]))
        self.TotAvgVL.setText(str(self.TotalAvg))
        self.StDevVL.setText(str(self.StDev))
        self.StErrVL.setText(str(self.StErr))
        
        AddData(currentTime, currentCount, self.CountRateList[-1])

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QWidget()
    form = MainApp(window)
    app.exec_()

main()