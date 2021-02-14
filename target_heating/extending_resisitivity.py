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

integral = get_integral(temp, res, 2800)
print(integral)
integral = get_integral(temp, res, 45000)
print(integral)