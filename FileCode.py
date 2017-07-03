#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 09:41:09 2017

@author: Hobag
"""

#----------------Before Collection (When Start is pressed)--------------------#

#So within Start_fxn BEFORE self.graphTimer.start

Header = "Time (s)\t\tTotal Counts\t\tRate (counts/s)\n\n"
Handle = ""

def MakeTemp(tempDir):
    temp = open(tempDir, "w+")
    temp.write(Header)
    
#Directories have to be created in the first place even if the user doesn't end
#up saving any of their datasets.

#Long and short formats of the date, respectively.
DateL = datetime.date.today().isoformat()
DateS = DateL[2:3] + DateL[5:6] + DateL[8:9]

Folders = ["Data: ", DateL]
Temp = ["Temp", DateL]

saveDir = os.getcwd()
tempDir = os.getcwd()

"""
os.pathmjoin(path, *paths)

Join one or more path components intelligently. The return value is the
concatenation of path and any member of *paths with exactly one directory
separator following each non-empty part except the last, meaning that the
result will only end in a separator if the last part is empty. If a component
is an absolute path, all previous components are thrown away and joining
continues from the absolute path component.
"""

for folder in Folders:
    saveDir = os.path.join(saveDir, folder)
    tempDir = os.path.join(tempDir, folder)
if not(os.path.exists(saveDir)):
    osmakedirs(saveDir)

#----------------------------During Collection--------------------------------#

#So within Update()
DataString = (str(TimeValList[-1]) + "\t\t" +
              str(CountsList[-1]) + "\t\t" +
              str(CountsList[-1]/TimeValList[-1]) + "\n")
temp.write(DataString)
print("\nSuccessfully added new data!\n")
print(temp.read())

#-----------------------------After Collection--------------------------------#

#So within Stop_fxn

#Filename format (in folder "Data"): Data\yymmddCOUNT# NV#.txt
temp.close()
RunCount += 1
print("Here is your file: \n")
print(open(tempDir).read())

if (input("\nType y to save file, anything else \
              to leave: ").lower() == "y"):
    if RunCount == 0:       
        while os.path.isfile(saveDir) or Handle == "":
            Handle = input("\nEnter a name for your data files: ")
            if os.path.isfile(saveDir):
                print("\nThat filename is already in use.")
        FileName = DateS + "COUNT" + Handle
    else if RunCount >= 1:
        FileName = DateS + "COUNT" + Handle + "_" + RunCount
    saveDir = os.path.join(saveDir, FileName + ".txt")

"""
