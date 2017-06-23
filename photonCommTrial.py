# -*- coding: utf-8 -*-
"""
Fuming Qiu
06/22/2017
simple communication with the photon counter through serial. sets counter times
and reads data at the end
"""

import serial
import time


#encode helper 
def enc(str):
    return str.encode('ascii')

#takes a bytestring from SR400 converts to list of ints
def bytesToList(bStr):
    dList = []
    curVal = 0
    #iterate through the bytes, accumulating a value in curVal
    for b in bStr:
        #if carriage return, the number has ended
        if b == 13:
            dList.append(curVal)
            curVal = 0
        #else, take 10 times the current value, and add the next number
        #ascii - 48 is the numerical value
        else:
            curVal = curVal * 10 + b - 48
            
    return dList

#some variables
countTime = "1e7"
countTimeFloat = 1.0
numCounts = "5"
dwellTime = "1e-1"
dwellTimeFloat = 0.1


#ask for the com port and the filename, create file, write headers
comPort = input("Enter com port: ")
fileName = input("Enter filename: include .txt: ")
file = open(fileName, "w+")
file.write("Time\tCounts\n")

#the last parameter is the timeout.
ser = serial.Serial(comPort, 9600, serial.EIGHTBITS, serial.PARITY_EVEN, 
                    serial.STOPBITS_ONE, 2)

#set count time, set num counts, set dwell time, reset counts, press start
ser.write(enc('cp2, %s; np%s; dt %s; cr; cs \r' %(countTime, numCounts,
                                                  dwellTime)))

#set a pause
time.sleep(int(numCounts) + 1)

#ask to get data from A, stores in data variable, stops counting
ser.write(enc('ea \r'))
data = ser.read(1000) #set to some large value of bytes. rely on timeout to end

print(data)
print(type(data))

#formats data into a list
dataList = bytesToList(data)

for i in range(0, int(numCounts)):
    print("cur loop val ", i)
    file.write("%f" %(i * (dwellTimeFloat + countTimeFloat)) + "\t" + 
               str(dataList[i]) + "\n")

file.close()
print(dataList)
ser.close()