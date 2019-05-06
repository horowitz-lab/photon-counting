0#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 14:23:25 2017

@authors: Mikel Zemborain, Houghton Yonge and Fuming Qiu
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
import serial

#-------------------------------just a reminder-------------------------------#
print("")
print("")
print("####--------------------------------------------------------####")
print("     REMEMBER TO TURN ON SR400 AND CONNECT/POWER THE APD!!!")
print("####--------------------------------------------------------####")
#------------------------ Setting up Arduino Connectivity---------------------#
arduino = serial.Serial('COM5', 9600)
arduino.close()

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
Header = "Time (s), Total Counts, Rate (counts/s), \n\n"


#L = long, S = short
DateL = datetime.date.today().isoformat()      # = yyyy-mm-dd
DateS = DateL[2:3] + DateL[5:6] + DateL[8:9]   # = y[2:3]mmdd

TimeL = str(datetime.datetime.now().time())         
#this version of windows does not allow you to save a file with ":" in its title,
# so i had to replace all the colons with semi-colons.
TimeS = TimeL[0:2] + ";" + TimeL[3:5] + ";" + TimeL[6:8]


#This function is called by Update().                                          
def AddData(dataTimes, counts, rates):                                          
    """Given three lists of the same length, add all the data to data file"""
    for entry in range(len(dataTimes)):
        
        DataString = (str(dataTimes[entry]) + ",   " + str(counts[entry]) +
                      ",   " + str(rates[entry]) + "\n")                        
        # writes datastring into tempporary data file
        temp.write(DataString)                                                                        
    

#This function is called by Stop_fxn().
def FileSave(RunCount):        
    temp.close()
    print("Here is your file: \n\n")
    #reads the data just saved into our temporary data file
    data = open(tempFileName).read()
    print(data)
    #Done to ensure temp can be properly accessed and deleted now that it
    #isn't necessary anymore.
    print("\nYour file has been successfully saved!")


#----------------------------Establishing Variables---------------------------#
class MainApp(sr400_GUI.Ui_Form):
    
    
#lists and variables-:
    #the current time in secons
    curTimeVal = 0
    #list of all the count rates
    Ratelst= [] #
    #list of all the times where collection of data occurs
    Timelst=[]
    #list of all the counts
    Countlst = []
    #average rate
    average = 0
    #standard deviation of average rate
    StDev = 0
    #standard error of average rate
    StErr = 0
    #Counter parameters controlled by GUI
    TimeInt = 0
    #Tallies number of measurement periods in current session
    RunCount = 0   
    #the current period (1-2000), should be 0 when not counting.
    curPeriod= int(sr400.query("NN"))   
    print("new")
    print(curPeriod)\
    
    scrollWidth = 0 #the width of the x axis (in s) when graph scrolls
    scaleWidth = 20 #the width of the x axis (in s) when graph scales
    scrollCounter = 1   #keeps track of the window scroll number
    lag = 0 #the number of times lag has occured in a row
    
    #Threshold parameter controlled by GUI
    Threshold = 0 
    
    #sets dwell time, 
    sr400.write("DT 2E-3")
    #set number of periods (aka time bins)
    sr400.write("NP 2000")
    
    
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
    
        #button connections to functions
        self.StartBtn.clicked.connect(self.Start_fxn)
        self.StopBtn.clicked.connect(self.Stop_fxn)
        
        #enable/disable start and stop buttons
        self.StopBtn.setEnabled(False)
        self.StartBtn.setEnabled(True)
        
        #QTimer to update and call for data
        self.graphTimer = QTimer()
        self.graphTimer.setSingleShot(False)
        self.graphTimer.timeout.connect(self.Update)
        
        
    
#--------------Formatting Functions-------------------------------------------#
    def TSETtoFloat(self, text):
        #converts a string of the form NUMeNUM to an float
        return float(text)
    
    
#--------------------------GUI Widget Functions-------------------------------#
    def TSET_fxn(self):
        """gets the time value from the textbox and sets it as the sr400 time
           and sets an instance variable to hold that value"""
        #get value and assert it's in correct form
        TSETText = self.TSETBox.toPlainText()
        #this has to do with the syntax or the sr400 commands,1E7 = 1second
        TSET = str(self.TSETtoFloat(TSETText) * 10**7)
        #convert string to proper float and add dwell time
        self.TimeInt = self.TSETtoFloat(TSETText) + 0.002
        #set the width of the graph to be 50 times longer than the selected 
        #time bin time
        self.scrollWidth = ((self.TimeInt-.002)* 50)
        
        #set the sr400 to that time period
        sr400.write('CP2, ' + TSET)
    
    
    def valve(self, List): 
        #open serial comminucation with arduino if its not already open
        if(arduino.isOpen() == False):
            arduino.open()
        #find the current count rate value, assign it as rate    
        rate = List[-1]
        
        #get Threshold value and assert it's in correct form
        TSETText1 = self.TSETBox1.toPlainText()
        #convert string to proper float
        self.Threshold = self.TSETtoFloat(TSETText1)
       
        #if count rate is above the threshold, actuate valve.
        if rate >= self.Threshold:
            arduino.write(b'1')
        #if count rate is below the threshold, de-actuate valve.     
        elif rate < self.Threshold:  
            arduino.write(b'0')  
            
        
    def Stop_fxn(self):
        """stops the data collection, commands data to be saved, 
            closes serial communications"""
        #stop button gets dissablec after being clicked, start button gets enabled    
        self.StopBtn.setEnabled(False)
        self.StartBtn.setEnabled(True)
        #scale checkbox begs enabled
        self.checkBox1.setEnabled(True)
        #tells graphtimer to stop
        self.graphTimer.stop()
        #tells Photon counter to stop counting, reset data and tracking variables
        sr400.write('cr')
        #resets photon counter to factory settings 
        #(needed just in case a hardware issuephoton counter such as not 
        #turning on APD causes the SR400 to bug out)
        sr400.write('cl')
        
        #if you select to save the data, once you click the stop button,
        if self.checkBox.isChecked():
            #set up a folder in savedData to store our file in
            self.FileSetup()
            #add our data to a temporary file
            AddData(self.Timelst, self.Countlst, self.Ratelst)
            #save that temporary file
            FileSave(self.RunCount)
        #if you didnt select to save your data, say that    
        else:
            print("")
            print("you did not save your data")
            
        #reset the threshold limit
        self.Threshold = 0
        #close valve 
        arduino.write(b'0')
        #close serial communication
        arduino.close()
        
        #reset lists, so that old data is not stored in them during next measurement
        self.Ratelst = []
        self.Timelst = []
        self.Countlst = []
        
    def Start_fxn(self):
        """starts the data collection"""
        #reset data and tracking variables
        sr400.write('cr')
        
        self.TSET_fxn() 
        self.curTimeVal = 0
         
        #clear graph and reset window range. this depends on if your want to scale or scroll.
        self.rvtGraph.clear()
        if self.checkBox1.isChecked():
            self.rvtGraph.setXRange(0, self.scaleWidth)
        else: 
            self.rvtGraph.setXRange(0, int(self.scrollWidth))

        #reset data and tracking variables
        self.TSET_fxn() 
        self.curTimeVal = 0
        #self.curPeriod = 1
        self.scrollCounter = 1
        
        #enable/disable start and stop buttons
        self.StopBtn.setEnabled(True)
        self.StartBtn.setEnabled(False)
        #scale checkbox disabled
        self.checkBox1.setEnabled(False)
        
        #sets dwell time, 
        sr400.write("DT 2E-3")
        #set number of periods (aka time bins)
        sr400.write("NP 2000")
        #start counter        
        sr400.write("cs")
        #ask for the current period (1-2000) -> should = 1 here
        self.curPeriod= int(sr400.query("NN"))
        #When the number of time bins (Nperiods) reaches its maximum of 2000,
        #reset to 0 and continue measuring 
        sr400.write("NE 1")
        
        #starts the QTimer at timeInt, already includes 2ms dwell time
        self.graphTimer.start((self.TimeInt) * 1000)
    
    
    def FileSetup(self):
        """sets up files"""
        TimeL = str(datetime.datetime.now().time())
        #this version of windows does not allow you to save a file with ":" in its title,
        # so i had to replace all the colons with semi-colons.
        TimeS = TimeL[0:2] + ";" + TimeL[3:5] + ";" + TimeL[6:8]
        folder = DateL + "_" + TimeS + "_SavedData"  
        #The directory FileName goes in, look in SavedData folder in documents!
        saveDir = "C:/Users/HorowitzLab/Documents/SavedData/" + folder 
        os.makedirs(saveDir)
        os.chdir(saveDir)
        self.RunCount += 1
        global tempFileName 
        tempFileName = (DateS + "_Data_" + TimeS + ".csv")
        global temp
        temp = open(tempFileName, "w+")
        temp.write(Header)
    
    
    def Update(self):
        """gets current count and updates instance variables"""
        #create list holders for times and rates
        countVals = []
        timeVals = []
        rateVals = []
        
        
        #get data: continually ask for i-th point until not -1, add to list
        #poll for data until get -1
        
        #ask SR400 to give current Nperiod number
        self.curPeriod= int(sr400.query("NN"))
        print("new")
        print(self.curPeriod)
        #ask SR400 to give the photon count
        data = int(sr400.query("QA " + str(self.curPeriod))) 
        #print(data)
        while (data > -1):
           
            #add to list, update other vals
            countVals.append(data)
            self.curTimeVal += self.TimeInt
            self.curTimeVal = round(self.curTimeVal, 3)
            #print(self.curTimeVal)
            timeVals.append(self.curTimeVal)
            #print(timeVals)
            rateVals.append(round(data / (self.TimeInt-0.002), 1))
            print(data)
            print(rateVals)
            
            #at small time bins (> 0.2sec), the code will try to catch up to the measurements being taken
            # and produce a rateVals with multiple measurements, with only the last one being new data.
            #this if else loop ensures that this lag doesnt interfere with data collection
            if len(rateVals) > 1: 
                self.Ratelst.append(rateVals[-1])
                print("EXTRA!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print(timeVals)
                self.Countlst.append(countVals[-1])
                print(self.Ratelst)    
                self.Timelst.append(round(self.curTimeVal,3))
            else:  
                self.Ratelst.append(rateVals[0])
                self.Timelst.append(round(timeVals[0],3))
                self.Countlst.append(countVals[0])
            
            #calculates the avg, stdv, sterr and appends them to their respective lists 
            self.average = round(sum(self.Ratelst)/len(self.Ratelst), 1)
            self.StDev = round(np.std(self.Ratelst), 0)
            self.StErr = round( self.StDev / np.sqrt(len(self.Ratelst)), 0)

            #increase curPeriod, query for next data point
            self.curPeriod += 1
            data = int(sr400.query("QA " + str(self.curPeriod)))
            
        #shift window if enough time passes
        if self.checkBox1.isChecked():
            if (self.curTimeVal > self.scaleWidth * self.scrollCounter):
                self.scale()
        else:
            if (self.curTimeVal > self.scrollWidth * self.scrollCounter):
                self.scroll()
        
        
        #graph: x = time, y = rate, or photon count/period
        self.rvtGraph.plot(timeVals, rateVals, pen = None, symbol = '+')
        #put in all the values into their respected places in GUI
        self.TimeVL.setText(str(self.curTimeVal))
        self.CountRateVL.setText(str(rateVals[-1]))
        self.TotAvgVL.setText(str(self.average))
        self.StDevVL.setText(str(self.StDev) + "(1/s)")
        self.StErrVL.setText(str(self.StErr) + "(1/s)")
        self.valve(self.Ratelst)
        

    def scroll(self):
        """ scrolls the window, clearing old data off the graph. does not 
            experience lag. (lag mainly affects stoping measuring and starting
            a new measurement)"""
    
        self.rvtGraph.clear()
        self.rvtGraph.setXRange(self.scrollWidth * (self.scrollCounter), self.scrollWidth * (self.scrollCounter + 1))
        self.scrollCounter += 1
        
        
    def scale(self):
        """ scales the window to fit all the data. laggy when dealing with 
            large quantities of data, but good to see thigs slow phenomena
            such as photo-bleaching"""
        self.rvtGraph.setXRange(0, self.scaleWidth * (self.scrollCounter + 1))
        self.scrollCounter += 1     

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QWidget()
    form = MainApp(window)
    app.exec_()

main()