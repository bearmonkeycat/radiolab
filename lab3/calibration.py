import numpy as np
import matplotlib.pyplot as plt
from IPython import embed

def casAlow(x):
    a = 5.625
    b = -0.634
    c = -0.023
    return 10**(a + b*np.log10(x) + c*(np.log10(x)**2))

def casAhigh(x):
    a = 5.880
    b = -0.792
    c = 0
    return 10**(a + b*np.log10(x) + c*(np.log10(x)**2))


def cygAlow(x):
    a = 4.695
    b = 0.085
    c = -0.178
    return 10**(a + b*np.log10(x) + c*(np.log10(x)**2))


def cygAhigh(x):
    a = 7.161
    b = -1.244
    c = 0
    return 10**(a + b*np.log10(x) + c*(np.log10(x)**2))


def crab(x):
    a = 3.915
    b = -0.299
    c = 0
    return 10**(a + b*np.log10(x) + c*(np.log10(x)**2))


def virgo(x):
    a = 5.023
    b = -0.856
    c = 0
    return 10**(a + b*np.log10(x) + c*(np.log10(x)**2))

arrayfreq = 1.07e4

# plot measured values
orion = 36.198
craby = 41.415
cassy = 55.569
cygA = 0

plt.loglog(arrayfreq, orion, "o", markersize=7, label="Orion*")
plt.loglog(arrayfreq, craby, "o", markersize=7, label="Crab*")
plt.loglog(arrayfreq, cassy, "o", markersize=7, label="Cas*")
#plt.loglog(arrayfreq, cygA, "o", markersize=7, label="Cyg*")

caslow = np.linspace(22,300,1000)
cashigh = np.linspace(300, 31e3, 1000)
cyglow = np.linspace(20,2e3, 1000)
cyghigh = np.linspace(2e3, 31e3, 1000)
crabspace = np.linspace(1e3,35e3, 1000)
virgospace = np.linspace(400, 25e3, 1000)

plt.loglog(caslow, casAlow(caslow), label=r"Cas A Low $\nu$")
plt.loglog(cashigh, casAhigh(cashigh), label=r"Cas A High $\nu$")
plt.loglog(cyglow, cygAlow(cyglow), label=r"Cyg A Low $\nu$")
plt.loglog(cyghigh, cygAhigh(cyghigh), label=r"Cyg A High $\nu$")
plt.loglog(crabspace, crab(crabspace), label=r"Taurus A")
plt.loglog(virgospace, virgo(virgospace), label=r"Virgo A")


# plot calculated values
plt.loglog(arrayfreq, crab(arrayfreq), color="k", markersize=5, marker="+")
plt.loglog(arrayfreq, cygAhigh(arrayfreq), color="k", markersize=5, marker="+")
plt.loglog(arrayfreq, casAhigh(arrayfreq), color="k", markersize=5, marker="+")
plt.loglog(arrayfreq, virgo(arrayfreq), color="k", markersize=5, marker="+")
print(f'crab should be {crab(arrayfreq)}')
print(f'virgo should be {virgo(arrayfreq)}')
print(f'cyg should be {cygAhigh(arrayfreq)}')
print(f'cas should be {casAhigh(arrayfreq)}')
plt.annotate(f'{crab(arrayfreq):.2f}', (arrayfreq, crab(arrayfreq)))
plt.annotate(f'{casAhigh(arrayfreq):.2f}', (arrayfreq, casAhigh(arrayfreq) - 150))
plt.annotate(f'{virgo(arrayfreq):.2f}', (arrayfreq, virgo(arrayfreq)))
plt.annotate(f'{cygAhigh(arrayfreq):.2f}', (arrayfreq, cygAhigh(arrayfreq)))



plt.grid()
plt.legend()
plt.ylabel(r'Flux Density [Jy]')
plt.xlabel(r'$\nu [MHz]$')
plt.show()

# embed()
