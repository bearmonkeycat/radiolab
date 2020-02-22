# program to capture data via digital sampling
# kyle miller, gpl-3.0-licensed
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
        file_name = str(get_time(unix=get_time())) + "jd"

    start = get_time()
    raw_data = ugradio.pico.capture_data(vrange, div, dual, nsamp, nblock, host, port, verbose)
    finish = get_time()
    print("data capture finished")
    tag_data(file_name, start, finish)
    np.savetxt(file_name, raw_data)
    print(f"data written to {file_name}")



    
def tag_data(fname, start, finish):
    '''Tags data capture with a text file containing time/data/location information'''
    # make output file name
    ofname = "tagfile-" + fname
    
    # get ip address
    ip = subprocess.Popen(["curl",  "-s", "https://ipinfo.io/ip"], stdout=subprocess.PIPE)
    (ip_address, err) = ip.communicate()
    ip_address_text = ip_address.decode("utf-8").rstrip()

    # get location information
    lookup = f"http://api.geoiplookup.net/?query={ip_address_text}"
    loc = subprocess.Popen(["curl", "-s", lookup], stdout=subprocess.PIPE)
    (location_information, err) = loc.communicate()
    loc_info = location_information.decode("utf-8")

    # parse latitude
    lat_find = re.search(r'\<latitude>[\s\S]*?<\/latitude>', loc_info)
    latitude = lat_find.group()
    lat = re.sub('<[^<]+>', "", latitude)

    # parse longitude
    long_find = re.search(r'\<longitude>[\s\S]*?<\/longitude>', loc_info)
    longitude = long_find.group()
    longi = re.sub('<[^<]+>', "", longitude)    

    # parse isp
    isp_find = re.search(r'\<isp>[\s\S]*?<\/isp>', loc_info)
    internet_service_provider = isp_find.group()
    isp = re.sub('<[^<]+>', "", internet_service_provider)

    # parse city
    city_find = re.search(r'\<city>[\s\S]*?<\/city>', loc_info)
    city = city_find.group()
    cty = re.sub('<[^<]+>', "", city)

    # parse country
    country_find = re.search(r'\<countryname>[\s\S]*?<\/countryname>', loc_info)
    country = country_find.group()
    ctry = re.sub('<[^<]+>', "", country)

    # convert lat long to astronical coordinates


    
    with open(ofname, 'w') as output:
        output.write(f"Notes for data samples in {fname}\n")
        output.write(f"Sampling was started at (unix): {start}\n")
        output.write(f"Sampling was completed at (unix): {finish}\n")
        output.write(f"Dat capture took: {finish - start} seconds\n")
        output.write(f"Julian date of sample: {get_time(unix=start)}\n")
        output.write(f"IP address of computer sampling: {ip_address_text}\n")
        output.write(f"ISP used for internet access: {isp}\n")
        output.write(f"Latitude: {lat}\n")
        output.write(f"Longitude: {longi}\n")
        output.write(f"Country: {ctry}\n")
        output.write(f"City: {cty}\n")
        output.write('\neof\n')
        
    print(f"tag file written to {fname}")
    

def average_data():
    '''averages data into a single average file'''
    # import average data code
    
def transform():
    '''transforms coordinates'''
    # need rotation matrix stuff

def get_time(jd=None, unix=None):
   '''Return (current) time, in seconds since the Epoch (00:00:00 
    Coordinated Universal Time (UTC), Thursday, 1 January 1970).
    Note: unix time will be upgraded soon from 32bit to 64bit.
    Unix time is the default output; however,

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
   import time

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
       # add multi-block data capabilities
       
       try:
           capture()
           
       except Exception:
           print("[[AN ERROR OCCURED]]")
           traceback.print_exc()
           sys.exit(1)

else:
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
   import time
