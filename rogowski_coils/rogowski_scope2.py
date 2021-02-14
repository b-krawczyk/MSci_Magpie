import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.fftpack import fft, ifft, fftshift, fftfreq, ifftshift
import scipy.integrate as integrate

t,a,b,c,d,e,f,g,h = np.genfromtxt("Scope2.csv", delimiter=",", unpack=True)

fig1, (ax1, ax2, ax3) = plt.subplots(nrows=3, sharex=True)

ax1.grid()
ax1.plot(t[3500:5000], f[3500:5000])
ax1.plot(t[3500:5000], e[3500:5000])
ax1.set(ylabel="Rog Signal in V")
ax1.set(title="Main Return Post")


ax2.grid()
data_new = (-f[3500:5000]+e[3500:5000])/2
ax2.plot(t[3500:5000], data_new)
ax2.set(ylabel="Avg Rog Signal in V")


ax3.grid()
temp = 0
num = 3500
data_integrated = []
for i in data_new:
    temp += i*(t[num+1]-t[num])/1000000000*2.9966*10**9*8*170
    data_integrated.append(temp)
    num += 1

ax3.plot(t[3500:5000], np.array(data_integrated)/1000000)

plt.xlabel("time in ns")
ax3.set(ylabel="Current in MA")


#-------------------------------------------------


fig2, (ax4, ax5, ax6) = plt.subplots(nrows=3, sharex=True)

filter_limit = 200

f_fft = fft(f[3500:5000])
e_fft = fft(e[3500:5000])

f_filt_fft = ifftshift(fftshift(f_fft)[int(len(f_fft)/2)-filter_limit: int(len(f_fft)/2)+filter_limit])
f_filt = ifft(f_filt_fft)

e_filt_fft = ifftshift(fftshift(e_fft)[int(len(e_fft)/2)-filter_limit: int(len(e_fft)/2)+filter_limit])
e_filt = ifft(e_filt_fft)

freq = fftfreq(len(t[3500:5000]), t[3501]-t[3500])
freq_filt = ifftshift(fftshift(freq)[int(len(f_fft)/2)-filter_limit: int(len(f_fft)/2)+filter_limit])

t_new = np.linspace(t[3500],t[5000-1],len(e_filt))

f_filt = f_filt / len(t[3500:5000])*len(t_new)
e_filt = e_filt / len(t[3500:5000])*len(t_new)

ax4.grid()
ax4.plot(t_new, np.real(f_filt), "-")
ax4.plot(t_new, np.real(e_filt), "-")
ax4.set(ylabel="Rog Signal in V")
ax4.set(title="Main Return Post with FFT")


ax5.grid()
data_new = (-f_filt+e_filt)/2
ax5.plot(t_new, data_new)
#ax5.plot(t[3500:5000], (np.array(e[3500:5000])-np.array(f[3500:5000]))/2)
ax5.set(ylabel="Avg Rog Signal in V")


ax6.grid()
temp = 0
data_integrated = []
"""
for i in data_new:
    temp += i*(t_new[1]-t_new[0])/1000000000*3*10**9*800
    data_integrated.append(temp)
    print(temp)
"""
data_integrated.append(data_new[0])
for i in range(1,len(t_new)):
    temp = integrate.simps(data_new[:i],np.array(t_new[:i])/1000000000)*3*10**9*8*170
    data_integrated.append(temp)

'''temp = 0
num = 3500
data_integrated_non = []
for i in (np.array(e[3500:5000])-np.array(f[3500:5000]))/2:
    temp += i*(t[3501]-t[3500])/1000000*3*10**9*800
    data_integrated_non.append(temp)
    num += 1'''

ax6.plot(t_new, np.abs(np.array(data_integrated))/1000000)
#ax6.plot(t[3500:5000], data_integrated_non)

plt.xlabel("time in ns")
ax6.set(ylabel="Current in MA")

print(np.abs(sum(data_new))*len(t_new)*(t_new[1]-t_new[0])/1000000000*3*10**9*8*170)
print(sum((np.array(e[3500:5000])-np.array(f[3500:5000]))/2)*len(t[3500:5000])*(t[3501]-t[3500])/1000000000*3*10**9*8*170)
print(len(t_new))
print(len(t[3500:5000]))

plt.show()