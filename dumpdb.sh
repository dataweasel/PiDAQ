#!/bin/bash

#- Get the name of the file to dump.
dumpFile=$1

#- Call the python script that will dump the database to CSV
python ./dumpdb.py $dumpFile


