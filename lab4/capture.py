import numpy as np
from ugradio.hp_multi import HP_Multimeter
import time

duration = 3600*6.5 # seconds in hour*number of hours
dt = .01 # time between samples

start = time.time()
hpm = HP_Multimeter()
hpm.start_recording(dt)
print("recording started")
now = time.time()
while((now - start) < duration):
    print("sleeping")
    time.sleep(300) # write data out every five mins
    print(f"hpm status: {hpm.get_recording_status()}")
    output = hpm.get_recording_data()
    filename = "data"
    np.savez(filename, output)
    now = time.time()
    
hpm.end_recording()
print("recording finished")
finish = time.time()
print(f"total time was {finish - start}")
