# ----- sender.py ------

#For milestone one, we want sender to divide data from a file into
#multiple packets and transmit to receiver by UDP

#!/usr/bin/env python
from socket import *
import sys
import time

buf = 1024
seqNum = 0

class RUDP():
    def __init__(self, seqNum, data):
        self.seqNum = seqNum
        self.data = data

s = socket(AF_INET,SOCK_DGRAM)
host = sys.argv[1]
port = int(sys.argv[2])
addr = (host,port)
total_kb = 0 #needs dynamic size looki[]

pkt = RUDP(seqNum, sys.stdin.read(buf).encode()) #init pkt
seqNum += 1
#data = sys.stdin.read(buf).encode() #read in buf

#start timer
start_time = time.time()

while (pkt.data):
    if(s.sendto(pkt,addr)):
        pkt = RUDP(seqNum, sys.stdin.read(buf).encode())
        seqNum += 1
        #data = sys.stdin.read(buf).encode()
        total_kb += buf #track size

s.close()

#end timer
end_time = time.time()
elapsed_time = end_time - start_time

#statistics
if (elapsed_time == 0):
    elapsed_time = 0.001
kbRate = (total_kb / 125) / elapsed_time
kbRate = float("%0.2f" % (kbRate))
elapsed_time = float("%0.3f" % (elapsed_time))
print("Sent " + str(total_kb) + " bytes in " + str(elapsed_time) + " seconds: " + str(kbRate) + " kB/s")
