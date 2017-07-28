# #####################################################################################
# # bdcstPiDAQ.py - Pi-DAQ UDP packet broadcast                                      #
# # Joe Kimbler (dataweasel@gmail.com)                                                #
# # Phantom Electronics                                                               #
# #####################################################################################
# # When called this script will broadcast a UDP packet on Port 13131 with the        #
# # IP Address of the Pi.  This can be received by another program to know what IP    #
# # the Pi is on.                                                                     #
# #####################################################################################
# # Version 00.01.02                                                                  #
# # Copyright (c) 2015 by Joe Kimbler and Phantom Electronics                         #
# # ALL RIGHTS RESERVED                                                               #
# #####################################################################################
#
# UDP Port: 13131
#

#- Set the port to broadcast on.  All listeners will have to use this same port.
MYPORT = 13131     #- Port 13131 is "general use" port.  Officially Unassigned.

import sys
import time
import socket
import datetime

#- Create the socket as a UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#- Bind it to all interfaces
s.bind(('', 0))

#- We create a simple packet for the purposes of getting the host name and IP Address of
#- the host.  In this case...the PiDAQ.
tmpHost = socket.gethostname()            #- Get the host name
s.connect(('google.com', 0))              #- Create the simple packet
tmpIP = tmpHost+':'+s.getsockname()[0]    #- Append the IP address to the end of the host name

#- Set the final options to make the UDP packet a broadcast packet.
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

#- Send the broadcast packet to the entire subnet on the selected port.
s.sendto(tmpIP, ('<broadcast>', MYPORT))

#- The broadcast data should look something like:  PiDAQ001:192.168.20.140  (hostname:ipaddress)

with open("/home/pi/eventlog.txt", "a") as f:
        f.write("%s %s" % (datetime.datetime.now(), ' :: -- Broadcast Sent :'+tmpIP+'\n'))
