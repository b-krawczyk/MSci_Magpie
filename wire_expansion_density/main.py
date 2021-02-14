import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
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

def bessel(x, k, r, beta, t):
    return (x*r*beta)**(2*k)/((np.math.factorial(k))**2*t**(4*k))

def bessel_sum(x, k_lim, r, beta, t):
    summed = 0
    for i in range(k_lim+1):
        summed += bessel(x, i, r, beta, t)
    return summed

def integral_func(x, k_lim, r, beta, t):
    return x*np.e**(-beta*x**2/t**2)*bessel_sum(x, k_lim, r, beta, t)

def integral(k_lim, r, beta, t, a):
    return quad(integral_func,0,a,args=(k_lim,r,beta,t))[0]

def total_func(k_lim, r, beta, t, a):
    return 2*beta*t**(-2)*np.e**(-beta*r**2/t**2)*integral(k_lim, r, beta, t, a)

#vec_integral = np.vectorize(integral)

#data = vec_integral(10,[1,2,3],1,1)

beta = 3.5897*10**(-8)
k_lim = 20
r = np.linspace(0,1.5*10**6,200)
t = np.linspace(1,400,200)
a = 20*10**(3)

r_len = len(r)
t_len = len(t)
"""
data = np.zeros((t_len, r_len))

for i in range(t_len):
    for j in range(r_len):
        data[i,j] = total_func(k_lim, r[j], beta, t[i], a)
    print(str(i)+"/"+str(t_len))

np.savetxt("data.csv", data, delimiter=",")
"""

data = np.genfromtxt("data.csv", delimiter=",")
#print(total_func(k_lim, 2, beta, 5, a))
#data_log = np.log(np.array(data))
fix, ax = plt.subplots()
image = ax.imshow(data,cmap="gist_heat", origin="lower",extent=[0,1.5,1,400], aspect="auto", norm=MidpointNormalize(vmin=np.min(data), vmax=np.max(data), vcenter=np.average(data)))
plt.colorbar(image, ax=ax)
plt.xlabel("r in mm")
plt.ylabel("t in ns")
plt.show()


print(data)