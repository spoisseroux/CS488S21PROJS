# ----- sender.py ------

#For milestone one, we want sender to divide data from a file into
#multiple packets and transmit to receiver by UDP

#1 put ten packets in QUEUE
#2 send packets from queue
#3 wait to recv acks, resend if necessary
#4 repeat?

#TODO:implement timers for timeout in queue

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
s.bind((host,port))

#start timer
global start_time
start_time = time.time()

def receive(packet):
    global s
    global buf
    global host
    global port
    global addr
    #s = socket(AF_INET,SOCK_DGRAM)

    data,addr = s.recvfrom(buf)
    data = data.decode()
    receivedSeqNum = data[:1] #received seqNUM Ack

    #check if received data (ACK)
    if (int(receivedSeqNum) == int(packet.decode()[:1]) + 1): #Check for cumulative ack (incresed by 1)
        #continue (break?)
        pass
    else:
        #resend packet
        pass


def send(packet):
    global s
    global total_kb
    global host
    global port
    global buf
    global addr

    s.sendto(packet,addr)
    total_kb += buf #track kb sent


def getData():
    #get data, call send, recv after getting data in loop
    global buf

    #init data
    seqNum = 0
    data = sys.stdin.read(buf - getsizeof(str(seqNum))).encode()
    packet = str(seqNum).encode() + data
    seqNum = seqNum + 1

    while (data):
        send(packet) #send data
        receive(packet) #receive ack for sent data
        seqNum = seqNum + 1
        if (seqNum >= 10): #make sure seqnum never goes above 9
            seqNum = 0
        data = sys.stdin.read(buf - getsizeof(str(seqNum))).encode()
        packet = str(seqNum).encode() + data #prepend seq num to data

    s.close()
    printStats() #print stats when no more data, end


def printStats():
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

getData()
