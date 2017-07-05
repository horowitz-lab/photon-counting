#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 14:13:50 2017

@author: fqiu
"""

import visa
import time
import os






fileName = "continuous_polling_0.2_s_intervals" + ".csv"
waitTime = 405
NPERIODS = 1000
TSET = "9e11;"




#1. GPIB

rm = visa.ResourceManager()
instList = rm.list_resources()
print(instList)

GPIBName = ''
for instr in instList:
    if instr.find('GPIB') == 0:
        GPIBName = instr

sr400 = rm.open_resource(GPIBName)
sr400.timeout = 1000


#setup directory
saveDir = os.getcwd()


#open file
file = open(fileName, "w+")

#tell the machine to start
sr400.write("cr")
sr400.write("np " + str(NPERIODS))
sr400.write("CP 2, " + TSET)
sr400.write("cs")



#get the data

data = []

for i in range(1, NPERIODS):
    time.sleep(0.2)
    data.append(sr400.query("XA"))
    print(data[-1])
    
for item in data:
    file.write(str(data) + ",")

file.close()







