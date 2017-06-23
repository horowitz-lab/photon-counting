#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
inital pyvisa test for GPIB communcation
"""

import visa
import time

#encode string to ascii code
def enc(str):
    return str.encode('ascii')


#initialize the resource manager
rm = visa.ResourceManager()
instList = rm.list_resources()
gpibName = ''

#get the GPIB port, set up inst object. then set timeout to 1s
for instr in instList:
    if instr.find('GPIB') == 0:
        gpibName = instr
sr400 = rm.open_resource(gpibName)
sr400.timeout = 1000

#set count time, set num counts, set dwell time, reset counts, press start
sr400.write_raw(enc('cp2, 1e7; np5; dt 1e-1; cr; cs \r'))

#set a pause
time.sleep(6)

#ask for data
data = sr400.query_ascii_values('ea \r')
print('using query')
print(data)
print(type(data))



sr400.write_raw(enc('ea \r'))
data = sr400.read()
print('using read')
print(data)
print(type(data))