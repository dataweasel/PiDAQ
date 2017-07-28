# #####################################################################################
# # PiDAQSerial.py  -  Serial port monitor/logger for PiDAQ unit                      #
# # Joe Kimbler (dataweasel@gmail.com)                                                #
# # Phantom Electronics                                                               #
# #####################################################################################
# # Designed to run as a background process (restartListener.sh) this script will     #
# # open the COM port and monitor for data coming in (from an Arduino or other)       #
# # microcontroller under test.  This way the unit under test can periodically send   #
# # current status and/or error codes to the PiDAQ to have them cataloged in the      #
# # DAQ database with the other data.
# #####################################################################################
# # Version 00.01.03                                                                  #
# # Copyright (c) 2015 by Joe Kimbler and Phantom Electronics                         #
# # ALL RIGHTS RESERVED                                                               #
# #####################################################################################

#!/usr/bin/env python
import sqlite3
from time import time, gmtime, strftime
import time
import serial
import struct

#- global variables
dbname = '/home/pi/raspberry-pi-daq/sensordata.db'       #- Default location of PiDAQ database
DEVICE = '/dev/ttyAMA0'                                  #- Raspberry Pi serial port to monitor 
BAUD = 9600												 #- Standard baud rate
ser = serial.Serial(DEVICE, BAUD)                        #- Port definition

#- Open the DB, create the SYSNOTE table (if needed), insert the note and close the database
def log_note(tmpNote):
    conn = sqlite3.connect(dbname)
    curs = conn.cursor()
    strQuery = "CREATE TABLE IF NOT EXISTS sysnote (DateTime DATETIME DEFAULT (datetime('now', 'localtime')), Note TEXT)"
    curs.execute(strQuery)
    conn.commit()
    strQuery = "INSERT INTO sysnote (Note) VALUES ('%s')" % (tmpNote)
    curs.execute(strQuery)
    conn.commit()
    conn.close()

def main():

    #- Endless loop - where the magic happens
    while 1:
        myNote = ser.readline()     #- RX'ed anything on the COM port?
        if (len(myNote) > 0):       #- Yes?  
            log_note(myNote)        #- Send it to the database log


if __name__ == "__main__":
    main()
	
#- myNote = strftime("%Y-%m-%d %H:%M:%S", gmtime())+'\t'+ser.readline()

# Device being monitored should send the string to put into the database.  The act of inserting it into the database will
# insert the DATE/TIME of the note into the DATETIME field.
