#Spencer Poisseroux
# ----- receiver.py -----

from socket import *
import sys, os
import select
import struct
import random

host = "127.0.0.1"
port = int(sys.argv[1])
s = socket(AF_INET,SOCK_DGRAM)
s.bind((host,port))
addr = (host,port)
buf=524
seqNum = 42
conID = 0
payloadSize = 0
prevFlag = 0
recvdFlag = 0
prevSize = 1
prevSeq = 0
firstHandshakeResend = False

def recieve():
    global s
    global buf
    global addr
    global seqNum
    global conID
    global prevFlag
    global recvdFlag
    global prevSize
    global prevSeq
    global firstHandshakeResend

    data,addr = s.recvfrom(buf)
    prevFlag = recvdFlag
    recvdPayload = struct.unpack_from('512s', data, 12)[0]
    recvdPayload = recvdPayload.decode().rstrip('\x00')
    recvdSeqNum, recvdAck, recvdConID, recvdFlag, recvdPayloadNull = struct.unpack('iihh512s', data)

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
    recvPrint = "RECV " + str(recvdSeqNum) + " " + str(recvdAck) + " " + str(recvdConID) + " " + flag

    #recvdPayload = recvdPayload.decode()
    if (prevFlag == 1 and recvdFlag == 5):
        s.close()
        sys.exit(0)
    if (recvdFlag == 2): # first handshake
        if (firstHandshakeResend == True):
            sys.stderr.write("DROP " + str(recvdSeqNum) + " " + str(recvdAck) + " " + str(recvdConID) + flag + "\n")
            seqNum = seqNum - 1
            recvPrint = recvPrint + " DUP"
        conID = random.randint(1, 20)
        prevSize = 1
        firstHandshakeResend = True
    # TODO elif recvdFlag ==4 and prevFlag == 1
    sys.stderr.write(recvPrint + "\n")
    if (recvdFlag == 1):
        finning()
    elif ((recvdFlag == 4 or recvdFlag == 0) and (conID == recvdConID)):
        if (recvdSeqNum == seqNum):
            sys.stdout.write(recvdPayload)
        elif (recvdSeqNum == prevSeq):
            seqNum = prevSeq
            sys.stderr.write("DROP " + str(recvdSeqNum) + " " + str(recvdAck) + " " + str(recvdConID) + flag + "\n")
            # retransmission
        prevSize = len(recvdPayload)
    # elif recvdFlag == 1 TODO
    prevSeq = seqNum
    # TODO prevFlag = recvdFlag

def finning():
    global addr
    global prevFlag
    global recvdFlag

    packet = buildFinAckHeader()

    flag = ''
    sentSeqNum, sentAck, sentConID, sentFlag = struct.unpack('iihh', packet)
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
    sys.stderr.write("SEND " + str(sentSeqNum) + " " + str(sentAck) + " " + str(sentConID) + " " + flag + "\n")

    s.sendto(packet, addr)
    #recv all the stuff
    packet = buildFinHeader()

    flag = ''
    sentSeqNum, sentAck, sentConID, sentFlag = struct.unpack('iihh', packet)
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
    sys.stderr.write("SEND " + str(sentSeqNum) + " " + str(sentAck) + " " + str(sentConID) + " " + flag + "\n")

    s.sendto(packet,addr)
    recieve()

def buildFinHeader():
    global conID
    global seqNum

    header = struct.pack('iihh', seqNum, 0, conID, 1)

    return header

def buildFinAckHeader():
    global conID
    global seqNum

    ackNum = seqNum + prevSize
    header = struct.pack('iihh', seqNum, ackNum, conID, 5)
    return header

def send():
    global s
    global total_kb
    global host
    global port
    global buf
    global addr
    global recvdFlag
    global prevSize
    global conID
    global seqNum

    ackNum = seqNum + prevSize
    if (ackNum >= 204800): ackNum = abs(204800 - ackNum)

    #dummyPayload = bytearray(512)
    if (recvdFlag == 2):
        packet = struct.pack('iihh', seqNum, ackNum, conID, 6)
    elif (recvdFlag == 1): #final
        pass #TODO
        # define and send ack
        # packet = defined fin
    #elif recvdFlag == 4 and prev == 1 then return
    elif (recvdFlag == 0 or recvdFlag == 4):
        packet = struct.pack('iihh', seqNum, ackNum, conID, 4)

    flag = ''
    sentSeqNum, sentAck, sentConID, sentFlag = struct.unpack('iihh', packet)
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
    sys.stderr.write("SEND " + str(sentSeqNum) + " " + str(sentAck) + " " + str(sentConID) + " " + flag + "\n")

    s.sendto(packet,addr)

def main():
    global seqNum #init seqnum
    global prevSize

    try:
        while(True):
            s.settimeout(2)
            recieve()
            send()
            seqNum = seqNum + prevSize #increase next expected seqNum
            if (seqNum >= 204800): seqNum = abs(204800 - seqNum)

    except timeout:
        #end
        s.close()
        sys.stderr.write("File received, exiting.\n")
        pass

main()
