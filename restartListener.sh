#!/bin/bash

#- PiDAQ: Enable Pithon Serial Monitoring Script
#- =============================================
#- Kill any active script -- ANY Python script running
pgrep '^python*' | xargs kill

#- Restart the listener
/home/pi/raspberry-pi-daq/PiDAQSerial.py &

