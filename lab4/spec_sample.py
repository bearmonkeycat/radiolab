#!/usr/bin/env python
import sys
import os
import subprocess
import re
import argparse
import numpy as np
import ugradio
from ugradio.leusch import LeuschTelescope, LeuschNoise, ALT_MIN, ALT_MAX, AZ_MIN, AZ_MAX
from ugradio.leusch import Spectrometer
from ugradio.agilent import SynthDirect
import astropy.time as at
from astropy.coordinates import SkyCoord, EarthLocation, AltAz, Galactic
from astropy import units as u
from astropy.time import Time
import traceback
import time
""" Program to capture data from Leuschner observatory via digital sampling

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

#####################################################################################
def capture(loc, integration, target, errors, file_name=None):
    '''Capture data from Leuschner Spectrometer, uses tracking module'''
    breakout = 0
    # verify pointing
    # get current ra/dec of target
    az, alt, breakout = get_coordinates(target, verify=True)
    if breakout == 1:
        return 1
    
    '''object verified, continue tracking and capture'''    
    # make instance of agilent freqency synthesizer
    agilent = SynthDirect()

    # make instance of FPGA spectrometer interface
    spec = Spectrometer()

    # make instance of telescope control interface
    scope = LeuschTelescope()

    # make instance of noise diode control interface
    nd = LeuschNoise()
     
    # logistics for storing data capture
    if file_name is None:
        if args.target:
            file_name = str(args.target).replace(" ","") + str(get_time(unix=get_time())) + "jd"
        else:
            file_name = str(get_time(unix=get_time())) + "jd"

    # set up spectrometer
    print(f"{spec.check_connected()}") # make sure the spectrometer is connected
    # 3.5 seconds per integration (5 spectra)

    # set local oscillator for down mixing
    # frequency presets
    freq = 635
    freqoff = 636
    #for andromeda
    #freq = 637
    #freqoff = 639

    # set to standard frequency
    agilent.set_frequency(freq, 'MHz') # there is a frequency doubler
    print(f"The LO was told to be {freq} MHz")
    #print(f"The LO is set to {agilent.get_frequency()}")

    # calibrate (make sure noise is off before taking data)
    nd.off()
    print("Noise diode is off.")
    
    # set up for loop
    start = get_time()
    intendedpositions = []
    actualpositions = []
    j2000 = None
    pointing_count = 0
    calibration = 0
    first_point = 1
    while(get_time()-start < integration):
        '''main tracking loop'''
        # start cycle timer
        cstart = get_time()

        # get coordiantes, check for breakout
        vector, eqvector,  breakout = get_coordinates(target)
        if breakout == 1:
            print("[[BREAKING OUT OF POINTING]]")
            return 1
        
        # slew
        scope.point(eqvector[0], eqvector[1])
        
        # compensate for large slew time on first pointing
        if first_point == 1:
            integration = integration + (get_time() - start)
            first_point = 0
            
        # calibration
        if calibration == 0:
            nd.on()
            calibrationname = file_name + "calibration.fits"
            spec.read_spec(calibrationname, 5, vector, 'eq')
            nd.off()
            print("Calibration complete, noise diode is off.")
            calibration = 1
        
        # capture data: on/off
        specnameon = str(pointing_count) + file_name + "on.fits"
        specnameoff = str(pointing_count) + file_name + "off.fits"
        spec.read_spec(specnameon, 5, vector, 'eq')
        agilent.set_frequency(freqoff, 'MHz')
        print(f"The LO was told to be {freqoff} MHz")
        #print(f"The LO is set to {agilent.get_frequency()}")
        spec.read_spec(specnameoff, 5, vector, 'eq')
        agilent.set_frequency(freq, 'MHz') # switch back to standard frequency
        print(f"The LO was told to be {freq} MHz")
        #print(f"The LO is set to {agilent.get_frequency()}")
        
        pointing_count += 1

        # record pointing information
        pointing = scope.get_pointing()
        print(f"Telescope pointing at {pointing}")
        intendedpositions.append((alt, az))
        actualpositions.append(pointing)
        # check cycle time and delay if needed
        cfinish = get_time()
        cycle = cfinish-cstart
        print(f"Cycle took {cycle} seconds")
        tt = get_time() - start
        print(f"Tracked for {tt} seconds")
        print(f"Time till completion {integration - tt} seconds")
        if(cycle < 10):
            print("sleeping")
            time.sleep(10 - cycle)

    '''out of main tracking loop'''
    # tracking completed, get total time        
    finish = get_time()

    # save data (or breakout)
    if breakout == 1:
        print("[[BREAKING OUT OF POINTING]]")
        return 1
    else:
        print("Data capture finished.")
        tag_data(file_name, start, finish)
        np.savez('intendedpositionsfile' + file_name, intendedpositions)
        np.savez('actualpositionsfile' + file_name, actualpositions)
        print("Tag file written.")
        return 0







    



#####################################################################################
# get current ra/dec of target
def get_coordinates(target, verify=False):
    '''Return current precessed coordinates of target'''
    if target == 'moon':
        vector = ugradio.coord.moonpos(get_time(unix=get_time()))
    elif target == 'sun':
        vector = ugradio.coord.sunpos(get_time(unix=get_time()))
    else:
        j2000 = target
        pra, pdec  = ugradio.coord.precess(j2000[0], j2000[1])
        vector = (pra, pdec)
        
    # reposition telescope taking into account limits of alt-az mount
    eqvector = ugradio.coord.get_altaz(vector[0], vector[1])   
    az = eqvector[1]
    alt = eqvector[0]
    if j2000:
        print(f"Target was at ra={j2000[0]} dec={j2000[1]} [J2000]")
        print(f"Target at ra={vector[0]} dec={vector[1]}")
    print(f"Target at az={az} alt={alt}")

    # check azimuth
    if az < AZ_MIN:
        print('[[OBJECT BELOW TELESCOPE AZIMUTH]]')
        return vector, eqvector, 1    
    elif az > AZ_MAX:
        print('[[OBJECT ABOVE TELESCOPE AZIMUTH]]')
        return vector, eqvector, 1
    
    # check altitude
    if verify:
        if alt < (ALT_MIN + np.pi):
            print('[[OBJECT BELOW TELESCOPE HORIZON]]')
            return vector, eqvector, 1
        elif alt > ALT_MAX:
            print('[[OBJECT ABOVE  TELESCOPE HORIZON]]')
            return vector, eqvector, 1
    else:
        
        if alt < (ALT_MIN):
            print('[[OBJECT BELOW TELESCOPE HORIZON]]')
            return vector, eqvector, 1
        elif alt > ALT_MAX:
            print('[[OBJECT ABOVE  TELESCOPE HORIZON]]')
            return vector, eqvector, 1
        
    # coordiantes are good, return them
    return vector, eqvector, 0







    

    
    
#####################################################################################
def tag_data(file_name, start, finish):
    '''Tag data capture with a text file containing time/data/location information'''
    # make output file name
    ofname = "tagfile-" + file_name + "xyz"

    # list of parameter names for data capture
    with open(ofname, 'w') as output:
        output.write(f"\n[[METADATA FOR DATA SAMPLES IN {file_name}]]\n")

        # write out internet metadata
        output.write(f"{get_date()}\n")
        output.write(f"{get_date(utc=True)}\n")
        output.write(f"Sampling was started at (unix): {start}\n")
        output.write(f"Sampling was completed at (unix): {finish}\n")
        output.write(f"Data capture took: {finish - start} seconds\n")
        output.write(f"Julian date of sample: {get_time(unix=start)}\n")                

        # write out location information
        output.write(f"\n[[LOCATION INFORMATION]]\n")
        if args.lat:
            output.write(f"User input latitude: {args.lat}\n")
        if args.lon:
            output.write(f"User input longitude: {args.lon}\n")
        if location is not None:
            output.write(f"Location was set to: {args.location}\n") 
            output.write(f"lat[{location.lat}] lon[{location.lon}]\n")

        # write out target information
        output.write(f"\n[[TARGET INFORMATION]]\n")
        if args.rightascention:
            output.write(f"Target right acension: {args.rightascention}\n")
        if args.declination:
            output.write(f"Target declination: {args.declination}\n")
        if args.target:
            output.write(f"Target was: {args.target}\n")
        if args.trackduration:
            output.write(f"Target was tracked for: {args.trackduration} seconds\n")

        # make room for lab notes
        output.write("\n\n[[LAB NOTES]]\n")

        # end of file marker
        output.write('\neof\n')

    # tag file written    
    print(f"tag file written to {ofname}")

    







    
#####################################################################################
def coordinates(latitude, longitude):
    '''Transform coordinates to galatic coordinates'''
    c = SkyCoord(longitude, latitude, unit='deg')
    return c

def get_altaz(alt, az):
    '''Return altitude and azimuth'''
    obs = AltAz(alt=alt*u.deg, az=az*u.deg, location=nch, obstime=Time.now())
    return obs

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

   if jd is not None:
       t = at.Time(jd, format='jd')
       return t.unix
      
       
   elif unix is not None:
       t = at.Time(unix, format='unix')
       return t.jd
    
   else:
       t = time.time()
       return t

   
def get_utc():
    utc = Time.now()
    return utc


def get_lst():
    lst = 0 # need to implement this
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





    
        



    
#####################################################################################
#####################################################################################
# main program implemented as boiler plate logic
if __name__ == "__main__":

   # nch location
   nch = EarthLocation(lat="37.8732", lon="-122.2573", height=123.1*u.m)
   leuschner = EarthLocation(lat="37.9193", lon="-122.1539", height=304*u.m)
   
   # argparse stuff
   parser = argparse.ArgumentParser(description='''Program used to capture data via digital sampling''')
   parser.add_argument('-loc', "--location", type=str, help="[string] enter location instead of lat, lon. Format: 'address, city, state', e.g., 'University Dr., Berkeley, CA'")
   parser.add_argument('-lt', "--lat", type=float, help="[float] takes in latitude")
   parser.add_argument('-lg', "--lon", type=float, help="[float] takes in longitude")
   parser.add_argument('-ra', "--rightascention", type=float, help="[float] take in right ascention")
   parser.add_argument('-dec', "--declination", type=float, help="[float] take in declination")
   parser.add_argument('-c', "--capture", action="store_true", help="captures data")
   parser.add_argument('-tg', "--target", type=str, help="[string] input target")
   parser.add_argument('-tgf', "--targetfile", type=str, help="[string] input target file (with ra, dec for acquistion)")
   parser.add_argument('-dt', "--trackduration", type=int, help="[int] sets time to track for")
   parser.add_argument('-t', "--time", action="store_true", help="prints the current time. Unix, utc, and local system time.")
   args = parser.parse_args()

   '''print time if toggled'''
   if args.time:
      print(f"The current unix time is: {get_time()}")
      print(f"The current UTC time is: {get_utc()}")
      print(f"The current local system time is: {get_date()}")


   # check for proper lat-lon values
   if args.lat:
       assert(-90 <= args.lat <= 90)
   if args.lon:
       assert(-180 <= args.lon <= 180)

       
   '''set location if location is toggled'''
   if args.location:
       try:
           location = EarthLocation.of_address(args.location)
           print(f"Location set to lat[{location.lat}] lon[{location.lon}]")
       except:
           print("[[LOCATION LOOKUP ERROR]]")
           sys.exit(1)
   else:
       location = leuschner # change this depending on observatory

       
   '''check for local celetial bodies'''
   if args.target:
       if  args.target == 'sun':
           tg = 'sun'
       elif args.target == 'moon':
           tg = 'moon'
       elif args.target:
           try:
               obj = SkyCoord.from_name(args.target)
               tg = (obj.ra, obj.dec)
               print(f"Target set to {args.target}")
           except:
               print("[[OBJECT LOOKUP ERROR]]")
               sys.exit(1)
       else:
           '''make target with ra and dec'''
           if args.rightascention:
               ra = args.rightascention
           else:
               print("[[RIGHT ASCENTION MISSING]]")
               sys.exit(1)
           if args.declination:
               dec = args.declination
           else:
               print("[[DECLIATION MISSING]]")
               sys.exit(1)
           tg = (ra, dec)

   '''check for time duration to track'''
   # change to integration time (/ # of spectra)
   if args.trackduration:
       duration = args.trackduration
   else:
       duration = 10 # default to ten seconds
            
   '''capture data if toggled'''
   if args.capture:
       # main loop variables
       begin = time.time()
       errors = 0
       now = time.time()
       elapsed = begin - now
       
       # check for target file
       if args.targetfile:
           targetfile = np.load(args.targetfile, allow_pickle=True).item()
           print(f"Iterating through target file {args.targetfile}.")
           try:
               checkfileTemp = np.load('completed.npy', allow_pickle=True)
               checkfile = checkfileTemp.tolist()
           except Exception:
               print("[[NO COMPLETED FILE]]")
               checkfile = []
           
       while(elapsed < duration):
           '''loop will make tracking continue even if there is an error'''
           print(f"Total tracking time: {begin - elapsed}")
           print(f"Remaining tracking time: {duration - (begin - elapsed)}")
           if args.targetfile:
               location = leuschner
               # set integration time (900 for orion) -> (420) -> (180)
               integration = 180 # duration for total loop, integration for sub loops (doubled for on/off)
               for i in range(len(targetfile)):
                   tg =  targetfile[f'{i}'].tolist()
                   if tg not in checkfile:
                       try:
                           pointing_name = f"pointing{i}"
                           return_status = capture(location, integration, tg, errors, pointing_name)
                           # add this pointing to check file
                           if return_status == 0:
                               checkfile.append(targetfile[f'{i}'].tolist())
                               np.save('completed.npy', checkfile)
                               print(f"Pointing {i} completed, checkfile saved.\n\n")
                               now = time.time()
                               elapsed = begin - now
                           else:
                               print("[[TRACKING ERROR]]")
                               print("[[SWITCHING TO NEXT POINTING]]")
                               now = time.time()
                               elapsed = begin - now
                               continue
                           
                       except Exception:
                           print("[[DATA CAPTURE ERROR]]")
                           errors += 1
                           traceback.print_exc()
                           now = time.time()
                           elapsed = begin - now
                           if elapsed > duration:
                               print("[[BEYOND SCHEDULED TRACK DURATION]]")
                               np.save('completed.npy', checkfile)
                               print("Checkfile saved, exiting.")
                               sys.exit(1)
                               # need anything here?
                           print(f"Restarting tracking code, there have been {errors} errors, will continue for {duration - elapsed} seconds.\n\n")
                           continue
                   else:
                       continue
                
               print("[[ALL POINTINGS ATTEMPTTED]]")
               print("[[EXITING]]")
               sys.exit(0)
               
           else:
               try:
                   return_status = capture(location, duration, tg, errors)
                   break
           
               except Exception:
                   print("[[DATA CAPTURE ERROR]]")
                   errors += 1
                   traceback.print_exc()
                   now = time.time()
                   elapsed = begin - now 
                   if elapsed > duration:
                       print("[[BEYOND SCHEDULED TRACK DURATION]]")
                       print("[[EXITING]]")
                       sys.exit(1)                       
                   print(f"Restarting tracking code, there have been {errors} errors, will continue for {duration - elapsed} seconds.\n\n")
                   continue

               print("[[ALL POINTINGS ATTEMPTTED]]")
               print("[[EXITING]]")
               sys.exit(0)
