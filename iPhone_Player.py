# Records messages for a set number of seconds, then writes a file

import sys
import socket
import time
import struct
import random

fileName = sys.argv[1]
print("Playback of this file:", fileName)


randomSeshID = False
if len(sys.argv) > 2:
    if sys.argv[2] == "random":
        randomSeshID = True

MESSAGE = "23,567,32,4356,456,132,4353467" #init message

data = 0 #artificial data

UDP_IP = "127.0.0.1" #standard ip udp (localhost)
#UDP_IP = "132.145.38.38" #instance IP on cloud, load balancer in UK South
#UDP_IP = "132.145.30.140" #instance IP on cloud, load balancer in UK South
#UDP_IP = "129.153.176.88" #instance in ASBURN
#UDP_IP = "130.61.110.184" #standard ip udp (localhost)

UDP_PORT_1 = 20777   #chosen port to instance 

# Socket to Cloud instance listener - initiate socket and send first message
sockSession = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet, UDP
try:
    sockSession.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT_1))
except:
    print('Initial message failed!')


#Read file into memory
f = open(fileName, "rb")
data = f.read()
f.close()

lines = data.split(b'NEWLINE')
#print(data)
#print(len(lines))

keepGoing = True

#startTime = time.time()
#print("Start Time")

count = 1

while keepGoing:

    print("Starting: " + str(count) + " times through.")
    
    startTime = time.time()
    print("    using this start time: ", startTime)
    offsetTime = 0
    backDateTime = 0

    lineCount = 0
    
    for line in lines:
        
        lineCount = lineCount + 1
        
        

        # Check length
        #if len(line) < 24:
        #    print("Bad message, length: ", len(line))
        #    continue

        

        
       
            

        #print("Sending message:", struct.unpack('<b', line[5:6])[0], messageTimeStamp)
        newLine = line + ('\n').encode()
        
        #Send to IP and port
        sockSession.sendto(newLine, (UDP_IP, UDP_PORT_1))

        #Time the messages
        time.sleep(0.010)
    

        
    
    count = count + 1

