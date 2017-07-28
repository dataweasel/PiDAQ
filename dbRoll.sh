#!/bin/bash

#- This script is to be called by CRON daily just before midnight.  The script will
#- copy the current sensordata.db file to the DataStage directory, and delete the 
#- current sensordata.db in the DAQ.  This will cause the DAQ to create a new database
#- on the next run.  In the staging directory, the date will be appended to the file.

tmpDate=$(date +"%m%d%Y")
tmpName="/home/pi/DataStage/sensordata_$tmpDate.db"

cp /home/pi/raspberry-pi-daq/sensordata.db $tmpName

