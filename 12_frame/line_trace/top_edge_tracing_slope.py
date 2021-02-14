import matplotlib.pyplot as plt
import numpy as np
import scipy.fftpack as fft
from scipy.optimize import curve_fit

limit = 200

fig_rgb = plt.imread("s1117_20_Shot_012_rotated.png")

fig = np.dot(fig_rgb[...,:3], [0.2989, 0.5870, 0.1140])

fig_cut = fig[560:650,150:1020]
max_jump = []
temp_ar = np.zeros(np.shape(fig_cut))
for col_num in range(len(fig_cut[0])):
    temp = []
    for row_num in range(4,len(fig_cut)):
        try:
            #temp.append(1/280*fig_cut[row_num-4][col_num]-4/105*fig_cut[row_num-3][col_num]+0.2*fig_cut[row_num-2][col_num]-4/5*fig_cut[row_num-1][col_num]+4/5*fig_cut[row_num+1][col_num]-0.2*fig_cut[row_num+2][col_num]+4/105*fig_cut[row_num+3][col_num]-1/280*fig_cut[row_num+4][col_num])
            #temp.append(fig_cut[row_num+1][col_num]-fig_cut[row_num-1][col_num])
            temp_ar[row_num][col_num] = 1/280*fig_cut[row_num-4][col_num]-4/105*fig_cut[row_num-3][col_num]+0.2*fig_cut[row_num-2][col_num]-4/5*fig_cut[row_num-1][col_num]+4/5*fig_cut[row_num+1][col_num]-0.2*fig_cut[row_num+2][col_num]+4/105*fig_cut[row_num+3][col_num]-1/280*fig_cut[row_num+4][col_num]
            #temp_ar[row_num][col_num] = fig_cut[row_num+1][col_num]-fig_cut[row_num-1][col_num]

        except:
            #temp.append(0)
            temp_ar[row_num][col_num] = 0
    #max_jump.append(temp.index(min(temp)))

for i in range(len(temp_ar[0])):
    temp = []
    for j in temp_ar:
        temp.append(j[i])
    max_jump.append(temp.index(max(temp)))

x = range(len(max_jump))
print(x)
#plt.figure()

max_jump_fft = fft.fft(max_jump[90:800])
f = fft.fftfreq(len(max_jump_fft))
plt.figure()
plt.plot(f,max_jump_fft, "x")

plt.figure()
plt.imshow(temp_ar)
plt.plot(x[90:800], max_jump[90:800], color = "white")

plt.figure()
plt.imshow(fig_cut)
plt.plot(x, max_jump, color = "white")
plt.show()