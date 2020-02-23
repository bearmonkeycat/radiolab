#!/usr/bin/env python
""" Program to capture data via digital sampling

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
"""

__author__ = "kyle miller"
__copyright__ = "Copyright 2020, Kyle Miller"
__date__ = "2020/02/22"
__license__ = "GPLv3"
__status__ = "alpha"
__version__ = "0.0.1"


# functions used in the program
def capture(volt_range=0, divisor=1, dual_mode=False, nsamples=16000, nblocks=1, host='10.32.92.95', port=1340, verbose=False, file_name=None):
    '''Caputure raw data from pico sampler'''
    # parameters for data capture
    # default voltage ranges from ugradio package:: ugradio.pico.VOLT_RANGE
    voltages = ['50mV', '100mV', '200mV', '500mV', '1V', '2V', '5V', '10V', '20V']
    vrange = voltages[volt_range]
    #div = divisor
    div = 12
    #dual = dual_mode
    dual = True
    nsamp = nsamples
    nblock = nblocks
    host = host
    port = port
    verbose = verbose

    # parameters in list form
    parameters = [vrange, div, dual, nsamp, nblock, host, port, verbose]

    # logistics for storing data capture
    if file_name is None:
        file_name = str(get_time(unix=get_time())) + "jd"

    if args.directory:
        if os.path.isdir(args.directory):
            pass
        else:
            os.mkdir(args.directory)

    # capture data
    start = get_time()
    raw_data = ugradio.pico.capture_data(vrange, div, dual, nsamp, nblock, host, port, verbose)
    finish = get_time()
    print("data capture finished")
    tag_data(file_name, start, finish, parameters)
    if args.directory:
        path = "./" + args.directory + "/" + file_name
        np.savetxt(path, raw_data)
        print(f"data written to {path}")
    else:
        np.savetxt(file_name, raw_data)
        print(f"data written to {file_name}")



    
def tag_data(fname, start, finish, params):
    '''Tag data capture with a text file containing time/data/location information'''
    # make output file name
    ofname = "tagfile-" + fname

    if args.directory:
        ofname = "./" + args.directory + "/" + ofname

    # try to get internet information with curl
    iinfo=True
    try:
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

    except:
        iinfo = False
        print("[[ERROR GETTING INTERNET INFORMATION]]")
        
    # convert lat long to astronomical coordinates
    # location = location

    # list of parameter names for data capture
    parameters = ['vrange', 'div', 'dual', 'nsamp', 'nblock', 'host', 'port', 'verbose']
    with open(ofname, 'w') as output:
        output.write(f"\n[[METADATA FOR DATA SAMPLES IN {fname}]]\n")

        # write out internet metadata
        output.write(f"{get_date()}\n")
        output.write(f"{get_date(utc=True)}\n")
        output.write(f"Sampling was started at (unix): {start}\n")
        output.write(f"Sampling was completed at (unix): {finish}\n")
        output.write(f"Data capture took: {finish - start} seconds\n")
        output.write(f"Julian date of sample: {get_time(unix=start)}\n")
        if iinfo:
            output.write(f"IP address of computer sampling: {ip_address_text}\n")
            output.write(f"ISP used for internet access: {isp}\n")
            output.write(f"Latitude: {lat}\n")
            output.write(f"Longitude: {longi}\n")
            output.write(f"Country: {ctry}\n")
            output.write(f"City: {cty}\n\n")

        # write out parameters used
        output.write(f"[[PARAMETERS FROM DATA CAPTURE]]\n")
        for i in range(len(params)):
            output.write(f"{parameters[i]}: {params[i]}\n")

        # write out location information
        output.write(f"\n[[LOCATION INFORMATION]]\n")
        if args.lat:
            output.write(f"User input latitude: {args.lat}\n")
        if args.lon:
            output.write(f"User input longitude: {args.lon}\n")
        if args.azimuth:
            output.write(f"User input azimuth: {args.azimuth}\n")
        if args.altitude:
            output.write(f"User input altitude: {args.altitude}\n")
        if location is not None:
            output.write(f"Location was set to lat[{location.lat}] lon[{location.lon}]")

        # make room for lab notes
        output.write("\n\n[[LAB NOTES]]\n")
        output.write("Vpp: \n")
        output.write("First LO power: \n")
        output.write("Second LO power: \n")
        output.write("Low-pass filter: \n\n\n")
        output.write('\neof\n')

    # tag file written    
    print(f"tag file written to {ofname}")
    
    
def transform(latitude, longitude):
    '''Transform coordinates'''
    # need rotation matrix stuff
    c = SkyCoord(latitude, longitude, unit=u.deg)

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

def get_utc():
    utc = Time.now()
    return utc

def get_lst():
    lst = 0
    return lst

def get_date(utc=False):
    if utc:
        date = subprocess.Popen(["date",  "-u"], stdout=subprocess.PIPE)
        (date, err) = date.communicate()
        date_text = date.decode("utf-8").rstrip()
        return date_text
    else:
        date = subprocess.Popen(["date"], stdout=subprocess.PIPE)
        (date, err) = date.communicate()
        date_text = date.decode("utf-8").rstrip()
        return date_text

        
   
# main program implemented as boiler plate logic
if __name__ == "__main__":
   from sys import argv
   import sys
   import os
   import subprocess
   import re
   import argparse
   import pprint
   import numpy as np
   import scipy as sp
   import ugradio
   import astropy.time as at
   from astropy.coordinates import SkyCoord
   from astropy.coordinates import EarthLocation
   from astropy.coordinates import AltAz
   from astropy import units as u
   from astropy.time import Time
   import matplotlib.pyplot as plt
   import traceback
   import time

   # nch location
   nch = EarthLocation(lat="37.8732", lon="-122.2573", height=123.1*u.m)
   
   # argparse stuff
   parser = argparse.ArgumentParser(description='''Program used to capture data via digital sampling''')
   parser.add_argument('-v', "--verbose", action="store_true", help="displays numerical quantities to high precision")
   parser.add_argument('-vr', "--volts", action="store_true", help="shows volt range options")
   parser.add_argument('-loc', "--location", type=str, help="[string] enter location instead of lat, lon. Format: 'address, city, state', e.g., 'University Dr., Berkeley, CA'")
   parser.add_argument('-lt', "--lat", type=float, help="[float] takes in latitude")
   parser.add_argument('-lg', "--lon", type=float, help="[float] takes in longitude")
   parser.add_argument('-az', "--azimuth", type=float, help="[float] take in azimuth")
   parser.add_argument('-alt', "--altitude", type=float, help="[float] take in altitude")
   parser.add_argument('-c', "--capture", action="store_true", help="captures data")
   parser.add_argument('-d', "--directory", type=str, help="[string] write data to new directory")
   parser.add_argument('-ns', "--numsamples", type=int, help="[int] sets the number of samples to take")
   parser.add_argument('-nb', "--numblocks", type=int, help="[int] sets the number of blocks to take")
   parser.add_argument('-div', "--divisor", type=int, help="[int] sets the divisor (sample rate)")
   parser.add_argument('-sr', "--srate", type=int, help="[int] returns what the sample rate would be (base_rate/input)")
   parser.add_argument('-t', "--time", action="store_true", help="prints the current time. Unix, utc, and local system time.")
   args = parser.parse_args()

   '''print time if toggled'''
   if args.time:
      print(f"The current unix time is: {get_time()}")
      print(f"The current UTC time is: {get_utc()}")
      print(f"The current local system time is: {get_date()}")

   '''return what the sample rate would be'''
   if args.srate:
      base_rate = 62.5e6
      print(f"The sample rate would be {base_rate/args.srate:2.5e} Hz")

   '''print volt_range options'''
   if args.volts:
      print("['50mV', '100mV', '200mV', '500mV', '1V', '2V', '5V', '10V', '20V']")
      

   '''set location if location is toggled'''
   if args.location:
       try:
           location = EarthLocation.of_address(args.location)
           print(f"Location set to lat[{location.lat}] lon[{location.lon}]")
       except:
           print("[[LOCATION LOOKUP ERROR]]")
           sys.exit(1)
   else:
       location = None

   '''capture data if toggled'''
   if args.capture:
       try:
           if args.numsamples:
               for i in range(args.numsamples):
                   capture()
           else:
               capture()
           
       except Exception:
           print("[[DATA CAPTURE ERROR]]")
           traceback.print_exc()
           sys.exit(1)


           
# import all dependancies if imported as a module
else:
   from sys import argv
   import sys
   import os
   import subprocess
   import re
   import argparse
   import pprint
   import numpy as np
   import scipy as sp
   import ugradio
   import astropy.time as at
   from astropy.coordinates import SkyCoord
   from astropy.coordinates import EarthLocation
   from astropy.coordinates import AltAz
   from astropy import units as u
   from astropy.time import Time
   import matplotlib.pyplot as plt
   import traceback
   import time

