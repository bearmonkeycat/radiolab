import argparse
from sys import argv
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import astropy
import astropy.time as at
import ugradio
# program to capture data via digital sampling
# kyle miller, gpl-licensed
#

# functions used in the program
def capture(volt_range, divisor=1, dual_mode=False, nsampes=16000, nblocks=1, host='10.32.92.95', port=1340, verbose=False, file_name=None):
    '''caputures raw data from pico sampler'''
    vrange = volt_range
    div = divisor
    dual = dual_mode
    nsamp = nsamples
    nblock = nblocks
    host = host
    port = port
    verbose = verbose

    if file_name is None:
        file_name = str(get_time(unix=time.time()))

    raw_data = ugradio.pico.capture_data(vrange, div, dual, nsamp, nblock, host, port, verbose)

    np.savetxt(raw_data, file_name)
    


    
def tag_data():
    '''tags data with a text file containing time/data information'''

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
        time = time.time()
        return time
    
    else if unix is None:
        time = at.Time(jd, format='jd')
        return time.unix
    
    else:
        time = at.Time(unix, format='unix')
        return time.jd

   
# main program implemented as boiler plate logic
if __name__ == "__main__":
   from sys import argv
   import subprocess
   import re
   import argparse
   import pprint
   import numpy as np
   import scipy as sp
   import ugradio
   import astropy
   import matplotlib.pyplot as plt

   # argparse stuff
   parser = argparse.ArgumentParser(description='program to capture data via digital sampling')
   parser.add_argument('-v', "--verbose", action="store_true", help="displays numerical quantities to high precision")
   parser.add_argument('-lat', "--lat", action="store_true", help="takes in latitude")
   parser.add_argument('-long', "--long", action="store_true", help="takes in longitude")
   parser.add_argument('-c', "--capture", action="store_true", help="captures data")
   parser.add_argument('-nsamples', "--nsamples", action="store_true", help="sets the number of blocks to take")
   parser.add_argument('-t', "--time", action="store_true", help="prints out the current time in various ways")
   args = parser.parse_args()

   if args.time:
      get_time()

      
   '''fetch network node hostname'''
   try:
      hostname = getInfo("/etc/hostname")
      print(f"hostname: {hostname}\n")

   except:
      pass

