import matplotlib.pyplot as plt
import numpy as np

def get_trace(image, scale):
    fig = np.dot(image[...,:3], [0.2989, 0.5870, 0.1140])

    x = []
    y = []
    x_num = 0
    y_num = 0

    for i in fig[::-1]:
        for j in i:
            if j == 0:
                x.append(x_num)
                y.append(y_num)
            x_num += 1
        x_num = 0
        y_num += 1
    
    zipped_lists = zip(x, y)
    sorted_pairs = sorted(zipped_lists)

    tuples = zip(*sorted_pairs)
    x, y = [ list(tuple) for tuple in  tuples]

    return [x, y]

def get_difference(line1, line2):
    if line1[0][0] >= line2[0][0]:
        start = line1[0][0] - line2[0][0]
        end = start + len(line1[0])
        #plt.plot(line1[0], line2[1][start:end])
        return [line1[0], np.array(line1[1]) - np.array(line2[1][start:end])]
    else:
        print("Wrong order")


shot_top = plt.imread("shot_top.png")
shot_top_trace = get_trace(shot_top, 175)

background_top = plt.imread("background_top.png")
background_top_trace = get_trace(background_top, 175)



shot_bottom = plt.imread("shot_bottom.png")
shot_bottom_trace = get_trace(shot_bottom, 175)

background_bottom = plt.imread("background_bottom.png")
background_bottom_trace = get_trace(background_bottom, 175)



plt.plot(np.array(shot_top_trace[0])/175, np.array(shot_top_trace[1])/175)
plt.plot(np.array(background_top_trace[0])/175, np.array(background_top_trace[1])/175)

plt.plot(np.array(shot_bottom_trace[0])/175, np.array(shot_bottom_trace[1])/175)
plt.plot(np.array(background_bottom_trace[0])/175, np.array(background_bottom_trace[1])/175)

plt.grid()


fig, ax = plt.subplots()
diff = get_difference(shot_top_trace, background_top_trace)
diff_b = get_difference(shot_bottom_trace, background_bottom_trace)

ax.plot(np.array(diff[0])/175, np.array(diff[1])/175, label="Top distance")
ax.plot(np.array(diff_b[0])/175, np.array(diff_b[1])/175, label="Bottom distance")

plt.legend()
plt.grid()
plt.show()