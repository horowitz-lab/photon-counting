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
                          
                           #__Defining Variables__#

#This line formats the categories of the data for a text file.
Header = "Time (s)\t\tTotal Counts\t\tRate (counts/s)\n\n"

Handle = ""         #Stores a name to use for saved files from current session
FileName = ""       #For the SAVED data file
RunCount = 0        #Tallies number of measurement periods in current session

temp = None
#L = long, S = short
DateL = datetime.date.today().isoformat()
DateS = DateL[2:3] + DateL[5:6] + DateL[8:9]

#MAC PATH NAME
GitHub = "/Users/pguest/Documents/GitHub/photon-counting"

#WINDOWS PATH NAME
GitHub = "C:\\Users"

#These functions occur in Start_fxn before self.graphTimer.start.
#TESTED

def tempCreate():
    
    #These lines properly index data files in preparation for saving, and simi-
    #lar processes will be used later.
    if os.getcwd() != GitHub:
        os.chdir(GitHub)
    if RunCount == 0:
        tempFileName = DateS + "_Temp"
    else if RunCount >= 1:
        tempFileName = DateS + "_Temp" + "_" + RunCount
    temp = open(tempFileName, "w+")
    temp.write(Header)
    temp.close()

#Gets current directory (photon-counting in GitHub)
#TESTED

def dirSetup():
    temp = tempCreate()

    #Creates new folders
    saveDir = DateL+"Save_Data"
    if not(os.path.exists(saveDir)):
        os.makedirs(saveDir)
    os.chdir("Save_Data")

#This function occurs within Update().

def AddData(time, count, file):
    DataString = (str(time) + "\t\t" +
                  str(count) + "\t\t" +
                  str(count / time) + "\n")
    file.write(DataString)
    print("\nSuccessfully added new data!\n")
    print(file.read())  #FT


#This function occurs within Stop_fxn.

def FileSave(fileItem):              #fileItem being the temporary file
    read_op = open(fileItem, "r")
    
    #readlines() is used rather than read() because it will read the entirety
    #of the file if no parameter is given to it, whereas read() would just read
    #the file starting at the end of the last operation on it (right after the
    #last character was written to it).
    FullData = fileItem.readlines()  
    fileItem.close()
    RunCount += 1
    print("Here is your file: \n\n")
    print(FullData)
    
    if not (input("\nType y to save file, anything else \
                  to delete: ").lower() == "y"):
        os.remove(saveDir)
    else:
        if RunCount == 0:
            #So the first of these conditions will always be true when no data
            #files have been created by this program during its last usage, and
            #the second is a check for duplicate filenames that HAVE already 
            #been created.
            while Handle == "" or os.path.isfile(saveDir):
                Handle = input("\nEnter a name for your data files: ")
                if os.path.isfile(saveDir):
                    print("\nThat file name is already in use.")
            FileName = DateS + "COUNT" + Handle + ".txt"
        else if RunCount >= 1:
            #i.e. if files using this session's handle have already been
            #created, new files will index properly using that handle.
            FileName = DateS + "COUNT" + Handle + "_" + str(RunCount) + ".txt"
            
        #These lines copy all the data into what will be the permanently saved
        #data file.
        saveDir = os.path.join(saveDir, FileName)
        savedFile = open(FileName, "w+")
        savedFile.write(FullData)
        savedFile.close()
    
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
        
        FileSave(temp)
    
    def Start_fxn(self):
        self.StopBtn.setEnabled(True)
        print('Start Button works!')
        sr400.write('cr; cs')
        self.StartBtn.setEnabled(False)
        
        print("Where?")
        
        self.StartTime = time.clock()
        loopTime = time.clock()
        
        print("Current Time: ", loopTime)
        
        dirSetup()
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
        
        currentTime = TimeValList[-1]
        currentCount = CountsList[-1]
        
        self.TimeVL.setText(str(self.currentTime))
        self.PhotonVL.setText(str(self.currentCount))
        self.TotAvgVL.setText(str(self.TotalAvg))
        self.StDevVL.setText(str(self.StDev))
        self.StErrVL.setText(str(self.StErr))
        
        AddData(currentTime, currentCount, temp)

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QWidget()
    form = MainApp(window)
    app.exec_()

main()