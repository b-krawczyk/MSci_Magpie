import matplotlib.pyplot as plt
import scipy as sp
import scipy.fftpack as fft
from scipy.optimize import curve_fit

limit = 200

fig_rgb = plt.imread("shadow_tracing.png")

fig = sp.dot(fig_rgb[...,:3], [0.2989, 0.5870, 0.1140])
temp_x = []
temp_y = []
x = []
y = []
x_num = 0
y_num = 0

for i in fig:
    for j in i:
        if j == 0:
            x.append(x_num)
            y.append(y_num)
        x_num += 1
    x_num = 0
    y_num += 1

y_fft = fft.fft(y)
x_fft = fft.fftfreq(len(x))
#x_fft = fft.fftshift(x_fft)

y_fft[0] = 0
#y = fft.ifft(y_fft)
y_fft = fft.fftshift(y_fft)
y_fft = y_fft[int(len(y_fft)/2-limit):int(len(y_fft)/2+limit)]
x_fft = fft.fftshift(x_fft)[int(len(x_fft)/2-limit):int(len(x_fft)/2+limit)]

x_fft = fft.ifftshift(x_fft)
y_fft = fft.ifftshift(y_fft)

def sine(x, a, b, c, d):
    return a*sp.sin(b*x+c)+d

popt, pcov = curve_fit(sine, x, sp.array(y)-sp.average(y),p0=[10, 0.04, 0.2, 0])
print(popt)
print(sp.sqrt(pcov[1,1]))


y_new = fft.ifft(y_fft)
#y_new = fft.fftshift(y_new)
x_new = x[::int(len(x)/len(y_new))]

x_new = x_new[:len(y_new)]
y_new = y_new * len(x_new)/len(x)
#plt.plot(x_fft, abs(y_fft), "x")
plt.plot(x,sp.array(y)-sp.average(y),".")
plt.plot(x, sine(sp.array(x), *popt), "x")
#plt.plot(x_new,abs(y_new),".")

#plt.imshow(fig, cmap="gray")
plt.grid()
plt.show()