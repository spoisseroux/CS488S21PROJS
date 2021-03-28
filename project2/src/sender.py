# ----- sender.py ------

#For milestone one, we want sender to divide data from a file into
#multiple packets and transmit to receiver by UDP

#!/usr/bin/env python
from socket import *
import sys
import time

def main():
    s = socket(AF_INET,SOCK_DGRAM)
    host = sys.argv[1]
    port = int(sys.argv[2])
    buf = 1024
    addr = (host,port)
    total_kb = 0

    f=open("HUGE_FILE.txt","rb") #hardcoded file name
    data = f.read(buf)

    #start timer
    start_time = time.time()

    while (data):
        if(s.sendto(data,addr)):
            #print("sending ...")
            data = f.read(buf)
            total_kb += 1024

    #end timer
    end_time = time.time()
    elapsed_time = end_time - start_time

    s.close()
    f.close()

    #statistics
    kbRate = (total_kb / 125) / elapsed_time
    kbRate = float("%0.3f" % (kbRate))
    elapsed_time = float("%0.3f" % (elapsed_time))
    print("Sent " + str(total_kb) + " bytes in " + str(elapsed_time) + " seconds: " + str(kbRate) + " kB/s")

main()
