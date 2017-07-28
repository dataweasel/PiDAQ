# #####################################################################################
# # getSensorSN.py  -  Temperature Sensor gathering script for Pi-DAQ                 #
# # Joe Kimbler (dataweasel@gmail.com)                                                #
# # Phantom Electronics                                                               #
# #####################################################################################
# # When called this script will return the serial number(s) for the sensor(s) that   #
# # are connected to the 1-Wire bus.  It simply returns the serial number of the      #
# # MAX31820 sensor(s), not the data from them.  This is primarily for labeling and   #
# # identification purposes.                                                          #
# #####################################################################################
# # Version 00.01.01                                                                  #
# # Copyright (c) 2015 by Joe Kimbler and Phantom Electronics                         #
# # ALL RIGHTS RESERVED                                                               #
# #####################################################################################

import os
import glob
import time
import sys
import datetime

#- Spin up the 1-Wire Sub-System (if its not already running)
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

#- Base location of where the devices will write their data
base_dir = '/sys/bus/w1/devices/'

print ""
print "Device serial numbers currently connected to the 1-Wire bus:"
print "============================================================"

intCount = 0

for name in glob.glob(base_dir + '28*'):
    intCount = intCount + 1
    #- Just return the actual sensor data starting with "28" and dump the rest of the name
    tmpName = name.rsplit('/', 1)[1]
    print "Device %s: %s" % (intCount, tmpName)
    
print ""
