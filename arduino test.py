# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 12:58:57 2019

@author: HorowitzLab
"""

import serial

arduino = serial.Serial('COM5', 9600)

def valve(List): 
    n = len(List)
    rate = List[n]
    
    
    if rate >= 1000:
        arduino.write(b'1')
    elif rate < 1000:  
        arduino.write(b'0')
  
    arduino.close()

