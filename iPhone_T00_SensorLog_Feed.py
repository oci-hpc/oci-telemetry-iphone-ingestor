# Data provider for the iPhone_T00_SensorLog implementation
# Receives data from iPhone_Splitter via UDP Port 20778 and splits it and sends data to an specified UDP port for the OpenMCT server.

import socket
import time
import struct
import json

# Listens to this port from the splitter
UDP_PORT_0 = 20778   #chosen port to Motion feed

UDP_IP = "127.0.0.1" #standard ip udp (localhost)
UDP_PORT =50022   #chosen port to OpenMCT (same as in telemetry server object)
MESSAGE = "23,567,32,4356,456,132,4353467" #init message


# Connects to OpenMCT server - initiate socket and send first message
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet, UDP
try:
    sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))
except:
    print('Initial message failed!')

#Receiver socket from splitter
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.settimeout(15)
server_socket.bind(('127.0.0.1', UDP_PORT_0))


count = 0

while True:

    message = None

    try:
        message, address = server_socket.recvfrom(1024000)
    except KeyboardInterrupt:
        print("User stopped: iPhone_T00_SensorLog.")
        exit()
    except:
        print("Timeout: iPhone_T00_SensorLog waiting for more data from port:", UDP_PORT_0) 

    if message is not None:
        messageDecoded = message.decode("utf-8").split(',')
    
        # Check message is correct length, per documentation
        if len(messageDecoded) != 82:
            continue

        #print(messageDecoded)
        #server_socket.sendto(message, address)

        #---Send the whole message at once---
        #Fake the timestamp for now, until we figure out how to offset properly
        timeStamp = time.time()
        
        # Full message send
        #MESSAGE = "{},{},{},{}".format(header + unpacked)
        MESSAGE = "{}".format(json.dumps(["packet_iPhoneSensorLog", messageDecoded, timeStamp]));
        #MESSAGE = str(header + unpacked)
        #print(MESSAGE)
        sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))

        count = count + 1
        if count % 1000 == 0:
            print("    Packet iPhoneSensorLog messages sent: " + str(count))

