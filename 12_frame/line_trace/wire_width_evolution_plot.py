import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

frames = ["002","003","004","005","006","007","008","009","010","011","012"]

for i in frames:
    filename = "s1117_20_Shot_" + i

    top = pd.read_csv(filename+".csv", names=["x", "y"], )
    bottom = pd.read_csv(filename+"_bottom.csv", names=["x", "y"])
    image_rgb = plt.imread(filename+"_rotated.png")
    image = np.dot(image_rgb[...,:3], [0.2989, 0.5870, 0.1140])

    fig, (ax1) = plt.subplots()

    top["y_avg"] = top["y"].rolling(3, center=True).mean() / 42.2
    bottom["y_avg"] = bottom["y"].rolling(3, center=True).mean() / 42.2


    ax1.imshow(image, cmap="gray", aspect="auto")
    ax1.set_ylabel("index from top")
    ax3 = ax1.twinx()
    top[93:778].plot(x="x", y="y_avg", ax=ax3, label="top")
    bottom[93:778].plot(x="x", y="y_avg", ax=ax3, label="bottom")
    ax3.set_ylim(0,len(image)/42.2)
    ax3.set_ylabel("Distance from bottom in mm")
    plt.title("Frame " + i)
    plt.tight_layout()
    plt.savefig("traced/"+filename+"_traced.png", dpi=300)
    #plt.show()