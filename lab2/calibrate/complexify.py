import numpy as np
import matplotlib.pyplot as plt

# take in raw data
data_human = np.loadtxt('human')
data_sky = np.loadtxt('sky')

# make complex numpy array with data
complex_data_human = np.empty(16000, dtype=complex)
complex_data_human.real = data_human[:16000]
complex_data_human.imag = data_human[16000:]

# compute fourier transform
fourier_human = np.fft.fft(complex_data_human)
# sample rate is 62.5e6 Hz, spacing is inverse
sample_spacing = 1.6e-8
fourier_axis_human = np.fft.fftfreq(n=len(complex_data_human), d=sample_spacing)
# fourier filter
fourier_human[0] = 0


# make complex numpy array with data
complex_data_sky = np.empty(16000, dtype=complex)
complex_data_sky.real = data_sky[:16000]
complex_data_sky.imag = data_sky[16000:]

# compute fourier transform
fourier_sky = np.fft.fft(complex_data_sky)
# sample rate is 62.5e6 Hz, spacing is inverse
sample_spacing = 1.6e-8
fourier_axis_sky = np.fft.fftfreq(n=len(complex_data_sky), d=sample_spacing)
# fourier filter
fourier_sky[0] = 0

# calculate the gain
T_human = 310.15
T_sky = 3
G = ((T_human - T_sky)/(np.sum(np.abs(fourier_human)**2 - np.abs(fourier_sky)**2)))*(np.sum(np.abs(fourier_sky)**2))
print(f"The gain of the system is: {G:5.5f}")
     
# plot results
plt.plot(fourier_axis_human, np.abs(np.fft.fftshift(fourier_human))**2, label="human")
plt.plot(fourier_axis_sky, np.abs(np.fft.fftshift(fourier_sky))**2, label="sky")
plt.yscale('log')
plt.ylabel('Intensity ~W/Hz')
plt.xlabel(r'$\nu$ Hz')
plt.grid()
plt.legend()
plt.savefig('tempdiff.png')
