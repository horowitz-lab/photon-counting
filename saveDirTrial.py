# -*- coding: utf-8 -*-
"""
Fuming Qiu
save to directory program
"""

import os

folders = ["data", "20170626"]

"""
#relative path option: will most likely use absolute path option
#saveDir = os.getcwd()
"""

saveDir = "C:\\Users\\HorowitzLab\\Documents"

#make new directory if not exist
for folder in folders:
    saveDir = os.path.join(saveDir, folder)
if not(os.path.exists(saveDir)):
    os.makedirs(saveDir)

fileName = input("filename?: ")
saveDir = os.path.join(saveDir, fileName + ".txt")

file = open(saveDir, "w+")
file.write("aw83refhs dvjkcn")
file.close()

#text overwrite protection