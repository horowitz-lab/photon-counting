# -*- coding: utf-8 -*-
"""
Fuming Qiu
save to directory program
"""

import os
import datetime
counter = 1


def createFileName(date, count):
    """creates a filename in the format
       yyyy-mm-dd\function\count\description.txt where \ is used to denote
       separate sections that are not space separated"""
    return date + count

def saveData(path):
    """creates a file at the location given by path (includes name) and 
       saves the data there"""
    file = open(path, "w+")
    file.write("adfiuhawef")
    file.close()

#auto date entry
date = datetime.date.today().isoformat()
folders = ["data", date]

"""
#relative path option: will most likely use absolute path option
#saveDir = os.getcwd()
"""
saveDir = os.getcwd()
#saveDir = "C:\\Users\\HorowitzLab\\Documents"

#make new directory if not exist
for folder in folders:
    saveDir = os.path.join(saveDir, folder)
if not(os.path.exists(saveDir)):
    os.makedirs(saveDir)

fileName = input("filename?: ")
saveDir = os.path.join(saveDir, fileName + ".txt")

#if file already exists, let user know and then create new filename
while os.path.isfile(saveDir):
    print("heuhaefu that's already a file o.o")
    print("adding _new to the end of file name")
    saveDir = saveDir[:-4] + "_new" + saveDir[-4:]

saveData(saveDir)