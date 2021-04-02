#Spencer Poisseroux
# ----- sender.py ------

#!/usr/bin/env python
from socket import *
import sys
from sys import getsizeof
import time

host = sys.argv[1]
port = int(sys.argv[2])
total_kb = 0 #keep track for stats
buf = 1024
addr = (host,port)
s = socket(AF_INET,SOCK_DGRAM)
end_time=0
#s.bind((host,port))

#start timer
global start_time
start_time = time.time()

def resend(packet):
    #resend lost packet
    global s
    global addr

    print("in resend()")
    s.sendto(packet,addr)
    receive(packet) #go to receive lost packet

def receive(packet):
    global s
    global buf
    global host
    global port
    global addr
    #s = socket(AF_INET,SOCK_DGRAM)

    print("in receive()")
    try:
        s.settimeout(1)
        if (data,addr = s.recvfrom(buf)):
            data = data.decode()
            receivedSeqNum = int(data[:1]) #received seqNUM Ack
            print("Received ack: " + str(receivedSeqNum))
            expectedSeqNum = int(packet.decode()[:1]) + 1
            if (expectedSeqNum == 10): #after 9 is zero
                expectedSeqNum = 0
                #check if received data (ACK)
            if (receivedSeqNum != expectedSeqNum): #Check for cumulative ack (incresed by 1)
                resend(packet)
        else:
            printStats() #end, no more packets?

    except timeout: #ACK got lost
        resend(packet)



def send(packet):
    global s
    global total_kb
    global host
    global port
    global buf
    global addr

    print("in send()")
    s.sendto(packet,addr)
    total_kb += buf #track kb sent


def getData():
    #get data, call send, recv after getting data in loop
    global buf
    global end_time

    #init data
    seqNum = 0
    data = sys.stdin.read(buf - getsizeof(str(seqNum))).encode()
    packet = str(seqNum).encode() + data
    seqNum = seqNum + 1

    try:
        while (data):
            s.settimeout(2)
            send(packet) #send data
            receive(packet) #receive ack for sent data
            seqNum = seqNum + 1
            if (seqNum == 10): #make sure seqnum never goes above 9
                seqNum = 0
            data = sys.stdin.read(buf - getsizeof(str(seqNum))).encode()
            packet = str(seqNum).encode() + data #prepend seq num to data

    except timeout:
        end_time = time.time()
        end_time = end_time - 2 #adjust for timeout
        pass

    end_time = time.time()
    s.close()
    printStats() #print stats when no more data, end


def printStats():
    #end timer

    elapsed_time = end_time - start_time

    #statistics
    if (elapsed_time == 0):
        elapsed_time = 0.001
    kbRate = (total_kb / 125) / elapsed_time
    kbRate = float("%0.2f" % (kbRate))
    elapsed_time = float("%0.3f" % (elapsed_time))
    print("Sent " + str(total_kb) + " bytes in " + str(elapsed_time) + " seconds: " + str(kbRate) + " kB/s")

getData()
