#Spencer Poisseroux
# ----- sender.py ------

#!/usr/bin/env python
from socket import *
import sys
from sys import getsizeof
import time
import struct

#print("first line")

host = sys.argv[1]
port = int(sys.argv[2])
total_kb = 0 #keep track for stats
buf = 512
addr = (host,port)
s = socket(AF_INET,SOCK_DGRAM)
end_time=0
seqNum = 42
conID = 0
payloadSize = 0
finished = False
#s.bind((host,port))

#start timer
global start_time
start_time = time.time()

def resend(packet):
    #resend lost packet
    global s
    global addr

    flag = ''
    sentSeqNum, sentAck, sentConID, sentFlag, sentPayload = struct.unpack('iihh512s', packet)
    if (sentFlag == 4):
        flag = "ACK"
    elif (sentFlag == 2):
        flag = "SYN"
    elif (sentFlag == 6):
        flag = "ACK SYN"
    elif (sentFlag == 1):
        flag = "FIN"
    elif (sentFlag == 5):
        flag = "ACK FIN"
    print("DROP " + str(sentSeqNum) + " " + str(sentAck) + " " + str(sentConID) + " " + flag)
    print("SEND " + str(sentSeqNum) + " " + str(sentAck) + " " + str(sentConID) + " " + flag + " DUP")

    s.sendto(packet,addr)
    receive(packet) #go to receive lost packet

def resendSYNACK(packet):
    global s
    global addr

    flag = ''
    sentSeqNum, sentAck, sentConID, sentFlag, sentPayload = struct.unpack('iihh512s', packet)
    if (sentFlag == 4):
        flag = "ACK"
    elif (sentFlag == 2):
        flag = "SYN"
    elif (sentFlag == 6):
        flag = "ACK SYN"
    elif (sentFlag == 1):
        flag = "FIN"
    elif (sentFlag == 5):
        flag = "ACK FIN"
    print("DROP " + str(sentSeqNum) + " " + str(sentAck) + " " + str(sentConID) + " " + flag)
    print("SEND " + str(sentSeqNum) + " " + str(sentAck) + " " + str(sentConID) + " " + flag + " DUP")

    s.sendto(packet,addr)
    receiveSYNACK(packet)

def receiveSYNACK(packet):
    global s
    global buf
    global host
    global port
    global addr
    global seqNum
    global conID

    try:
        s.settimeout(0.5)
        data, addr = s.recvfrom(buf)
        recvdSeqNum, recvdAck, conID, recvdFlag = struct.unpack('iihh', data)

        flag = ''
        if (recvdFlag == 4):
            flag = "ACK"
        elif (recvdFlag == 2):
            flag = "SYN"
        elif (recvdFlag == 6):
            flag = "ACK SYN"
        elif (recvdFlag == 1):
            flag = "FIN"
        elif (recvdFlag == 5):
            flag = "ACK FIN"
        print("RECV " + str(recvdSeqNum) + " " + str(recvdAck) + " " + str(conID) + " " + flag)

        if (recvdFlag != 6 or recvdAck != seqNum+1):
            resendSYNACK(packet)
    except timeout:
        resendSYNACK(packet)

def receive(packet, timer=0.5):
    global s
    global buf
    global host
    global port
    global addr
    global seqNum
    global conID
    global payloadSize
    global finished

    #print("in receive()")
    try:
        if (timer != 0.5):
            s.settimeout(timer)
        else:
            s.settimeout(timer)
        expectedSeqNum = seqNum
        data,addr = s.recvfrom(buf)
        # TODO split header + payload decoded
        recvdSeqNum, recvdAck, recvdConID, recvdFlag = struct.unpack('iihh', data)
        sentSeqNum, sentAck, sentConID, sentFlag, sentPayload = struct.unpack('iihh512s', packet)

        flag = ''
        if (recvdFlag == 4):
            flag = "ACK"
        elif (recvdFlag == 2):
            flag = "SYN"
        elif (recvdFlag == 6):
            flag = "ACK SYN"
        elif (recvdFlag == 1):
            flag = "FIN"
        elif (recvdFlag == 5):
            flag = "ACK FIN"
        print("RECV " + str(recvdSeqNum) + " " + str(recvdAck) + " " + str(recvdConID) + " " + flag)


        if (recvdFlag == 1):
            seqNum = expectedSeqNum
            return
        if (sentFlag == 5):
            seqNum = expectedSeqNum
            return
        if (sentFlag == 1):
            return
            #if ((recvdAck != expectedSeqNum) or recvdConID != conID) or (recvdFlag != 5):
            #    resend(packet)
            #seqNum = expectedSeqNum
            #return
        if (recvdFlag == 0 or recvdFlag == 4):
            expectedSeqNum = seqNum
        if (expectedSeqNum >= 204801): #after 204800 is zero
            expectedSeqNum = abs(204800 - expectedSeqNum)
        #check if received correct data (ACK)
        #print("receive if state (recvdSeq, seqNum, recvdAck, expected SeqNum)" + str(recvdSeqNum) + " " + str(seqNum) + " " +  str(recvdAck) + " " + str(expectedSeqNum))
        if ((recvdAck != expectedSeqNum)
            or (recvdConID != conID) or (recvdFlag != 4)):
            #print("if final\n)")
            resend(packet)
    except timeout: #ACK got lost
        if (timer == 0.5):
            resend(packet)
    seqNum = expectedSeqNum

def send(packet):
    global s
    global total_kb
    global host
    global port
    global buf
    global addr
    global seqNum

    flag = ''
    sentSeqNum, sentAck, sentConID, sentFlag, sentPayload = struct.unpack('iihh512s',packet)
    if (sentFlag == 4):
        flag = "ACK"
    elif (sentFlag == 2):
        flag = "SYN"
    elif (sentFlag == 6):
        flag = "ACK SYN"
    elif (sentFlag == 1):
        flag = "FIN"
    elif (sentFlag == 5):
        flag = "ACK FIN"
    print("SEND " + str(sentSeqNum) + " " + str(sentAck) + " " + str(sentConID) + " " + flag)

    s.sendto(packet,addr)
    total_kb += buf #track kb sent

def main():
    #get data, call send, recv after getting data in loop
    global buf
    global end_time
    global seqNum
    global payloadSize
    global finished

    #print("in getdata() init")

    completeHandshakePacket = handshake()
    receive(completeHandshakePacket)
    data = sys.stdin.read(buf)
    #print("got data")
    packet = buildStandardHeader(data)
    seqNum = seqNum + payloadSize
    #print(seqNum)

    try:
        while (data):
            #print("in getdata() while loop")
            s.settimeout(10)
            #seqNum = seqNum + 1
            send(packet) #send data
            receive(packet) #receive ack for sent data
            #seqNum = seqNum + payloadSize
            if (seqNum >= 204800): #make sure seqnum never goes above 9
                seqNum = abs(204800 - seqNum) #TODO IS THIS RIGHT?
            data = sys.stdin.read(buf)
            packet = buildStandardHeader(data)
            seqNum = seqNum + payloadSize
        packet = buildFinHeader()
        send(packet)
        receive(packet)
        finTimerStart = time.time()
        finTimerDiff = time.time()
        while ((finTimerDiff - finTimerStart) <= 2):
            finTimerDiff = time.time()
            receive(packet, 2)
            packet = buildFinAckHeader()
            send(packet)
        # try w/ timeout 2
        # receive ack from server
        # receive fin's from server and ack em

    except timeout:
        s.close()
        sys.exit(1)
    s.close()
    sys.exit(0)

def printStats():
    #end timer

    elapsed_time = end_time - start_time

    #statistics
    if (elapsed_time == 0):
        elapsed_time = 0.001
    kbRate = (total_kb / 125) / elapsed_time
    kbRate = float("%0.2f" % (kbRate))
    elapsed_time = float("%0.3f" % (elapsed_time))

def buildStandardHeader(payload):
    global conID
    global seqNum
    global payloadSize

    payloadSize = len(payload)
    payload = payload.encode()
    header = struct.pack('iihh512s', seqNum, 0, conID, 0, payload)

    return header

def buildFirstHandshakeHeader():
    global seqNum
    emptyPayload = bytearray(512)
    header = struct.pack('iihh512s', seqNum, 0, 0, 2, emptyPayload)
    #print("FIRST HANDSHAKE HEADER")
    return header

def buildThirdHandshakeHeader(payload):
    global conID
    global seqNum
    global payloadSize

    #payload = bytes(payload, 'utf-8')

    payload = payload.encode()
    payloadSize = len(payload)
    header = struct.pack('iihh512s', seqNum, 0, conID, 4, payload)
    #print("THIRD HANDSHAKE HEADER")
    return header

def buildFinHeader():
    global conID
    global seqNum

    emptyPayload = bytearray(512)
    header = struct.pack('iihh512s', seqNum, 0, conID, 1, emptyPayload)
    #print("FIN HEADER")
    return header

def buildFinAckHeader():
    global conID
    global seqNum

    emptyPayload = bytearray(512)
    header = struct.pack('iihh512s', seqNum, seqNum + 1, conID, 5, emptyPayload)
    #TODO WHAT IS SEQNUM
    #print("FIN ACK HEADER")
    return header

def handshake():
    global seqNum
    initpacket = buildFirstHandshakeHeader()
    send(initpacket)
    #print("init" + str(seqNum))
    receiveSYNACK(initpacket)
    data = sys.stdin.read(buf)
    seqNum = seqNum + 1
    secondpacket = buildThirdHandshakeHeader(data)
    send(secondpacket)
    #print("init2" + str(seqNum) + " data " + str(data))
    seqNum = seqNum + payloadSize
    return secondpacket

main()
# ACTUALLY START W/ HANDSHAKE
