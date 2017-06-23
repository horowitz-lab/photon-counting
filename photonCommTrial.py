# -*- coding: utf-8 -*-
"""
Fuming Qiu
06/22/2017
simple communcation with the photon counter through serial. sets counter times
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

#check com port. the last parameter is the timeout.
ser = serial.Serial('COM7', 9600, serial.EIGHTBITS, serial.PARITY_EVEN, 
                    serial.STOPBITS_ONE, 2)

#set count time, set num counts, set dwell time, reset counts, press start
ser.write(enc('cp2, 1e7; np5; dt 1e-1; cr; cs \r'))

#set a pause
time.sleep(6)

#ask to get data from A, stores in data variable, stops counting
ser.write(enc('ea \r'))
data = ser.read(1000) #set to some large value of bytes. rely on timeout to end

print(data)
print(type(data))

dataList = bytesToList(data)

print(dataList)
ser.close()