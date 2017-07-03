#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 16:12:06 2017

@author: pguest
"""

import os

a = os.getcwd()
print(a)
testfile = open("TestFile.txt", "w+")
testfile.write("This is a test. A what? A test.")
testfile.close()

os.mkdir("TestDir")
os.chdir("TestDir")
b = os.getcwd()
print(b)


GitHub = "/Users/pguest/Documents/GitHub/photon-counting"
os.chdir(GitHub)
os.remove("TestFile.txt")

"""
#Directory Creation and Change Test
a = os.getcwd()
print(a)
os.mkdir("TestDir")
os.chdir("TestDir")
b = os.getcwd()
print(b)

#File writing test
a = os.getcwd()

Header = "Format\n"
temp = open("Text.txt", "w+")
temp.write(Header)
temp.close()

def AddData(num1, num2, TextFileName):
    DataString = (str(num1) + "\t\t" +
                  str(num2) + "\t\t" +
                  str(num1 / num2) + "\n")
    operation = open(TextFileName, "w+")
    for i in range(0, 5):
        operation.write(DataString)
    operation.close()
    
AddData(3, 5, "Text.txt")

op_2 = open("Text.txt", "r")
a = op_2.readlines()
print(a)
op_2.close()
"""