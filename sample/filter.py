import numpy as np
import subprocess
import os
# progess needs to be installed with pip
# pip install progess
from progress.bar import Bar

# get filenames
lsoutput = subprocess.Popen('ls', stdout=subprocess.PIPE)
(files, err) = lsoutput.communicate()
filenames = files.decode('utf-8')
filenames_list = filenames.split()

# sample rate
base_rate = 62.5e6
divisor = 12
sr = 1/(base_rate/divisor)

# load data
data = dict()
bar = Bar('Processing Data', max=100)
for i in range(100):
    data[f"dataset_{i}"] = [np.loadtxt(filenames_list[i])]
    complex_data = np.empty(16000, dtype=complex)
    complex_data.real = data[f"dataset_{i}"][0][:16000]
    complex_data.imag = data[f"dataset_{i}"][0][16000:]
    data[f"dataset_{i}"].append(complex_data)
    data[f"dataset_{i}"].append(np.abs(np.fft.fft(data[f"dataset_{i}"][1]))**2)
    data[f"dataset_{i}"].append(np.fft.fftfreq(n=len(data[f"dataset_{i}"][1]), d=sr))
    bar.next()
bar.finish()

# average data
averages = []
bar = Bar('Averaging Data', max=100)
for data_set in data:
    averages.append(data[data_set][2])
    bar.next()
bar.finish()
average = np.average(averages, axis=0)

# write output
np.savetxt('avg-pspec-heart-off', average)
