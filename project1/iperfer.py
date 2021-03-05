#CLIENT
import time
import sys
import socket

#print to confirm command line arguments
print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))

#confirm correct amount of parameters
if (len(sys.argv) != 4):
    print("Error: missing or additional arguments")
    quit()

#parse command line arguments
server_hostname = sys.argv[1]
server_port = int(sys.argv[2])
timeSec = int(sys.argv[3])
start_time = time.time()
total_kb = 0

#confirm server port in parameters
if server_port < 1024 or server_port > 65535:
    print("Error: port number must be in the range 1024 to 65535\n")
    quit()

#main program body
while True:
    #keep track of time
    current_time = time.time()
    elapsed_time = current_time - start_time

    #sends the packet here
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((server_hostname, server_port))
        s.sendall(b'0')
        data = s.recv(1000)

    #keep track of kb sent
    total_kb = total_kb + 1

    #end of time
    if elapsed_time > timeSec:
        break

#print statistics
rate = (total_kb / 1000) / timeSec
print("sent=" + total_kb + " KB rate=" + rate + " Mbps")



