import argparse
import subprocess
from sys import argv
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import astropy
import astropy.time as at
import ugradio
import time
# program to capture data via digital sampling
# kyle miller, gpl-licensed
#




# functions used in the program
def capture(volt_range=0, divisor=1, dual_mode=False, nsamples=16000, nblocks=1, host='10.32.92.95', port=1340, verbose=False, file_name=None):
    '''caputures raw data from pico sampler'''
    # default voltage ranges from ugradio package
    # ugradio.pico.VOLT_RANGE = ['50mV', '100mV', '200mV', '500mV', '1V', '2V', '5V', '10V', '20V']
    voltages = ['50mV', '100mV', '200mV', '500mV', '1V', '2V', '5V', '10V', '20V']
    vrange = voltages[volt_range]
    
    div = divisor
    dual = dual_mode
    nsamp = nsamples
    nblock = nblocks
    host = host
    port = port
    verbose = verbose

    if file_name is None:
        file_name = str(get_time(unix=time.time())) + "jd"

    start = get_time()
    raw_data = ugradio.pico.capture_data(vrange, div, dual, nsamp, nblock, host, port, verbose)
    finish = get_time()
    print("data capture finished")
    print(f"data written to {file_name}")
    tag_data(file_name, start, finish)
    np.savetxt(file_name, raw_data)
    


    
def tag_data(fname, start, finish):
    '''tags data with a text file containing time/data information'''
    # make file name
    fname = "tagfile-" + fname
    
    # get ip address and geolocation (lat and long)
    ip = subprocess.Popen(["curl",  "-s", "https://ipinfo.io/ip"], stdout=subprocess.PIPE)
    (ip_address, err) = ip.communicate()
    ip_address_text = ip_address.decode("utf-8")
    lookup = f"http://api.geoiplookup.net/?query={ip_address_text}"
    loc = subprocess.Popen(["curl", "-s", lookup], stdout=subprocess.PIPE)
    (location_information, err) = loc.communicate()
    loc_info = location_information.decode("utf-8")
    
    
    with open(fname, 'w') as output:
        output.write(f"Notes for data samples in {fname}")
        output.write(f"Sampling was started at: {start}")
        output.write(f"Sampling was completed at: {finish}")
        output.write(f"Julian date of sample: {get_time(unix=start)}")
        output.write(f"ip address of computer sampling: {ip_address_text}")
        output.write(f"Location Information:")
        output.write(loc_info)
    print("tag file written to {fname}")
    

def average_data():
    '''averages data into a single average file'''

def transform():
    '''transforms coordinates'''
    # need rotation matrix

def get_time(jd=None, unix=None):
   '''Return (current) time, in seconds since the Epoch (00:00:00 
    Coordinated Universal Time (UTC), Thursday, 1 January 1970).
    Note: unix time will be upgraded soon from 32bit to 64bit.
    This is the default.

    If jd is entered, unix time will be returned.
    If unix is entered, jd will be returned.
   
    Parameters
    ----------
    jd : float, julian date, default=None (i.e., now)
    unix : float, unix time

    Returns
    -------
    time : float, seconds since the Epoch or jd of unix time'''

   if jd is None:
       t = time.time()
       return t
    
   elif unix is None:
       t = at.Time(jd, format='jd')
       return t.unix
    
   else:
       t = at.Time(unix, format='unix')
       return t.jd

   
# main program implemented as boiler plate logic
if __name__ == "__main__":
   from sys import argv
   import sys
   import subprocess
   import re
   import argparse
   import pprint
   import numpy as np
   import scipy as sp
   import ugradio
   import astropy
   import matplotlib.pyplot as plt
   import traceback

   # argparse stuff
   parser = argparse.ArgumentParser(description='program to capture data via digital sampling')
   parser.add_argument('-v', "--verbose", action="store_true", help="displays numerical quantities to high precision")
   parser.add_argument('-lat', "--lat", action="store_true", help="takes in latitude")
   parser.add_argument('-long', "--long", action="store_true", help="takes in longitude")
   parser.add_argument('-c', "--capture", action="store_true", help="captures data")
   parser.add_argument('-nsamples', "--nsamples", action="store_true", help="sets the number of blocks to take")
   parser.add_argument('-t', "--time", action="store_true", help="prints out the current time in various ways")
   args = parser.parse_args()

   '''print time if toggled'''
   if args.time:
      print(f"The current unix time is: {get_time()}")
      


   '''capture data if toggled'''
   if args.capture:
       
       try:
           capture()
           
       except Exception:
           print("[[AN ERROR OCCURED]]")
           traceback.print_exc()
           sys.exit(1)

