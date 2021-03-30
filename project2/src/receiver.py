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
port = 7000 #TODO: hardcoded port
s = socket(AF_INET,SOCK_DGRAM)
s.bind((host,port))
addr = (host,port)
buf=1024

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

def recvQueue():
    #ONLY RUN AFTER QUEUE IS EMPTY
    global q
    global s
    global buf
    global addr

    #Fill queue with expected numbers
    for i in range(10):
        q.enqueue(str(i))

    data,addr = s.recvfrom(buf)
    data = data.decode()
    receivedSeqNum = data[:1] #received sequence ADD TO CIRCULAR QUEUE
    q.ack(receivedSeqNum) #ack if expected in queue arrives

    try:
        while(data):
            sys.stdout.write(data[1:]) #write data without header
            s.settimeout(2)
            data,addr = s.recvfrom(buf)
            data = data.decode()
            receivedSeqNum = data[:1] #received sequence ADD TO CIRCULAR QUEUE
            q.ack(receivedSeqNum)
            #SEND BACK PACKET IF IT MATCHES PACKET IN QUEUE OF SENDER IT CAN THEN SLIDE THE WINDOW

    except timeout:
        print("IS IT ALL ACKED?\n")
        q.display()
        print()

        #NOW SEND ACKS
        sendQueue()

def sendQueue():
    global total_kb
    global host
    global port
    global q
    global buf
    addr = (host,port)

    #send all ACKd packets from queue
    for i in range(10):
        head = str(q.getHead())
        if (head[1:4] == "ack"): #check if acked
            packet = head.encode() #sending ack to sender
            s.sendto(packet,addr)
            q.dequeue()

    #not all were acked, packet lost
    if (q.isEmpty() == False):
        #LISTEN FOR RESENT PACKETS NOW
        #SENDER WILL TIMEOUT AND TRY TO SEND AGAIN
        recvRetransmit()

def recvRetransmit():
    sys.stderr.write("PACKET LOST \n")
    sys.exit(1)
    #TODO: recvRetrainsmit()
    #listen for retransmit
    #when recv'd ack in QUEUE
    #send the ack'd header and any after it again

recvQueue()
