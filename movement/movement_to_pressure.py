import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


###################

fig_rgb = plt.imread("shadow_tracing.png")

fig = np.dot(fig_rgb[...,:3], [0.2989, 0.5870, 0.1140])
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
            y.append(y_num)
        x_num += 1
    x_num = 0
    y_num += 1

zipped_lists = zip(x, y)
sorted_pairs = sorted(zipped_lists)

tuples = zip(*sorted_pairs)
x, y = [ list(tuple) for tuple in  tuples]

shadow = pd.DataFrame({"x":x,"y":y})

shadow["x_avg"] = shadow["x"].rolling(3, center=True).mean()/175
shadow["y_avg"] = 15-shadow["y"].rolling(3, center=True).mean()/175
###################

data = np.genfromtxt("s1117_20_Shot_011.csv", delimiter=",", unpack=False)
pressure_array = np.genfromtxt("s1118_20_jet_density.csv")

pressure = pd.DataFrame(pressure_array, columns=["distance (mm)", "plasma density (cm^-3)"])

df = pd.DataFrame(data,columns=["x", "y"])
df["x_avg"] = df["x"].rolling(3, center=True).mean()/42.2
df["y_avg"] = df["y"].rolling(3, center=True).mean()/42.2

pressure["plasma density scaled"] = pressure["plasma density (cm^-3)"]/(0.5*10**18)
pressure["distance shifted (mm)"] = pressure["distance (mm)"] +5.9

fig, ax = plt.subplots()
ax1 = ax.twinx()
ax.set_ylabel("Position (mm)")
ax1.set_ylabel("plasma density (cm^-3)")
shadow.plot(x="x_avg", y="y_avg", ax=ax, label="Wire top edge position")
pressure.plot(x="distance shifted (mm)",y="plasma density (cm^-3)", ax=ax1, color="red", label="Plasma density")
plt.legend()
plt.grid()
plt.show()
