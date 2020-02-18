import ugradio
import numpy as np
# script to take data from signal generator
# for Astro 121 Group "Space Waves"

# default voltage ranges from ugradio package
# ugradio.pico.VOLT_RANGE = ['50mV', '100mV', '200mV', '500mV', '1V', '2V', '5V', '10V', '20V']

# set for data taking
vrange = ugradio.pico.VOLT_RANGE[0]
division = 1 # 5 will turn 62.5 MHz sample rate into 12.5 MHz sample rate

# should be power of 2
# defaults to 16000
'''use argument nsamples=samples'''

# samples = 2**12

# dual mode (set to True to sample both A and B ports)
mode = True

# capture data and write to file (will repeat N times)
N = 3
for i in range(11):
    data = ugradio.pico.capture_data(vrange, 1, dual_mode=mode)
    np.savetxt(f'output-ssb-mixer-{i}', data)
