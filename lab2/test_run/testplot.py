import numpy as np
import matplotlib.pyplot as plt

# load data
data = np.loadtxt('avgtest')

# make complex numpy array with data
complex_data = np.empty(16000, dtype=complex)
complex_data.real = data[:16000]
complex_data.imag = data[16000:]

# compute fourier transform
fourier_data = np.fft.fft(complex_data)
# sample rate is 62.5e6 Hz, spacing is inverse
sample_spacing = 1.6e-8
fourier_axis = np.fft.fftfreq(n=len(complex_data), d=sample_spacing)
# fourier filter
fourier_data[0] = 0 

# plot result
plt.plot(fourier_axis, np.abs(np.fft.fftshift(fourier_data))**2, label="Test Run")
#plt.yscale('log')
plt.grid()
plt.xlabel(r'$\nu$ Hz')
plt.ylabel('Column Density')
plt.legend()
plt.show()
