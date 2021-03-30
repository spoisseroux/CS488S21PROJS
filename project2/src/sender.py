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
port = 5008 #TODO:hardcoded port
total_kb = 0 #keep track for stats
buf = 1024
s = socket(AF_INET,SOCK_DGRAM)
s.bind((host,port))

#start timer
global start_time
start_time = time.time()

class CircularQueue():

    # constructor
    def __init__(self, size): # initializing the class
        self.size = size

        # initializing queue with none
        self.queue = [None for i in range(size)]
        self.front = self.rear = -1

    def isFull(self):
        # condition if queue is full
        if ((self.rear + 1) % self.size == self.front):
            return True
        else:
            return False

    def enqueue(self, data):

        # condition if queue is full
        if ((self.rear + 1) % self.size == self.front):
            print(" Queue is Full\n")
            #Full


        # condition for empty queue
        elif (self.front == -1):
            self.front = 0
            self.rear = 0
            self.queue[self.rear] = data
        else:

            # next position of rear
            self.rear = (self.rear + 1) % self.size
            self.queue[self.rear] = data

    def dequeue(self):
        if (self.front == -1): # codition for empty queue
            print ("Queue is Empty\n")

        # condition for only one element
        elif (self.front == self.rear):
            temp=self.queue[self.front]
            self.front = -1
            self.rear = -1
            return temp
        else:
            temp = self.queue[self.front]
            self.front = (self.front + 1) % self.size
            return temp

    def display(self):

        # condition for empty queue
        if(self.front == -1):
            print ("Queue is Empty")

        elif (self.rear >= self.front):
            print("Elements in the circular queue are:",
                                              end = " ")
            for i in range(self.front, self.rear + 1):
                print(self.queue[i], end = " ")
            print ()

        else:
            print ("Elements in Circular Queue are:",
                                           end = " ")
            for i in range(self.front, self.size):
                print(self.queue[i], end = " ")
            for i in range(0, self.rear + 1):
                print(self.queue[i], end = " ")
            print ()

        if ((self.rear + 1) % self.size == self.front):
            print("Queue is Full")#if full go to waitToRecv

    def getHead(self): #GET HEAD TO COMPARE
        if(self.front == -1):
            print ("Queue is Empty")
        else:
            for i in range(self.front, self.size):
                return (self.queue[0])

    def ack(self, num):
        if (self.rear >= self.front):
            for i in range(self.front, self.rear + 1):
                str = self.queue[i]
                if (num == str[:1]):
                    self.queue[i] = str[:1] + "ack" #get rid of rest of data on ack

        else:
            print("something went wrong with ack")

    def get(self, num):
        if (self.rear >= self.front):
            for i in range(self.front, self.rear + 1):
                str = self.queue[i]
                if (num == str[:1]):
                    return str #get data

        else:
            print("something went wrong with get")

    def isEmpty(self):
        if (self.front == -1): # codition for empty queue
            return True
        else:
            return False

q = CircularQueue(10)

def resendPacket():
    ## TODO: resend timeout packet
    #resend q.getHead()
    #after send start listening
    #finish and start fillQueue() again
    print("PACKET LOST \n")
    sys.exit(1)
    pass

def recvQueue():
    global q
    global s
    global buf
    #s = socket(AF_INET,SOCK_DGRAM)

    addr = (host,port)
    data,addr = s.recvfrom(buf)
    data = data.decode()
    receivedSeqNum = data[:1] #received seqNUM Ack in CIRCULAR QUEUE
    q.ack(receivedSeqNum)

    try:
        while(data):
            #TRY TO RECEIVE AND ACK ALL DATA
            #append 'ack' if ackd
            #check if data is head in queue
            s.settimeout(2)
            data,addr = s.recvfrom(buf)
            data = dataRecv.decode()
            receivedSeqNum = data[:1] #received sequence ADD TO CIRCULAR QUEUE
            q.ack(receivedSeqNum) #ACK RECEIVED PACKET
            #SEND BACK PACKET IF IT MATCHES PACKET IN QUEUE OF SENDER IT CAN THEN SLIDE THE WINDOW

    except timeout:

        print("IS IT ALL ACKED?\n")
        q.display()
        print()

        #this should empty whole queue if it is all acked
        for i in range(10):
            #check if head is acked, if so dequeue()
            head = str(q.getHead())
            if (head[1:4] == "ack"): #check if already acked
                q.dequeue()

        print("IS IT NOW EMPTY?\n")
        q.display()
        print()

        if (q.isEmpty):
            fillQueue():
        else:
            resendPacket():

def sendQueue():
    global total_kb
    global host
    global port
    global q
    global buf
    addr = (host,port)

    #send all packets from queue
    while (q.getHead() != None):
        for i in range(10):
            seqNum = str(i)
            packet = q.get(seqNum).encode()
            s.sendto(packet,addr)
            total_kb += buf

def fillQueue():
    seqNum = 0

    #populate queue 0-9
    for i in range(10):
        data = sys.stdin.read(buf - getsizeof(str(seqNum))).encode()
        packet = str(seqNum).encode() + data
        q.enqueue(packet.decode())
        seqNum = seqNum + 1

    sendQueue()






def showStats():
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

fillQueue()
