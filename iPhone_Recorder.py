# Saves messages in a buffer until a set number of messages, then appends to a file.
# Also has a timeout set to write remaining messages in the buffer.

import sys
import socket
import time
import struct
from threading import Thread
from queue import Queue
#import subprocess
from datetime import datetime




# Dedicated file writing task
def file_writer(fileName, queue):
    # open the file
    with open(fileName, 'ab') as file:
        # run until the event is set
        while True:
            # get a line of text from the queue
            line = queue.get()
            # check if we are done
            if line is None:
                # exit the loop
                break
            # write it to file
            file.write(line)
            file.write("NEWLINE".encode('utf-8'))
            # flush the buffer
            file.flush()
            # mark the unit of work complete
            queue.task_done()
    # mark the exit signal as processed, after the file was closed
    queue.task_done()
 
# Task for worker threads
def task(number, queue, messageBuffer):
    # task loop
    #size= struct.unpack('<i', messageBuffer[number][0:4])
    #print("Task number", number)
    #queue.put(f'Thread {number} got {size}.\n')
    queue.put(messageBuffer[number])
    #for i in range(1000):
    #    # generate random number between 0 and 1
    #    value = random()
    #    # put the result in the queue
    #    queue.put(f'Thread {number} got {value}.\n')


# Write the messageBuffer to file on separate threads
def flushBufferToFile(messageBuffer,fileName):
    print("Flushing buffer to file at:" + str(datetime.now()))
    startingTime = time.time()
    #print(len(messageBuffer))
    # Create the shared queue
    queue = Queue()

    # Create and start the file writer thread
    writer_thread = Thread(target=file_writer, args=(fileName,queue), daemon=True)
    writer_thread.start()

    ## Configure worker threads, 1 for each message in the buffer
    threads = [Thread(target=task, args=(i,queue, messageBuffer)) for i in range(len(messageBuffer))]

    # Start Threads
    for thread in threads:
        thread.start()
    # Wait for threads to finish
    for thread in threads:
        thread.join()
    # Signal the file writer thread that we are done
    queue.put(None)
    # Wait for all tasks in the queue to be processed
    queue.join()
    endingTime = time.time()
    print("Time to write file:" + str(f'{(endingTime - startingTime):.3f}'))

def buildFilePath(withSessionID, sessionID):
    filepath = "iPhone_Output_"
    filepath = filepath + str(datetime.now().year) + "-"
    filepath = filepath + str(datetime.now().month) + "-"
    filepath = filepath + str(datetime.now().day) + "-"
    filepath = filepath + str(datetime.now().hour) + "-"
    filepath = filepath + str(datetime.now().minute) + "-"
    filepath = filepath + str(datetime.now().second)
    if withSessionID:
        filepath = filepath + "-" + str(sessionID)
    filepath = filepath + ".dat"

    return filepath



#for item in sys.argv:
#    pass

# Fake initial message
MESSAGE = "23,567,32,4356,456,132,4353467" #init message
data = 0 #artificial data

#Receiver socket from game UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.settimeout(15)
server_socket.bind(('', 20776))

messageBuffer = []
sessionID = None

# Build the shared filename (path) from time this recorder starts
filepath = buildFilePath(False, None)

print("iPhone_Recording to this file prefix: " + filepath)


keepGoing = True
bufferFlushSize = 1500 #messages
minFlushTime = 30 #seconds
timeOfLastFlush = time.time()

while keepGoing:
  
    message = None
    try:
        message, address = server_socket.recvfrom(1024000)
    except:
        print("Timeout: waiting for more data.", str(datetime.now()))


    # Just the message
    if message is not None:
        #print(message)
        messageBuffer.append(message)
    
    
    if len(messageBuffer) >= bufferFlushSize:
        bufferToFlush = messageBuffer
        flushBufferToFile(bufferToFlush, filepath)
        messageBuffer = []
        timeOfLastFlush = time.time()
    elif time.time() - timeOfLastFlush >= minFlushTime:
        if len(messageBuffer) > 0:
            bufferToFlush = messageBuffer
            flushBufferToFile(bufferToFlush, filepath)
            messageBuffer = []
            timeOfLastFlush = time.time()



