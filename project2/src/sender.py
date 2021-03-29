# ----- sender.py ------

#For milestone one, we want sender to divide data from a file into
#multiple packets and transmit to receiver by UDP

#!/usr/bin/env python
from socket import *
import sys
from sys import getsizeof
import time

s = socket(AF_INET,SOCK_DGRAM)
host = sys.argv[1]
port = int(sys.argv[2])
buf = 1024
addr = (host,port)
total_kb = 0 #keep track for stats
seqNum = 0

#prepend int to read
data = sys.stdin.read(buf - getsizeof(str(seqNum))).encode()
packet = str(seqNum).encode() + data
seqNum += 1

#start timer
start_time = time.time()

while (data):
    if(s.sendto(packet,addr)):
        data = sys.stdin.read(buf - getsizeof(str(seqNum))).encode()
        packet = str(seqNum).encode() + data
        seqNum += 1
        if seqNum == 10: seqNum = 0
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
