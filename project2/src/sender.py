# ----- sender.py ------

#For milestone one, we want sender to divide data from a file into
#multiple packets and transmit to receiver by UDP

#!/usr/bin/env python
from socket import *
import sys
import time

buf = 1024
seqLast = 0

class RUDP():
    seqNum = 0
    data = bytearray(buf)

    def make(self, data):
        self.data = data
        self.seqNum = seqLast
        seqLast+=1

s = socket(AF_INET,SOCK_DGRAM)
host = sys.argv[1]
port = int(sys.argv[2])
addr = (host,port)
total_kb = 0 #needs dynamic size looki[]

pkt = RUDP() #init pkt
pkt.make(sys.stdin.read(buf).encode())
#data = sys.stdin.read(buf).encode() #read in buf

#start timer
start_time = time.time()

while (pkt.data):
    if(s.sendto(bytes(pkt),addr)):
        pkt.make(sys.stdin.read(buf).encode())
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
