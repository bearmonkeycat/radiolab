import numpy as np
from ugradio.hp_multi import HP_Multimeter
import time

duration = 3600*8 # seconds in hour*number of hours
dt = .25 # time between samples

start = time.time()
file_number = 1
hpm = HP_Multimeter()
hpm.start_recording(dt)
print("recording started")
now = time.time()
while((now - start) < duration):
    print("sleeping")
    time.sleep(3600) # write data out every hour
    print(f"hpm status: {hpm.get_recording_status()}")
    output = hpm.get_recording_data()
    filename = "data" + str(file_number)
    file_number += 1
    np.savez(filename, output)
    now = time.time()
    
hpm.end_recording()
print("recording finished")
finish = time.time()
print(f"total time was {finish - start}")
