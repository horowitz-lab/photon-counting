#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 14:23:25 2017

@author: Houghton Yonge and Fuming Qiu
"""

#--------------------------------Library Imports------------------------------#

from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer
import sys
import sr400_GUI
import visa
import datetime
import os
import numpy as np
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
Header = "Time (s),   Total Counts,   Rate (counts/period),   average rate,   StDev,   StErr\n\n"

Handle = ""         #Stores a name to use for saved files from current session
FileName = ""       #For the SAVED data file

#L = long, S = short
DateL = datetime.date.today().isoformat()      # = yyyy-mm-dd
DateS = DateL[2:3] + DateL[5:6] + DateL[8:9]   # = y[2:3]mmdd

TimeL = str(datetime.datetime.now().time())         ###################
TimeS = TimeL[0:2] + ";" + TimeL[3:5] + ";" + TimeL[6:8]

saveDir = DateL + "_" + TimeS + "_SavedData"  #The directory FileName goes in
os.makedirs(saveDir)
os.chdir(saveDir)


#This function is called by Update().
def AddData(dataTimes, counts, rates, avg, stdev, sterr):
    """Given three lists of the same length, add all the data to data file"""

    for entry in range(len(dataTimes)):
        DataString = (str(dataTimes[entry]) + ",   " + str(counts[entry]) +
                      ",   " + str(rates[entry])+",   " + str(avg) + ",   " + 
                      str(stdev) +  ",   " +  str(sterr) + "\n")
             
    temp.write(DataString)
  

#This function is called by Stop_fxn().
def FileSave(RunCount):             
    
    temp.close()
    print("Here is your file: \n\n")
    data = open(tempFileName).read()

    print(data)
    
    #Done to ensure temp can be properly accessed and deleted now that it
    #isn't necessary anymore.
    print("\nYour file has been successfully saved!")


#----------------------------Establishing Variables---------------------------#
class MainApp(sr400_GUI.Ui_Form):
    #lists and variables
    AS = ""
    curTimeVal = 0
    Ratelst= []
    average = 0
    StDev = 0
    StErr = 0
    
    RunCount = 0      #Tallies number of measurement periods in current session
    NPER = 2000     #the number of periods
    curPeriod = 1   #the current period (1-2000)
    scrollWidth = 20   #the width of the x axis (in s)
    scrollCounter = 1   #keeps track of the window scroll number
    
    #Counter parameters controlled by GUI
    TimeInt = 0
    
    
    #Bases = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    #Exponents = ["0",] + Bases + ["10", "11"]
    
    currentTime = 0
    currentCount = 0
    
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        
        #setup SR400 to do nperiods = 2000
        sr400.write('np 2000')
        
        #button connections to functions
        self.StartBtn.clicked.connect(self.Start_fxn)
        self.StopBtn.clicked.connect(self.Stop_fxn)
        
        self.StopBtn.setEnabled(False)
        self.StartBtn.setEnabled(True)
        
        #QTimer to update and call for data
        self.graphTimer = QTimer()
        self.graphTimer.setSingleShot(False)
        self.graphTimer.timeout.connect(self.Update)
    
#--------------Formatting Functions-------------------------------------------#
    def TSETtoFloat(self, text):
        #converts a string of the form NUMeNUM to an float
        return float(text) # * 10 ** int(text[2:]) / (1e7)
    
#--------------------------GUI Widget Functions-------------------------------#
    def TSET_fxn(self):
        """gets the time value from the textbox and sets it as the sr400 time
           and sets an instance variable to hold that value"""
           
        #get value and assert it's in correct form
        TSETText = self.TSETBox.toPlainText()

        #assert TSETText[0] in self.Bases, "Base must be a \
        #     non-zero number!"
        # assert TSETText[1] == "e", "Second character must be e for \
        #     base-exponent notation!"
        #assert TSETText[2] in self.Exponents, "Exponent must range \
           # from 0 to 11!"

        #convert string to proper float and add dwell time
        self.TimeInt = self.TSETtoFloat(TSETText) + 0.002
        
        #set the sr400 to that time period
        sr400.write('cp2, ' + TSETText)
        
        
    def Stop_fxn(self):
        
        self.StopBtn.setEnabled(False)
        self.StartBtn.setEnabled(True)
        
        sr400.write('cr')
        self.StartBtn.setEnabled(True)
        self.graphTimer.stop()
        FileSave(self.RunCount)
        
        
    def Start_fxn(self):
        """starts the data collection"""
        #reset data and tracking variables
        self.curTimeVal = 0
        self.curPeriod = 1
        self.scrollCounter = 1
        
        #clear graph and reset window range
        self.rvtGraph.clear()
        self.rvtGraph.setXRange(0, self.scrollWidth)
        
        #enable/disable buttons
        self.StopBtn.setEnabled(True)
        self.StartBtn.setEnabled(False)

        #sets the time interval through tset
        self.TSET_fxn()

        #sets dwell time, reset and start the counter
        sr400.write("DT 2E-3")
        sr400.write("cr")
        sr400.write("cs")
        
        self.FileSetup()
        
        #starts the QTimer at timeInt, already includes 2ms dwell time
        self.graphTimer.start(self.TimeInt * 1000)
    
    
    def FileSetup(self):
        TimeL = str(datetime.datetime.now().time())
        TimeS = TimeL[0:2] + ";" + TimeL[3:5] + ";" + TimeL[6:8]
        self.RunCount += 1
        global tempFileName 
        tempFileName = (DateS + "_Data_" + TimeS + ".csv")
        global temp
        temp = open(tempFileName, "w+")
        temp.write(Header)
    
    
    def Update(self):
        """gets current count and updates instance variables"""
        #create list holders for times and rates
        #get data: continually ask for i-th point until not -1, add to list
        countVals = []
        timeVals = []
        rateVals = []
 
        
        #poll for data until get -1
        data = int(sr400.query("QA " + str(self.curPeriod))) 
        while (data > -1):
            #add to list, update other vals
            countVals.append(data)
            self.curTimeVal += self.TimeInt
            self.curTimeVal = round(self.curTimeVal, 3)
            timeVals.append(self.curTimeVal)
            rateVals.append(round(data / self.TimeInt, 3)) 
            #increase curPeriod, query for next data point
            
            self.Ratelst.append(rateVals[0])
            self.average = round(sum(self.Ratelst)/self.curPeriod, 3)
            self.StDev = round(np.std(self.Ratelst), 3)
            self.StErr = round( self.StDev / np.sqrt(self.curPeriod), 3)
            #print(str(self.average) + ", " + str(self.StDev) + ", " + str(self.StErr))
            self.curPeriod += 1
            
            data = int(sr400.query("QA " + str(self.curPeriod)))
        
        #shift window if enought time passed
        if (self.curTimeVal > self.scrollCounter * self.scrollWidth):
            self.scroll()
        
        #graph: x = time, y = rate, or photon count/period
        self.rvtGraph.plot(timeVals, rateVals, pen = None, symbol = '+')
        #put in all the values into their respected places in GUI
        self.TimeVL.setText(str(self.curTimeVal))
        self.PhotonVL.setText(str(countVals[-1]))
        self.TotAvgVL.setText(str(self.average))
        self.StDevVL.setText(str(self.StDev))
        self.StErrVL.setText(str(self.StErr))

        AddData(timeVals, countVals, rateVals, self.average, self.StDev, self.StErr )
    
    
    def scroll(self):
        """clears, scrolls the window, leaving the last second still visible"""
        self.rvtGraph.setXRange(0, self.scrollWidth * (self.scrollCounter + 1))
        self.scrollCounter += 1

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QWidget()
    form = MainApp(window)
    app.exec_()

main()