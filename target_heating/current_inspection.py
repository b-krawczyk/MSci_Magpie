import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as sp

def get_integral(temp, res, T_end, T_start=300, jump=8,T_jump=830, n=1000):
    temp_start = temp[:jump]
    res_start = res[:jump]
    temp_end = temp[jump:]
    res_end = res[jump:]

    fit_start = np.polyfit(temp_start, res_start, 1)
    fit_end = np.polyfit(temp_end, res_end, 1)

    temp_interpolated = np.linspace(T_start, T_end, n)
    res_interpolated = []

    for i in temp_interpolated:
        if i < T_jump:
            temp = fit_start[0]*i + fit_start[1]
            res_interpolated.append(temp)
        else:
            temp = fit_end[0]*i + fit_end[1]
            res_interpolated.append(temp)
    
    conductivity = [1/i for i in res_interpolated]

    integrand = []

    for i in range(len(temp_interpolated)):
        temp = 4690036/conductivity[i]*10**(-5) + 5036880202/conductivity[i]*(np.exp(23.1*10**(-6)*(temp_interpolated[i] - T_start))-1)* np.exp(2*23.1*10**(-6)*(temp_interpolated[i] - T_start))
        integrand.append(temp)

    integral = np.trapz(integrand, temp_interpolated)*10**(-13)

    return integral


temp, res = np.genfromtxt("Al_resistivity.csv", delimiter=",", unpack=True)

data = np.genfromtxt("target_current.csv", delimiter=",")

time = np.array(data[0]) - data[0][0]
current = np.array(data[1])

temperature = np.linspace(300, 4500, 1000)
integral = [get_integral(temp, res, i) for i in temperature]

current_squared = current**2

current_squared_integrated = []
temp = 0
for i in range(len(current_squared)):
    current_squared_integrated.append(np.trapz(current_squared[:i], time[:i])*10**(-9))

#line = 41323.42503979442
"""
1.5672853068471462
41323.42503979442
"""
#plt.plot(time[:100], current_squared_integrated[:100], "x")
#plt.axhline(y=line)
T_func = []

for line in integral:
    print(line)

    close = [abs(i - line) for i in current_squared_integrated]
    #print(close)
    index = close.index(np.min(close))
    #print(index)
    t_line = time[index]
    #print(t_line)

    T_func.append(t_line + data[0][0])


temp_dict = dict(zip(T_func, temperature))
plt.plot(temp_dict.keys(), temp_dict.values(), "x")
print(temp_dict)

plt.grid()
plt.xlabel("time since current start (ns)")
plt.ylabel("Wire temperature (K)")
#plt.ylim(0,2)
plt.show()
