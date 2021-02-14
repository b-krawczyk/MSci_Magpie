import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from scipy.fft import fft, ifft ,fftfreq, fftshift, ifftshift

def sine(x, a, b, c, d):
    return a*np.sin(b*x+c) + d

files = ["003","004","005","006","007","008","009","010","011","012"]
data = []



for i in files:
    x, y = np.loadtxt("s1117_20_Shot_"+i+".csv", delimiter=",", unpack=True)
    data.append([i,x,y])

select = 1
for i in data:

    plt.subplot(5,2,select)
    plt.grid()
    #plt.plot(i[1][93:778],i[2][93:778],label=i[0])
    x = i[1][93:778]
    y = i[2][93:778]

    lim = 70

    f = fftfreq(len(x))
    y_fft = fft(y)

    f_shifted = fftshift(f)
    y_fft_shifted = fftshift(y_fft)

    y_cut = ifft(ifftshift(y_fft_shifted[int(len(y_fft_shifted)/2-lim):int(len(y_fft_shifted)/2+lim)]))
    x_new = np.array(range(len(y_cut)))*len(y)/len(y_cut)+x[0]

    #plt.figure()
    plt.plot(x_new,y_cut*len(y_cut)/len(y), label=i[0])
    plt.plot(plt.xlim(), [np.average(y_cut*len(y_cut)/len(y)),np.average(y_cut*len(y_cut)/len(y))],"--")
    plt.legend()
    plt.ylim([124,140])
    select += 1
    

#fit, cov = curve_fit(sine, data[0][1][93:778], data[0][2][93:778], p0=[5,2*np.pi/360,0,126])

#print(fit)
#print(np.sqrt(np.array(cov)))
#plt.plot(data[0][1][93:778], sine(data[0][1][93:778], *fit),"-")


"""
x = data[0][1][93:778]
y = data[0][2][93:778]

lim = 70

f = fftfreq(len(x))
y_fft = fft(y)

f_shifted = fftshift(f)
y_fft_shifted = fftshift(y_fft)

y_cut = ifft(ifftshift(y_fft_shifted[int(len(y_fft_shifted)/2-lim):int(len(y_fft_shifted)/2+lim)]))
x_new = np.array(range(len(y_cut)))*len(y)/len(y_cut)+x[0]

#plt.figure()
plt.plot(x,y)
plt.plot(x_new,y_cut*len(y_cut)/len(y), label="cut")
"""

plt.show()