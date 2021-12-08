# Project 3: Confundo

**Project assigned for Computer Networks & the Internet**

**TEAM**

Spencer Poisseroux and Jack Bonnelycke

**Setup**
((Linux environment required))

* To begin using our TCP-like Transport Protocol over UDP, please clone this repository into wherever you would like it saved. 
* Open a terminal in the location you would like to receive the file, with the repository cloned.
* Copy the file you would like to send into the cloned repository's project3/src/.
* In the receiving terminal, run the following
  * python3 ./server.py 5000 > RECEIVED_FILE
* In the sending terminal, run the following
  * cat FILENAME | python3 ./client.py HOSTNAME-OR-IP 5000
* Compare the two with:
  * diff FILENAME RECEIVED_FILE

**Purpose**

* To provide a TCP-like transport protocol over UDP with reliable transfer, relevant headers, and connection establishment.

[**Design**](https://github.com/jbonnelycke/CS488S21PROJS/blob/main/project3/design/receiver.png)
