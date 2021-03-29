# ----- receiver.py -----

#!/usr/bin/env python
#USE PORT 7000 to test

from socket import *
import sys, os
import select

class RUDP():
    seqNum = 0
    data = bytearray(buf)

    def make(self, data):
        self.data = data
        self.seqNum = seqLast
        seqLast+=1

host = "127.0.0.1" #hardcoded localhost
port = int(sys.argv[1])
s = socket(AF_INET,SOCK_DGRAM)
s.bind((host,port))

addr = (host,port)
buf=1024

data,addr = s.recvfrom(buf)

try:
    while(data):
        sys.stdout.write(data.decode())
        s.settimeout(2)
        data,addr = s.recvfrom(buf)

except timeout:
    #sys.stdout.close()
    s.close()
    sys.stderr.write("File received, exiting.\n")
