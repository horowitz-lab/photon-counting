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
import visa
import time

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

#----------------------------Establishing Variables---------------------------#

class MainApp(sr400_GUI.Ui_Form):

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
        super(self.__class__, self).__init__(parent)
        print('Check 2')
        
        sr400.write('DT ' + (str(self.DWELL)) + '; ' + 'cp2, 1e7')
        
        #button connections to functions
        self.NPERSlider.valueChanged.connect(self.NPERSet)
        self.StartBtn.clicked.connect(self.Start_fxn)
        self.StopBtn.clicked.connect(self.Stop_fxn)
        
#------------------------GUI-GPIB Connection Functions------------------------#

    def DataDump(self):
        """asks the sr400 for data and reads and returns what is sent"""
        #sr400.write('ea \r')
        #data = sr400.read(1000)
        data = sr400.query("ea \r")
        print(data)
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
        """converts a string of the form NUMeNUM to an int"""
        return int(text[0]) * 10 ** int(text[2:])
    
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
        #self.StartBtn.setEnabled(True)
    
    def Start_fxn(self):
        self.StopBtn.setEnabled(True)
        print('Start Button works!')
        sr400.write('cs')
        time.sleep(6)
        
        Data = self.DataDump()
        print(Data)
        
        DataList = self.BytesToList(data)
        print("\nData: \n")
        print(DataList)
        
        
        """
        self.StartBtn.setEnabled(False)
        #ser.write(self.enc(self.TSET_fxn() + ' \r'))
        sr400.write(self.TSET_fxn() + str(self.DWELL) + '; cr; cs')
        while self.StopFlag == 0:
            time.sleep(6)
            data = self.DataDump()
            dataList = self.BytesToList(data)
            self.GroupTally += 1
            
            groupTime = self.NPERIODS * (self.TSET + self.DWELL)
            self.timeVal = self.GroupTally * groupTime
            self.GroupAvg.append(np.mean(dataList))
            self.TotalAvg = np.mean(self.GroupAvg)
            self.StDev = np.std(self.GroupAvg)
            self.StErr = self.StDev / np.sqrt(self.GroupTally)
            
            #graph newest vals and add values to timeList
            self.Graph.plot(self.timeVal, self.GroupAvg[-1] / groupTime, 
                            pen = None, symbol = 'o')
            self._timeList.append(self.timeVal)
            
            
            self.Update()
            print(self.GroupAvg)
            
    def Update(self):
        self.TimeVL.setText(str(self.timeVal))
        self.PhotonVL.setText(str(self.GroupAvg[self.GroupTally])) ########################################
        self.TotAvgVL.setText(str(self.TotalAvg))
        self.StDevVL.setText(str(self.StDev))
        self.StErrVL.setText(str(self.StErr))
"""
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QWidget()
    form = MainApp(window)
    app.exec_()

main()