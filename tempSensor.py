# #####################################################################################
# # tempSensor.py   -  Temperature Sensor gathering script for Pi-DAQ                 #
# # Joe Kimbler (dataweasel@gmail.com)                                                #
# # Phantom Electronics                                                               #
# #####################################################################################
# # When called this script will check for the existance of the sensordata.db file    #
# # and will create it if needed.  It will then instruct the 1-wire MAX31820 temp     #
# # sensors to send in the latest temp, parse the data, and write it to the db        #
# # file.  All activity is logged in the eventlog.txt file in the home directory of   #
# # the "pi" user.                                                                    #
# #####################################################################################
# # Version 00.01.05                                                                  #
# # Copyright (c) 2015 by Joe Kimbler and Phantom Electronics                         #
# # ALL RIGHTS RESERVED                                                               #
# #####################################################################################

import os
import glob
import time
import sqlite3 as lite
import sys
import datetime

#- Spin up the 1-Wire Sub-System (if its not already running)
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

#- Base location of where the devices will write their data
base_dir = '/sys/bus/w1/devices/'

def read_temp_raw():
#- Given: the path and file to open
#-  Task: will return the entire (raw) file contents for parsing
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
#- Given: a defined value in "device_file" for the path and file we want to parse
#-  Task: return the value of the temperature in C
#- Needs: "device_file" variable to have the path to the "w1_slave" file for each sensor
#- Needs: a return variable to store the parsed C temperature in
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
	lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
	temp_string = lines[1][equals_pos+2:]
	temp_c = float(temp_string) / 1000.0
	return temp_c

def log_write(tmpMsg):
#- Given: a message to write to the log file.
#-  Task: write the message to the log file with date and time
    with open("/home/pi/eventlog.txt", "a") as f:
        f.write("%s %s" % (datetime.datetime.now(), tmpMsg))

try:
    #- Connect to the sensor database file.  If it doesn't exist, it will be created
    con = lite.connect('/home/pi/raspberry-pi-daq/sensordata.db')
except:
    log_write("!! Error: Cannot open database file.\n")
    sys.exit(1)

with con:
    cur = con.cursor()
    #- If the main tables don't exist, create them in the new file.
    cur.execute("CREATE TABLE IF NOT EXISTS daq(DateTime DATETIME DEFAULT (datetime('now', 'localtime')), SensorID TEXT, DAQValue INT)")

    #- Write a log entry to show that the sensor poll has begun.
    log_write(":: Gathering sensor data...\n")

    try:
        #- Get an object of each of the directory paths beginning with "28"
        for name in glob.glob(base_dir + '28*'):
            #- Take the next path and append the path to the sensor data file
            device_file = name + '/w1_slave'
            #- Call the Python function with the "device_file" variable set to parse the temp data
            tmpTemp = read_temp()
            #- Just return the actual sensor data starting with "28" and dump the rest of the name
            tmpName = name.rsplit('/', 1)[1]
            print "Device: %s   -- %s" % (tmpName, tmpTemp)
            #- Write the latest sensor values to the DB
            strQuery = "INSERT INTO daq (SensorID, DAQValue) VALUES ('%s', '%s')" % (tmpName, tmpTemp)
            cur.execute(strQuery)
    except:
        #- There is an error.  Let's attempt to log it in the EVENTS table.
        log_write("!!  ERROR:   %s\n" % (sys.exc_info()[0]))
		
con.close()

			
