#CLIENT AND SERVER
import time
import sys
import socket

def checkPort(port):
    #confirm server port in parameters
    if port <= 1024 or port >= 65535:
        print("Error: port number must be in the range 1024 to 65535")
        sys.exit(1)

def getIP():
    #get host ip
    try:
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
        #print("Hostname :  ",host_name)
        #print("IP : ",host_ip)
        return host_ip
    except:
        print("Error: unable to get Hostname and IP")
        sys.exit(1)

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
        s.sendall(b'0')
        data = s.recv(1000)

        #keep track of kb sent
        total_kb = total_kb + 1

        #end of time
        if elapsed_time > timeSec:
            break

    s.close()
    #print statistics
    rate = (total_kb / 1000) / timeSec
    rate = float("%0.3f" % (rate))
    print("sent=" + str(total_kb) + " KB rate=" + str(rate) + " Mbps")

def runServer():
    #parse server params
    listen_port = int(sys.argv[2])
    checkPort(listen_port)
    host_name = getIP()

    total_kb = 0

    #start server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host_name, listen_port))
    s.listen()
    conn, addr = s.accept()
    with conn:
        start_time = time.time()
        #print('Connected by', addr)
        while True:
            data = conn.recv(1000)
            total_kb = total_kb + 1
            if not data:
                break
            conn.sendall(data)
    end_time = time.time()
    total_time = start_time - end_time
    rate = (total_kb / 1000) / total_time
    rate = float("%0.3f" % (rate))
    print("received=" + str(total_kb) + " KB rate=" + str(rate) + " Mbps")

def start():

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
        runClient()

start()
