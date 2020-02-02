import ugradio
import numpy as np
# script to take data from signal generator
# for Astro 121 Group "Space Waves"

# default voltage ranges from ugradio package
# ugradio.pico.VOLT_RANGE = ['50mV', '100mV', '200mV', '500mV', '1V', '2V', '5V', '10V', '20V']

# set for data taking
vrange = ugradio.pico.VOLT_RANGE[4]
division = 5 # will turn 62.5 MHz sample rate into 12.5 MHz sample rate

# capture data and write to file
data = ugradio.pico.capture_data(vrange, 5)
np.savetxt('output', data)
