# ----- sender.py ------

#For milestone one, we want sender to divide data from a file into
#multiple packets and transmit to receiver by UDP

#!/usr/bin/env python
from socket import *
import sys
import time

# This is the CircularQueue class
class CircularQueue:

  # constructor for the class
  # taking input for the size of the Circular queue
  # from user
  def __init__(self, maxSize):
    self.queue = list()
    # user input value for maxSize
    self.maxSize = maxSize
    self.head = 0
    self.tail = 0

  # add element to the queue
  def enqueue(self, data):
    # if queue is full
    if self.size() == (self.maxSize - 1):
      return("Queue is full!")
    else:
      # add element to the queue
      self.queue.append(data)
      # increment the tail pointer
      self.tail = (self.tail+1) % self.maxSize
      return True

  # remove element from the queue
  def dequeue(self):
    # if queue is empty
    if self.size() == 0:
      return("Queue is empty!")
    else:
      # fetch data
      data = self.queue[self.head]
      # increment head
      self.head = (self.head+1) % self.maxSize
      return data

  # find the size of the queue
  def size(self):
    if self.tail >= self.head:
      qSize = self.tail - self.head
    else:
      qSize = self.maxSize - (self.head - self.tail)
    # return the size of the queue
    return qSize




def checkBuffer(q):
    if (q.size == 9):
        while (q.size == 9):
            waitToRecvACK()
        #retransmit
    else:
        pass

def main():
    s = socket(AF_INET,SOCK_DGRAM)
    host = sys.argv[1]
    port = int(sys.argv[2])
    buf = 1020 #-4 bytes for seqNum
    addr = (host,port)
    total_kb = 0
    q = CircularQueue(10)

    seqNum = 0
    q.enqueue(seqNum) #enqueue first packet
    data = sys.stdin.read(buf).encode() #file from cat command line and encode to byte obj
    toSend = str(seqNum).encode() + data
    seqNum += 1

def transmit():
    while (data):
        if(s.sendto(toSend,addr)):
            #print("sending ...")
            checkBuffer()
            q.enqueue(seqNum)
            data = sys.stdin.read(buf).encode()
            toSend = str(seqNum).encode() + data
            seqNum += 1
            total_kb += buf



def printStats():
    #end timer

    elapsed_time = end_time - start_time

    s.close()
    sys.stdin.close()

    #statistics
    if (elapsed_time == 0):
        elapsed_time = 0.001
    kbRate = (total_kb / 125) / elapsed_time
    kbRate = float("%0.2f" % (kbRate))
    elapsed_time = float("%0.3f" % (elapsed_time))
    print("Sent " + str(total_kb) + " bytes in " + str(elapsed_time) + " seconds: " + str(kbRate) + " kB/s")

main()
start_time = time.time()
transmit()
end_time = time.time()
printStats()
