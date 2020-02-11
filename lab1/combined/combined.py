import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import scipy.signal as signal

# load the data
darray = []
data1 = np.loadtxt('output-1-10-10.1')
darray.append(data1)
data2 = np.loadtxt('output-1-10-10.01')
darray.append(data2)
data3 = np.loadtxt('output-1-10-10.001')
darray.append(data3)
data4 = np.loadtxt('output-1-10-10.0001')
darray.append(data4)
data5 = np.loadtxt('output-1-10-10.00001')
darray.append(data5)
data6 = np.loadtxt('output-1-10-10.000001')
darray.append(data6)
data7 = np.loadtxt('output-1-10-10.0000001')

freqs = [10.1, 10.01, 10.001, 10.0001, 10.00001, 10.000001, 10.0000001]

strfreqs = [f"{item:1.7e}" for item in freqs]

# scale the data to voltages
# voltage oscillated wildly for this measurement

# analyze the data with fourier transform to find freqencies
fftarray = []
for i in range(6):
    fftarray.append(np.fft.fft(darray[i]))

nu = np.fft.fftfreq(n=16000, d=8e-8)

for i in range(0,4):
    plt.plot(nu, np.abs(fftarray[i])**2, label=strfreqs[i])

plt.xlabel(r"$\nu$ Hz")
plt.ylabel("Unormalized Intensity ~W/Hz")
plt.xscale('log')
plt.grid()
plt.legend()
plt.show()

fftfreqs = []
for i in range(7):
    fftfreqs.append(np.abs(nu[np.argmax(np.abs(fftarray[i]))]))

'''
plt.plot(freqs, marker="o", label="Exact Frequencies")
plt.plot(fftfreqs, marker="+", linestyle="None", label="FFT Frequencies (Data)")
plt.xlabel(r"$\nu_0$ is varied for 9 data captures")
plt.ylabel(r"$\nu_{fft}$ [Hz] is returned")
plt.yscale('log')
for i in range(9):
    plt.annotate(str(ferror[i]), (points[i], fftfreqs[i]))
plt.yticks(fftfreqs, fftfreqticks, style="italic")
plt.legend()
plt.grid()
plt.show()
'''

''' plotting real and imaginary parts of voltage spectrum '''

'''
plt.plot(nu, fftarray[8].real)
plt.plot(nu, fftarray[8].imag)
plt.show()
'''


# power spectrum stuff
pspecarray = []
for i in range(6):
    pspecarray.append(np.abs(fftarray[i])**2)
