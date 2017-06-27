#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 14:23:25 2017

@author: Houghton Yonge and Fuming Qiu
"""

#--------------------------------Library Imports------------------------------#

from PyQt5 import QtWidgets
import sys
import SR400_GUI
import serial as ser

#-----------------------Establishing Global(?) Variables----------------------#
Time = 0
TotalAvg = 0
StDev = 0
StErr = 0

GroupTally = 0
GroupAvg = []
StopFlag = 0

print('Check 1')
"""
ser = serial.Serial('COM#', 9600, serial.EIGHTBITS, serial.PARITY_EVEN, 
                    serial.STOPBITS_ONE, 2)
"""

#Counter parameters controlled by GUI
NPERIODS = 0
TSET = 0
NPERInst = ''
TSETInst = ''

DWELL = 2e-3

class MainApp(SR400_GUI.Ui_Form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        print('Check 2')
        
        #button connections to functions
        self.NPERSlider.valueChanged.connect(self.NPERSet)
        self.StartBtn.clicked.connect(self.Start_fxn)
        self.StopBtn.clicked.connect(self.Stop_fxn)
        self.TSETBox.textChanged.connect(self.TSET_fxn)
#----------------------GUI-Serial Connection Functions------------------------#

    def enc(self, str):
        return str.encode('ascii')
        
    def DataDump(self):
        ser.write(self.enc('ea \r'))
        data = ser.read(1000)
        return data
        
    def BytesToList(self, BStr):
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
    
#--------------------------GUI Widget Functions-------------------------------#
            
    def NPERSet(self):
        print('Harry Thomas is a weebo')
        """
        NPERIODS = NPERSlider.value()
        NPERInst = 'np' + str(NPERIODS) + '; '
        """
        
    def TSET_fxn(self):
        print('Oliver is too boojee to know what FAFSA is')
        """
        TSETText = TSETBox.toPlainText()
        TSET = int(TSETText)
        TSETInst = 'cp2, ' + TSETText + '; '
        """
        
    def Stop_fxn(self):
        print('Stop Button works!')
        """
        StopFlag = 1
        GroupTally = 0
        ser.write(enc('cr \r'))
        StartBtn.setEnabled(True)
        """
    
    def Start_fxn(self):
        print('Start Button works!')
        
        #making start do new random graph data
        self.setData()
        self.Graph.plot(self._x, self._y, pen = None, symbol = 'o')
        """
        StartBtn.setEnabled(False)
        ser.write(enc(TSETInst 
                      + NPERInst 
                      + 'dt ' + DWELL + '; '
                      + 'cr; cs \r'))
        while StopFlag == 0:
            time.sleep(6)
            data = DataDump()
            dataList = BytesToList(data)
            GroupTally = GroupTally + 1
            Time = GroupTally * (NPERIODS * (TSET + DWELL))
            GroupAvg.append(np.mean(dataList))
            TotalAvg = np.mean(GroupAvg)
            StDev = np.std(GroupAvg)
            StErr = StDev/sqrt(GroupTally)
            Update()
            print(GroupAvg)
            
        def Update(self):
            self.TimeVL.setText(str(Time))
            self.PhotonVL.setText(str(GroupAvg[GroupTally]))
            self.TotAvgVL.setText(str(TotalAvg))
            self.StDevVL.setText(str(StDev))
            self.StErrVL.setText(str(StErr))
            """
        
    

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QWidget()
    form = MainApp(window)
    print(type(MainApp))
    sys.exit(app.exec_())

main()