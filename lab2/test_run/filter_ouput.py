import numpy as np
# progess needs to be installed with pip
# pip install progess
from progress.bar import Bar

data = dict()

bar = Bar('Processing Data', max=10)
for i in range(10):
    data[f"dataset_{i}"] = np.loadtxt(f"output-ssb-mixer-{i}")
    bar.next()

bar.finish()
averages = []

bar = Bar('Averaging Data', max=10)
for data_set in data:
    averages.append(data[data_set])
    bar.next()
bar.finish()

average = np.average(averages, axis=0)

#print(average)
#print(len(average))
np.savetxt('avgtest', average)
