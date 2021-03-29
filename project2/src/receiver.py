# ----- receiver.py -----

#!/usr/bin/env python
#USE PORT 7000 to test

from socket import *
import sys, os
import select

buf = 1024

class RUDP():
    def __init__(self, seqNum, data):
        self.seqNum = seqNum
        self.data = data

host = "127.0.0.1" #hardcoded localhost
port = int(sys.argv[1])
s = socket(AF_INET,SOCK_DGRAM)
s.bind((host,port))

addr = (host,port)

data,addr = s.recvfrom(buf)
pkt = data.decode()

try:
    while(data):
        sys.stdout.write(pkt.data)
        s.settimeout(2)
        data,addr = s.recvfrom(buf)
        pkt = data.decode()

except timeout:
    #sys.stdout.close()
    s.close()
    sys.stderr.write("File received, exiting.\n")
