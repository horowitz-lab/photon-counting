#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 14:23:25 2017

@author: Houghton Yonge and Fuming Qiu
"""

#--------------------------------Library Imports------------------------------#

from PyQt5 import QtGui, QtWidgets
import sys
import sr400_GUI
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
ser = serial.Serial('COM#', 9600, serial.EIGHTBITS, seria.PARITY_EVEN, 
                    serial.STOPBITS_ONE, 2)
"""

#Counter parameters controlled by GUI
NPERIODS = 0
TSET = 0
NPERInst = ''
TSETInst = ''

DWELL = 2e-3

class MainApp(sr400_GUI.Ui_Form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        
        print('Check 2')
#----------------------GUI-Serial Connection Functions------------------------#

        def enc(self, str):
            return str.encode('ascii')
        
        def DataDump(self):
            ser.write(enc('ea \r'))
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
        
        """self.TSETBox.textChanged.connect(TSET_fxn)
        self.NPERSlider.valueChanged.connect(NPERSet)
        self.StartBtn.clicked.connect(Start_fxn)
        self.StopBtn.clicked.connect(Stop_fxn)"""
        
        def TSET_fxn(self):
            print('Oliver is too boojee to know what FAFSA is')
            """
            TSETText = TSETBox.toPlainText()
            TSET = int(TSETText)
            TSETInst = 'cp2, ' + TSETText + '; '
            """
            
        def NPERSet(self):
            print('Harry Thomas is a weebo')
            """
            NPERIODS = NPERSlider.value()
            NPERInst = 'np' + str(NPERIODS) + '; '
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

        self.TSETBox.textChanged.connect(TSET_fxn)
        self.NPERSlider.valueChanged.connect(NPERSet)
        self.StartBtn.clicked.connect(Start_fxn)
        self.StopBtn.clicked.connect(Stop_fxn)



def main():
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QWidget()
    form = MainApp(window)
    
    form.showWidgets()
    
    print(type(MainApp))
    sys.exit(app.exec_())

main()    