#!/bin/bash

#- This script calls the Python script to list all the 
#- 1-Wire devices currently connected to the 1-Wire
#- sub-system bus.

#- Reset the 1-Wire bus
modprobe w1-gpio
modprobe w1-therm

python /home/pi/raspberry-pi-daq/getSensorSN.py
