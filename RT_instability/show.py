import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy.signal import find_peaks

layers = [3,6,8,10,12]
fig_lst = []
points = []

for i in layers:
    filename = "shot_"+str(i)+"_trace_top.png"
    fig_lst.append(np.dot(plt.imread(filename)[...,:3], [0.2989, 0.5870, 0.1140]))

print(np.shape(fig_lst[0]))

temp_x = []
temp_y = []
x = []
y = []
x_num = 0
y_num = 0

for fig in fig_lst:
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
                y.append(np.shape(fig_lst[0])[0]-y_num)
            x_num += 1
        x_num = 0
        y_num += 1
    points.append([x,y])

temp_num = 1

for i in points:
    avg = np.average(i[1])
    print(avg)

    zipped_lists = zip(i[0], np.array(i[1]))#-avg)
    sorted_pairs = sorted(zipped_lists)
    tuples = zip(*sorted_pairs)
    x, y = [ list(tuple) for tuple in  tuples]

    #peaks, _ = find_peaks(y)
    #print(peaks)

    #plt.plot(np.array(x)[peaks], np.array(y)[peaks], "x")
    plt.plot(x,y, "-", color=[1/len(layers)*temp_num, 0.1, 0.1], label=layers[temp_num-1])

    temp_num += 1

plt.title("Deviation from average")
plt.legend()
plt.grid()
plt.show()