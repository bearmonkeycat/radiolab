import numpy as np
import matplotlib.pyplot as plt

# take in raw data
data = np.loadtxt('averaged_ouput')

# make complex numpy array with data
complex_data = np.empty(16000, dtype=complex)
complex_data.real = data[:16000]
complex_data.imag = data[16000:]

# compute fourier transform
fourier = np.fft.fft(complex_data)
# sample rate is 62.5e6 Hz, spacing is inverse
sample_spacing = 1.6e-8
fourier_axis = np.fft.fftfreq(n=len(complex_data), d=sample_spacing)
# fourier filter
fourier[0] = 0

# plot results
#print(fourier.size)
plt.plot(fourier_axis, np.abs(fourier)**2, label="complex")
plt.plot(fourier_axis, np.abs(fourier.imag)**2, label="imaginary")
plt.plot(fourier_axis, np.abs(fourier.real)**2, label="real")
plt.yscale('log')
plt.grid()
plt.legend()
plt.show()
