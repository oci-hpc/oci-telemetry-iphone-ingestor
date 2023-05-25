# Starts the Splitter and all the packet types on different threads (single type for iPhoneSensorLog)
# Records into a file if a "record" is given in the arguments list


import sys
from threading import Thread
import subprocess


record = False


for item in sys.argv:
    if item == "record":
        record = True

# Create threads
split = None
recorder = None

if record is True:
    split = Thread(target=subprocess.run, args=(["python3", "iPhone_Splitter.py", "record"],))
    
    recordArgs = ["python3", "iPhone_Recorder.py"]
    
    recorder = Thread(target=subprocess.run, args=(recordArgs,))
else:
    split = Thread(target=subprocess.run, args=(["python3", "iPhone_Splitter.py"],))


t00 = Thread(target=subprocess.run, args=(["python3", "iPhone_T00_SensorLog_Feed.py"],))


# Start threads
split.start()

if split is None:
    print("Splitter didn't start, exiting")
    exit()

if record:
    recorder.start()


t00.start()

# Join threads (wait till they are all finished, which is never)
#split.join()#
#recorder.join()
#t00.join()

