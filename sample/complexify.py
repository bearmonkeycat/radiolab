import numpy as np
import matplotlib.pyplot as plt
from progress.bar import Bar

# take in raw data
data_hearton = np.loadtxt('avg-on')
data_heartoff = np.loadtxt('avg-off')
diff = data_hearton - data_heartoff

# make complex numpy array with data
complex_data_hearton = np.empty(16000, dtype=complex)
complex_data_hearton.real = data_hearton[:16000]
complex_data_hearton.imag = data_hearton[16000:]

# compute fourier transform
fourier_hearton = np.fft.fft(complex_data_hearton)
# sample rate is 62.5e6 Hz, spacing is inverse
sample_spacing = 1.9200012288007864325e-7
fourier_axis_hearton = np.fft.fftfreq(n=len(complex_data_hearton), d=sample_spacing)
# fourier filter
fourier_hearton[0] = 0



# make complex numpy array with data
complex_data_heartoff = np.empty(16000, dtype=complex)
complex_data_heartoff.real = data_heartoff[:16000]
complex_data_heartoff.imag = data_heartoff[16000:]

# compute fourier transform
fourier_heartoff = np.fft.fft(complex_data_hearton)
# sample rate is 62.5e6 Hz, spacing is inverse
sample_spacing = 1.9200012288007864325e-7
fourier_axis_heartoff = np.fft.fftfreq(n=len(complex_data_heartoff), d=sample_spacing)
# fourier filter
fourier_heartoff[0] = 0




# make complex numpy array with data
complex_diff = np.empty(16000, dtype=complex)
complex_diff.real = diff[:16000]
complex_diff.imag = diff[16000:]

# compute fourier transform
fourier_diff = np.fft.fft(complex_diff)
# sample rate is 62.5e6 Hz, spacing is inverse
sample_spacing = 1.9200012288007864325e-7
fourier_axis_diff = np.fft.fftfreq(n=len(complex_diff), d=sample_spacing)
# fourier filter
fourier_diff[0] = 0




# plot results
#plt.plot(np.fft.fftshift(fourier_axis_hearton), np.abs(np.fft.fftshift(fourier_hearton))**2, label="heart nebula on")
#plt.plot(np.fft.fftshift(fourier_axis_heartoff), np.abs(np.fft.fftshift(fourie_heartoff))**2, label="heart nebula off")
plt.plot(np.fft.fftshift(fourier_axis_diff)[2000:-2000], np.abs(np.fft.fftshift(fourier_diff)[2000:-2000])**2, label="Filtered Spectrum")

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
