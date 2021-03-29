# ----- receiver.py -----

#!/usr/bin/env python
#USE PORT 7000 to test

from socket import *
import sys, os
import select

host = "127.0.0.1" #hardcoded localhost
port = int(sys.argv[1])
s = socket(AF_INET,SOCK_DGRAM)
s.bind((host,port))

addr = (host,port)
buf=1024

data,addr = s.recvfrom(buf)
data = data.decode()
receivedSeqNum = data[:1] #received sequence ADD TO CIRCULAR QUEUE
data = data[1:] #organic data


try:
    while(data):
        sys.stdout.write(data)
        s.settimeout(2)
        data,addr = s.recvfrom(buf)
        data = data.decode()
        receivedSeqNum = data[:1] #received sequence ADD TO CIRCULAR QUEUE
        #SEND BACK PACKET IF IT MATCHES PACKET IN QUEUE OF SENDER IT CAN THEN SLIDE THE WINDOW
        data = data[1:] #organic data

except timeout:
    #sys.stdout.close()
    s.close()
    sys.stderr.write("File received, exiting.\n")
