#Spencer Poisseroux
# ----- receiver.py -----

from socket import *
import sys, os
import select

host = "10.0.0.1"
port = int(sys.argv[1])
s = socket(AF_INET,SOCK_DGRAM)
s.bind((host,port))
addr = (host,port)
buf=1024
seqNum = 0

def recieve():
    global s
    global buf
    global addr
    global seqNum

    sys.stderr.write("in receive()\n")
    data,addr = s.recvfrom(buf)
    data = data.decode()
    receivedSeqNum = data[:1] #received sequence ADD TO CIRCULAR QUEUE
    writeData = data[1:]
    if (int(receivedSeqNum) == seqNum):
        sys.stdout.write(writeData)
    elif ((int(receivedSeqNum) == (seqNum - 1)) or ((int(receivedSeqNum) == 9) and (seqNum == 0))):
        sys.stderr.write("in elif\n")
        sys.stderr.write("expected " + str(seqNum)+ ": got "+str(receivedSeqNum)+"\n")
        seqNum = seqNum - 1
        if (seqNum < 0): seqNum = 9 #before 0 comes 9
        #what if sender doesnt receive ack, itll send another
        #and seq num will increase?
        #resend packet here?
        pass
    else:
        sys.stderr.write("in else\n")
        sys.stderr.write("expected " + str(seqNum)+ ": got "+str(receivedSeqNum)+"\n")
        pass


def send(ackNum):
    global s
    global total_kb
    global host
    global port
    global buf
    global addr

    sys.stderr.write("in send()\n")
    packet = str(ackNum).encode() #sending ack to sender
    s.sendto(packet,addr)


def main():
    global seqNum #init seqnum
    try:
        while(True):
            s.settimeout(2)
            recieve()
            ackNum = seqNum + 1 #Num to send as cumulative ack
            if (ackNum == 10): ackNum = 0 #after 9 comes zero
            sys.stderr.write("Sending ack: "+ str(ackNum) + "\n") #TODO: debug
            send(ackNum)
            seqNum = seqNum + 1 #increase next expected seqNum
            if (seqNum == 10): seqNum = 0 #after 9 comes zero

    except timeout:
        #end
        s.close()
        sys.stderr.write("File received, exiting.\n")
        pass

main()
