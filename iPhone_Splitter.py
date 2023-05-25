# Takes data from iPhone SensorLog and splits messages by message type found in header bit. Only 1 type right now
# Sends to other ports that read the messages.
# Listens on port from iPhone Sensor Log, UDP: UDP_PORT
# Sends all messages to the recorder port if "record" is in the arguments list

import socket
import time
import struct
import sys
from datetime import datetime



record = False

for item in sys.argv:
    if item == "record":
        record = True



# Sends data to these ports:
UDP_IP = "127.0.0.1" #standard ip udp (localhost)
UDP_PORT = 20777

UDP_PORT_RECORD = 20776 #Recorder

UDP_PORT_0  = 20778   #Type 0, SensorLog


MESSAGE = "23,567,32,4356,456,132,4353467" #init message

# Type R - initiate socket and send first message
sock_R = None
if record:
    
    sock_R = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet, UDP
    try:
        sock_R.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT_RECORD))
    except:
        print('Initial message failed -- Recorder')

# Type 0 - initiate socket and send first message
sock_0 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet, UDP
try:
    sock_0.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT_0))
except:
    print('Initial message failed!')



#Receiver socket from game UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.settimeout(15)
server_socket.bind(('', UDP_PORT))

count = 0

# Messages from SensorLog must be buffered as they come in separate messages.
buffer = ''


while True:

    message = None
    
    try:
        message, address = server_socket.recvfrom(1024000)
    except KeyboardInterrupt:
        print("User stopped: iPhone_Splitter.")
        exit()
    except:
        print("Timeout: Splitter waiting for more data from port:", UDP_PORT, str(datetime.now())) 
    #print(message)
    #server_socket.sendto(message, address)

    if message is not None:

        # Must gather up messages, split by newline '\n'
        messageStrings = message.decode("utf-8").split('\n',1)
        if len(messageStrings) == 2:
            buffer = buffer + messageStrings[0]
            remaining = messageStrings[1]
        
            # Send gathered up message
            sock_0.sendto(buffer.encode(), (UDP_IP, UDP_PORT_0))
            #print(buffer)
            #print("\n")
        
            if record:
                sock_R.sendto(buffer.encode(), (UDP_IP, UDP_PORT_RECORD))
        
        
            # Clear buffer to remaining portion
            buffer = remaining

        

            if count % 1000 == 0:
                print ("Total message count: " +  str(count))

            count = count + 1

    
        else:
            # gather message into buffer
            buffer = buffer + messageStrings[0]



    


