import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from scipy.fft import fft, ifft ,fftfreq, fftshift, ifftshift
import matplotlib.colors as colors

class MidpointNormalize(colors.Normalize):
    def __init__(self, vmin=None, vmax=None, vcenter=None, clip=False):
        self.vcenter = vcenter
        colors.Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        # I'm ignoring masked values and all kinds of edge cases to make a
        # simple example...
        x, y = [self.vmin, self.vcenter, self.vmax], [0, 0.5, 1]
        return np.ma.masked_array(np.interp(value, x, y))

def sine(x, a, b, c, d):
    return a*np.sin(b*x+c) + d

files = ["003","004","005","006","007","008","009","010","011","012"]
data = []



for i in files:
    x, y = np.loadtxt("s1117_20_Shot_"+i+".csv", delimiter=",", unpack=True)
    data.append([x[93:777],y[93:777]])

data_averaged =[]
data_std = []

#data = [[[0],[1,2,3,4,5,6]],[[0],[9,8,7,6,5,4]],[[0],[4,5,6,7,8]]]

for j in range(len(data)):
    temp = []
    temp_std = []
    #data_averaged.append([np.average(data[j][0][a:a+3]) for a in range(len(data))[::3]])
    for i in range(0,len(data[j][1]),3):
        temp.append(np.average(data[j][1][i:i+3]))
        temp_std.append(np.std(data[j][1][i:i+3]))

    data_averaged.append(temp)
    data_std.append(temp_std)


diff = []
for i in range(len(data_averaged)-1):
    diff.append(np.array(data_averaged[i+1])-np.array(data_averaged[i]))

travel = [data_averaged[-1][i]-data_averaged[0][i] for i in range(len(data_averaged[0]))]
travel_min = travel.index(min(travel))
travel_max = travel.index(max(travel))
travel_abs = [abs(i) for i in travel]
travel_0 = travel_abs.index(min(travel_abs))

print("max_backwards", travel_min)
print("max_forwards", travel_max)
print("0", travel_0)

temp_min = []
temp_max = []
temp_0 = []
for j in data_averaged:
    temp_min.append(j[travel_min]*3/42.2)
    temp_max.append(j[travel_max]*3/42.2)
    temp_0.append(j[travel_0]*3/42.2)

x = [3,4,5,6,7,8,9,10,11,12]
plt.plot(x, temp_min, label="max backwards, 155")
plt.plot(x, temp_max, label="max forwards, 181")
plt.plot(x, temp_0, label="min movement, 12")
plt.xlabel("Frame")
plt.ylabel("Position in mm")
plt.legend()
plt.grid()
plt.show()

"""
plt.subplot(3,1,1)
plt.imshow(data_averaged)
plt.title("Darker means further back")
plt.xlabel("Index")
plt.ylabel("Frame, starting at 3")

vmin = np.min(diff)
vmax = np.max(diff)

plt.subplot(3,1,2)
plt.imshow(diff, cmap="seismic", norm=MidpointNormalize(vmin=vmin, vmax=vmax, vcenter=0))
plt.colorbar(orientation='horizontal')
plt.title("Position change between frames")
plt.xlabel("Index")
plt.ylabel("From frame, starting at 3")

plt.subplot(3,1,3)


data11 = np.array(data_averaged[7])*3/42.2
x11 = np.array(range(len(data11)))*3/42.2

fit, cov = curve_fit(sine, x11, data11, p0 = [5,2,10,200])

travel = np.array(data_averaged[-1])-np.array(data_averaged[0])
travel_std = [np.sqrt(data_std[-1][i]**2 + data_std[0][i]**2) for i in range(len(data_averaged[-1]))]
#plt.errorbar(range(len(data_averaged[0])),data_averaged[0],data_std[0],label= "2")
#plt.errorbar(range(len(data_averaged[0])),data_averaged[-1],data_std[-1],label= "12")
plt.errorbar(np.array(range(len(travel)))*3/42.2,travel, travel_std, fmt="none", color = "red", elinewidth=1)
plt.plot(np.array(range(len(travel)))*3/42.2,travel, color="black")
plt.ylabel("Total position change in pixels")
plt.xlabel("Along the wire in mm")

plt.plot(x11, data11)
plt.plot(x11,sine(x11, *fit), color="orange")

#plt.title("Position of frame 12 - frame 3")
plt.ylabel("Total position change")
plt.xlabel("Along the wire in mm")
plt.grid()
#plt.legend()
plt.xlim([0,range(len(travel))[-1]*3/42.2])
print(fit)

plt.xlim([0,range(len(travel))[-1]*3/42.2])
plt.grid()
plt.show()
"""

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