import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import scipy.optimize as optimize
import scipy.stats as stats
import math
import ugradio

# load data
darray1 = []
for i in range(5,13):
    darray1.append(np.loadtxt(f'output-1-2**{i}'))

darray5 = []
for i in range(5,13):
    darray5.append(np.loadtxt(f'output-5-2**{i}'))

darray10 = []
for i in range(5,13):
    darray10.append(np.loadtxt(f'output-10-2**{i}'))


# normalize voltages
scale_factor = (darray1[7].max() - darray1[7].min()/1290)
scaled_data = darray1[7]/scale_factor
small_sample = darray1[5]/scale_factor

# compture fourier transform of square wave
fft = ugradio.dft.dft(scaled_data, vsamp=62.5e6)
fft_small = ugradio.dft.dft(small_sample, vsamp=62.5e6)

rms = scaled_data.max()/np.sqrt(2)
rms_array = [rms]*len(scaled_data)
print(len(darray1[5]))

plt.subplot(3,1,1)
t = np.linspace(0, len(darray1[7][-200:-1]), len(darray1[7][-200:-1]))
plt.plot(t, scaled_data[-200:-1], label="Time Series")
plt.plot(t, rms_array[-200:-1], label="RMS Voltage")
plt.annotate(f"{rms:2.3f} V", (0, rms))
plt.xlabel("time")
plt.ylabel(r"Voltage")
plt.legend()
plt.subplot(3,1,2)
plt.plot(fft[0],np.abs(fft[1])**2, color='lightcoral', label="N=4096")
plt.plot(fft_small[0], np.abs(fft_small[1] )**2, color="darkred", label="N=1024")
plt.xlabel(r"$\nu$ Hz")
plt.ylabel("Intensity")
plt.yscale('log')
plt.legend()
plt.subplot(3,1,3)
plt.plot(fft[0], fft[1], color='palegreen', label="N=4096")
plt.plot(fft_small[0],fft_small[1], color='darkgreen', label="N=1024")
plt.xlabel(r"$\nu$ Hz")
plt.ylabel("Intensity")
plt.yscale('log')
plt.legend()
plt.grid()
plt.show()
