# #####################################################################################
# # dumpdb.py   - Database conversion script for Pi-DAQ                               #
# # Joe Kimbler (dataweasel@gmail.com)                                                #
# # Phantom Electronics                                                               #
# #####################################################################################
# # When called this script will open the sensordata.db file and will output each     #
# # of the rows in the "daq" table to a comma-delimited (csv) file that can be read   #
# # into Excel or other tool for analysis.                                            #
# #####################################################################################
# # Version 00.01.03                                                                  #
# # Copyright (c) 2015 by Joe Kimbler and Phantom Electronics                         #
# # ALL RIGHTS RESERVED                                                               #
# #####################################################################################
#
# Data arranged by DATETIME field, oldest first (ASC)
#

import sqlite3 as lite
import csv
import sys
from time import sleep

#- Get command line arguments
dbFile = str(sys.argv[1])

#- Connect to the database file 
con = lite.connect(dbFile)
#- Create an object for getting the individual sensor Serial Numbers
cur = con.cursor()
dat = con.cursor()

#- Get a list of the sensor serial numbers so we can create a file per sensor.
cur.execute("SELECT DISTINCT SensorID FROM daq ORDER BY SensorID ASC")
for sensID in cur.fetchall():
    tmpSensorID = sensID[0]
    tmpFileName = sensID[0] + ".csv"

    #- Get the data from the query (ASC = Oldest data first / DESC = Newest data first)
    sqlCmd = """SELECT * FROM daq WHERE SensorID = "{0}" ORDER BY datetime ASC"""
    data = dat.execute(sqlCmd.format(tmpSensorID))

    #- Go through the dataset 1 row-at-a-time and write each line to the csv file for the sensor
    with open(tmpFileName, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(['DateTime', 'SensID', 'DAQVal'])   #- Write Header Row
        writer.writerows(data)                              #- Write each row of data

sleep(1)
#- Close the database connection
con.close()
