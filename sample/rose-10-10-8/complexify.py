import numpy as np
import matplotlib.pyplot as plt
from progress.bar import Bar

# take in raw data
data_rose = np.loadtxt('avgrose-10-10-1')

length = len(data_rose)
half_length = int(length/2)
# make complex numpy array with data
complex_data_rose = np.empty(half_length, dtype=complex)
complex_data_rose.real = data_rose[:half_length]
complex_data_rose.imag = data_rose[half_length:]

# compute fourier transform
fourier_rose = np.fft.fft(complex_data_rose)
# sample rate is 62.5e6 Hz, spacing is inverse
sample_spacing = 1.28e-7 # 1.9200012288007864325e-7
fourier_axis_rose = np.fft.fftfreq(n=len(complex_data_rose), d=sample_spacing)
# fourier filter
fourier_rose[0] = 0



plt.plot(np.fft.fftshift(fourier_axis_rose), np.abs(np.fft.fftshift(fourier_rose))**2, label="Filtered Spectrum")

#plt.yscale('log')
plt.ylabel('Intensity ~W/Hz')
plt.xlabel(r'$\nu$ Hz')
plt.grid()
plt.legend()
plt.show()

'''
# 3dplot
from mpl_toolkits import mplot3d
ig = plt.figure()
ax = plt.axes(projection="3d")

X,Y = np.meshgrid(np.fft.fftshift(fourier_axis_diff), np.fft.fftshift(fourier_axis_diff))
#p = np.meshgrid(np.ones(len(X)), np.ones(len(X)))
p = np.divide(X,X)
p*1000
Z = (np.abs(np.fft.fftshift(fourier_diff.imag))**2)*p
ax.plot_surface(X, Y, Z)
ax.set_ylim(-500000, 500000)
ax.set_xlim(-500000, 500000)

plt.show()
'''


# 3dplot stuff
'''
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d.axis3d as axis3d
from matplotlib import cm
import pylab
import mpmath
mpmath.dps = 5


# New axis settings
custom_AXINFO = {
    'x': {'i': 0, 'tickdir': 1, 'juggled': (1, 0, 2),
          'color': (0.25, 0.25, 0.25, .25)},
    'y': {'i': 1, 'tickdir': 0, 'juggled': (0, 1, 2),
          'color': (0.25, 0.25, 0.25, 0.25)},
    'z': {'i': 2, 'tickdir': 0, 'juggled': (0, 2, 1),
          'color': (.25, .25, .25, .25)},}

class custom_XAxis(axis3d.Axis):
    _AXINFO = custom_AXINFO

class custom_YAxis(axis3d.Axis):
    _AXINFO = custom_AXINFO

class custom_ZAxis(axis3d.Axis):
    _AXINFO = custom_AXINFO

class custom_Axes3D(Axes3D):
    def _init_axis(self):
        #Init 3D axes; overrides creation of regular X/Y axes
        self.w_xaxis = custom_XAxis('x', self.xy_viewLim.intervalx,
                                    self.xy_dataLim.intervalx, self)
        self.xaxis = self.w_xaxis
        self.w_yaxis = custom_YAxis('y', self.xy_viewLim.intervaly,
                            self.xy_dataLim.intervaly, self)
        self.yaxis = self.w_yaxis
        self.w_zaxis = custom_ZAxis('z', self.zz_viewLim.intervalx,
                            self.zz_dataLim.intervalx, self)
        self.zaxis = self.w_zaxis

        for ax in self.xaxis, self.yaxis, self.zaxis:
            ax.init3d()

# The rest of your code below, note the call to our new custom_Axes3D

fig = pylab.figure()
ax = custom_Axes3D(fig)
maximum = np.argmax(np.abs(fourier_diff)**2)
print(maximum)
print(len(fourier_diff))
X,Y = np.meshgrid(np.fft.fftshift(fourier_axis_diff)[6900:7000], np.fft.fftshift(fourier_axis_diff)[6900:7000])
xn, yn = X.shape
W = X*0
bar = Bar('Computing 3D Plot', max=100**2)
for xk in range(xn):
    for yk in range(yn):
        try:
            #z = complex(X[xk,yk],Y[xk,yk])
            #w = float(f(z))
            z = complex(fourier_diff[6900 + xk].real, fourier_diff[6900 + yk].imag)
            w = np.abs(z)**2
            if w != w:
                raise ValueError
            W[xk,yk] = w
        except (ValueError, TypeError, ZeroDivisionError):
            # can handle special values here
            pass
        bar.next()
bar.finish()

# can comment out one of these
ax.plot_surface(X, Y, W, rstride=1, cstride=1, cmap=cm.jet)
ax.set_xlabel('real')
ax.set_ylabel('imaginary')
ax.set_zlabel('intensity')
#ax.axis('off')
#ax.xaxis.set_ticks_position('none')
#ax.yaxis.set_ticks_position('none')
plt.gca().xaxis.set_major_locator(plt.NullLocator())
plt.gca().yaxis.set_major_locator(plt.NullLocator())
plt.gca().zaxis.set_major_locator(plt.NullLocator())
ax.grid(True)

#ax.plot_wireframe(X, Y, W, rstride=5, cstride=5)

pylab.show()
'''