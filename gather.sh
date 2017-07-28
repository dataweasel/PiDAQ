#!/bin/bash

#- Add additional scripts below to have them scanned when
#- this script is called by CRON.

python /home/pi/raspberry-pi-daq/tempSensor.py   #- Call MAX31820 Temperature Probe scan
python /home/pi/raspberry-pi-daq/bdcstPiDAQ.py   #- Send out a broadcast to let the subnet know the PiDAQ is here


#-
#- This script would be called by CRON at the sampling rate required for
#- testing.  If additional scripts are needed to be sampled at a different
#- frequency, set up a seperate "gather1.sh" file and schedule your tasks
#- with that.