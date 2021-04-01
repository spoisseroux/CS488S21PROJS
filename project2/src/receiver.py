# ----- receiver.py -----

#!/usr/bin/env python
#USE PORT 7000 to test

#1 fill queue with expected numbers
#2 receive packets from sender
#3

from socket import *
import sys, os
import select

host = "127.0.0.1" #hardcoded localhost
port = int(sys.argv[1])
s = socket(AF_INET,SOCK_DGRAM)
s.bind((host,port))
addr = (host,port)
buf=1024

def recieve(seqNum):
    global s
    global buf
    global addr

    data,addr = s.recvfrom(buf)
    data = data.decode()
    receivedSeqNum = data[:1] #received sequence ADD TO CIRCULAR QUEUE
    if (int(receivedSeqNum) == seqNum):
        pass
    else:
        #resend packet here?
        pass


def sendQueue(ackNum):
    global total_kb
    global host
    global port
    global buf
    global addr

    packet = ackNum.encode() #sending ack to sender
    s.sendto(packet,addr)


def main():
    try:
        while(True):
            s.settimeout(2)
            seqNum = 0
            recieve(seqNum)
            ackNum = seqNum + 1 #Num to send as cumulative ack
            if (ackNum == 10): ackNum = 0 #after 9 comes zero
            send(ackNum)
            seqNum = seqNum + 1 #increase next expected seqNum
            if (seqNum == 10): seqNum = 0 #after 9 comes zero

    except timeout:
        #end
        pass

main()
