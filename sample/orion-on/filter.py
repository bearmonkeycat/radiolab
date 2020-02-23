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

# load data
data = dict()
bar = Bar('Processing Data', max=100)
for i in range(100):
    data[f"dataset_{i}"] = np.loadtxt(filenames_list[i])
    bar.next()
bar.finish()

# average data
averages = []
bar = Bar('Averaging Data', max=100)
for data_set in data:
    averages.append(data[data_set])
    bar.next()
bar.finish()
average = np.average(averages, axis=0)

# write output
np.savetxt('avg', average)
