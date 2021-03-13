#IPERFER.PY
#SPENCER POISSEROUX, LAURIE DELINOIS, MARCUS WONG
import time
import sys
import socket
import fcntl
import struct


def checkPort(port):
    #confirm server port in parameters
    if port <= 1024 or port >= 65535:
        print("Error: port number must be in the range 1024 to 65535")
        sys.exit(1)
        

def getIP(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

def runClient():

    #parse command line arguments
    server_hostname = sys.argv[1]
    server_port = int(sys.argv[2])
    checkPort(server_port)
    timeSec = int(sys.argv[3])
    start_time = time.time()
    total_kb = 0

    #connect
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server_hostname, server_port))

    #main program body
    while True:
        #keep track of time
        current_time = time.time()
        elapsed_time = current_time - start_time

        #sends the packet here
        s.send(bytearray(1000))

        #keep track of kb sent
        total_kb = total_kb + 1

        #end of time
        if elapsed_time > timeSec:
            break

    s.close()
    #print statistics
    rate = (total_kb / 125) / timeSec
    rate = float("%0.3f" % (rate))
    print("sent=" + str(total_kb) + " KB rate=" + str(rate) + " Mbps")

def runServer():
    #parse server params
    listen_port = int(sys.argv[2])
    checkPort(listen_port)

    #host_name = '127.0.0.1' #localhost
    host_name = get_ip_address('eth0')  #dynamic ip get
    print("IP :  ",host_name) 

    total_kb = 0

    #start server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host_name, listen_port))
    s.listen(5) #was giving problem with no param for listen
    conn, addr = s.accept()
    with conn:
        start_time = time.time()
        #print('Connected by', addr)
        while True:
            data = conn.recv(1000)
            total_kb = total_kb + 1
            if not data:
                break
            #conn.sendall(data)
    end_time = time.time()
    total_time = start_time - end_time
    rate = (total_kb / 125) / total_time
    rate = float("%0.3f" % (rate))
    print("received=" + str(total_kb) + " KB rate=" + str(rate) + " Mbps")

def start():

    #debug
    #print to confirm command line arguments to debug
    #print('Number of arguments:', len(sys.argv), 'arguments.')
    #print('Argument List:', str(sys.argv))

    #confirm correct amount of parameters
    if (len(sys.argv) != 4) and (len(sys.argv) != 3):
        print("Error: missing or additional arguments")
        sys.exit(1)

    #run server mode
    if (len(sys.argv) == 3):
        if (sys.argv[1] == '-s'):
            runServer()
        else:
            print("Error: missing or additional arguments")
            sys.exit(1)

    #run client mode
    if (len(sys.argv) == 4):
        #TEST5 CORNER CASE
        if (sys.argv[1] == '-s'):
            print("Error: missing or additional arguments")
            sys.exit(1)
        else:
            runClient()

start()
