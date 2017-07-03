# -*- coding: utf-8 -*-
"""
Fuming Qiu
save to directory program
"""

#os is for file-controlling commands
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

#Each of these variables is a folder name.
save = ["data_", date]
temp = ["temp_", date]

"""
#relative path option: will most likely use absolute path option
#saveDir = os.getcwd()
"""

#These obtain the current directory.
saveDir = os.getcwd()
tempDir = os.getcwd()
#saveDir = "C:\\Users\\HorowitzLab\\Documents"

#make new directory if not exist

#os.path.join makes your new folder with a specific location 
#(e.g. C:\\Place1\\Place2, etc.)

saveDir = os.path.join(saveDir, save)
tempDir = os.path.join(tempDir, temp)

"""
for folder in folders:
    saveDir = os.path.join(saveDir, folder)
    tempDir = os.path.join(tempDir, folder)
"""
if not(os.path.exists(saveDir)):
    os.makedirs(saveDir)

fileName = input("filename?: ")
saveDir = os.path.join(saveDir, fileName + ".txt")

#if file already exists, let user know and then create new filename

#.isfile is a logical corresponding whether your path (from join) ENDS in a 
#path.
while os.path.isfile(saveDir):
    print("heuhaefu that's already a file o.o")
    print("adding _new to the end of file name")
    saveDir = saveDir[:-4] + "_new" + saveDir[-4:]

saveData(saveDir)

#prompt for save data
print("here is the file: ")
print(open(saveDir).read())

if not(input("type y to save file, anything else \
              to delete: ").lower() == "y"):
    os.remove(saveDir)
 
    #