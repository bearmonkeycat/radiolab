import numpy as np
import matplotlib.pyplot as plt

# take in raw data
data_heart = np.loadtxt('avg')

# make complex numpy array with data
complex_data_heart = np.empty(16000, dtype=complex)
complex_data_heart.real = data_heart[:16000]
complex_data_heart.imag = data_heart[16000:]

# compute fourier transform
fourier_heart = np.fft.fft(complex_data_heart)
# sample rate is 62.5e6 Hz, spacing is inverse
sample_spacing = 1.9200012288007864325e-7
fourier_axis_heart = np.fft.fftfreq(n=len(complex_data_heart), d=sample_spacing)
# fourier filter
fourier_heart[0] = 0


# calculate the gain
'''
T_human = 310.15
T_sky = 3
G = ((T_human - T_sky)/(np.sum(np.abs(fourier_human)**2 - np.abs(fourier_sky)**2)))*(np.sum(np.abs(fourier_sky)**2))
print(f"The gain of the system is: {G:5.5f}")
  '''

# plot results
plt.plot(np.fft.fftshift(fourier_axis_heart), np.abs(np.fft.fftshift(fourier_heart))**2, label="heart nebula")
#plt.yscale('log')
plt.ylabel('Intensity ~W/Hz')
plt.xlabel(r'$\nu$ Hz')
plt.grid()
plt.legend()
plt.show()
#savefig('tempdiff.png')
