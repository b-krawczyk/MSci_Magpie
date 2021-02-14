import matplotlib.pyplot as plt
import numpy as np
import scipy.fftpack as fft
from scipy.optimize import curve_fit

filename = "s1117_20_Shot_008"
x_lim_min = 592
x_lim_max = 630
y_lim_min = 150
y_lim_max = 1020

fig_rgb = plt.imread(filename+"_rotated.png")

fig = np.dot(fig_rgb[...,:3], [0.2989, 0.5870, 0.1140])

fig_cut = fig[x_lim_min:x_lim_max,y_lim_min:y_lim_max]
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

fig_new = fig_cut.copy()

colour_threshold = (np.average(fig_new)+np.min(fig_new))*1.4
growth_threshold = np.min(temp_ar)*0.1

for col_num in range(len(temp_ar[0])):
    for row_num in range(len(temp_ar)):
        if temp_ar[row_num][col_num] > growth_threshold:
            fig_new[row_num][col_num] = 2

fig_new = abs(np.array(fig_new)-colour_threshold)

for i in range(len(fig_new[0])):
    temp = []
    for j in fig_new:
        temp.append(j[i])
    max_jump.append(temp.index(min(temp)))

x = range(len(max_jump))
print(x)
#plt.figure()

data = [[np.array(x[i]) + y_lim_min, len(fig) - x_lim_min - np.array(max_jump[i])] for i in range(len(x))]

np.savetxt(filename+"_bottom.csv", data, delimiter=",")

fig, (ax1, ax2, ax3) = plt.subplots(3,1,sharex=True)

#ax1.title("test")

ax1.title.set_text("Figure cut around the wire for "+filename)
ax1.imshow(fig_cut, cmap="gray")
ax1.plot(x, max_jump, color = "white")

ax2.title.set_text("Derivative at given point")
ax2.imshow(temp_ar)
ax2.plot(x, max_jump, color = "white")

ax3.title.set_text("Points with accepted derivative and subtracted searched value")
ax3.imshow(fig_new)
ax3.plot(x, max_jump, color = "white")


plt.show()