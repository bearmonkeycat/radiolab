import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import scipy.optimize as optimize
import scipy.stats as stats
import math

# load data
darray = []
for i in range(32):
    darray.append(np.loadtxt(f'output-noise-{i}'))

# calculate average mean of all blocks
mean_array = []
for i in range(32):
    mean_array.append(np.mean(darray[i]))

average_mean = np.mean(mean_array)
print(mean_array)
print(f"The average mean is {average_mean}")

# calculate average variance of all blocks
variance_array = []
for i in range(32):
    variance_array.append(np.var(darray[i]))

average_variance = np.mean(variance_array)
print(variance_array)
print(f"The average variance is {average_variance}")

# calculate the average standard deviation of all blocks
# for a zero-mean distribution this is the same as the RMS
std_array = []
for i in range(32):
    std_array.append(np.std(darray[i]))

average_std = np.mean(std_array)
print(std_array)
print(f"The average standard deviation is {average_std}")


# gaussian curve fit
num_bins = 100
hist, bin_edges = np.histogram(darray[0], num_bins)
bincenters = 0.5*(bin_edges[1:] + bin_edges[:-1])
error = np.sqrt(hist)

def gaussian(x, a, mu, sigma):
    return (a/(sigma*np.sqrt(2*np.pi)))*np.exp(-((x-mu)/sigma)**2/2)

p0 = [10, average_mean, average_std]
popt, pcov = optimize.curve_fit(gaussian, bincenters, hist, p0)
perr = np.sqrt(np.diag(pcov))

nu = np.linspace(-30000, 30000, 10000)

# plot the histogram with curve fit
'''
plt.hist(darray[0], bins=100)
plt.plot(nu, gaussian(nu, popt[0], popt[1], popt[2]))
plt.xlabel(r"$\nu$ Hz (100 bins)")
plt.ylabel("Number per bin")
plt.grid()
plt.show()
'''

# compute the power spectrum of each block
pspecarray = []
vspecarray = []
for i in range(32):
    vspecarray.append(np.fft.fft(darray[i]))
    pspecarray.append(np.abs(vspecarray[i])**2)

# compute average of the power spectra
# pspecarray = np.array(pspecarray)
average_pspec = np.divide(sum(pspecarray), len(pspecarray))
average2_pspec = np.divide(sum(pspecarray[:1]), len(pspecarray[:1]))
average4_pspec = np.divide(sum(pspecarray[:3]), len(pspecarray[:3]))
average8_pspec = np.divide(sum(pspecarray[:7]), len(pspecarray[:7]))
average16_pspec = np.divide(sum(pspecarray[:15]), len(pspecarray[:15]))

# filter out the middle spike
average_pspec[0] = 0
average2_pspec[0] = 0
average4_pspec[0] = 0
average8_pspec[0] = 0
average16_pspec[0] = 0

# sample rate was r = 62.5 MHz
# sample spacing 1/r = 1.6e-8
f = np.fft.fftfreq(n=16000, d=1.6e-8)

# calculate signal to noise ratio (SNR)
# use log-log plot

N = [2, 4, 8, 16, 32]
noise_std = []
halfway = math.floor(len(average_pspec)/2)

noise_std.append(np.mean(average2_pspec)/np.std(average2_pspec))
noise_std.append(np.mean(average4_pspec)/np.std(average4_pspec))
noise_std.append(np.mean(average8_pspec)/np.std(average8_pspec))
noise_std.append(np.mean(average16_pspec)/np.std(average16_pspec))
noise_std.append(np.mean(average_pspec)/np.std(average_pspec))


# find slope of the curve
def linear_fit(x, n, b):
    return n*x + b

p0 = [2, 10]
popt, pcov = optimize.curve_fit(linear_fit, np.log(N), np.log(noise_std), p0)

x = np.linspace(np.log(2), np.log(32), 100)
y = linear_fit(x, popt[0], popt[1])

print(popt[0])
print(popt[1])

# plt.plot(f, pspecarray[0], label="First Block")
# plot signal to noise

plt.plot(np.log(N), np.log(noise_std), label="SNR")
plt.plot(x,y, label="Linear Fit")
plt.ylabel(r"$\log(\mu/\sigma)$")
plt.xlabel(r"$\log(N)$")
plt.legend()
plt.grid()
plt.show()



print(average_pspec)
# plot power spectrums
'''
plt.plot(f[:halfway], average2_pspec[:halfway], label="Average Power Spectrum N=2")
plt.plot(f[:halfway], average4_pspec[:halfway], label="Average Power Spectrum N=4")
plt.plot(f[:halfway], average8_pspec[:halfway], label="Average Power Spectrum N=8")
plt.plot(f[:halfway], average16_pspec[:halfway], label="Average Power Spectrum N=16")
plt.plot(f[:halfway], average_pspec[:halfway], label="Average Power Spectrum N=32")
plt.xlabel(r"$\nu$ Hz")
plt.ylabel("Unormalized Intensity ~W/Hz")
plt.grid()
plt.legend()
plt.show()
'''

# Fourier filtering
'''
index = np.argmax(average_pspec)
print(index)
print(average_pspec[index+1])
average_pspec[0]=0
plt.plot(f[:halfway], average_pspec[:halfway])
plt.show()
'''
