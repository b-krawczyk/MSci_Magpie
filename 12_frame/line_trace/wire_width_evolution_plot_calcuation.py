import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

frames = ["002","003","004","005","006","007","008","009","010","011","012"]
avg_list = []
std_list = []

for i in frames:
    filename = "s1117_20_Shot_" + i

    top = pd.read_csv(filename+".csv", names=["x", "y"], )
    bottom = pd.read_csv(filename+"_bottom.csv", names=["x", "y"])
    image_rgb = plt.imread(filename+"_rotated.png")
    image = np.dot(image_rgb[...,:3], [0.2989, 0.5870, 0.1140])

    top["y_avg"] = top["y"].rolling(3, center=True).mean() / 42.2
    bottom["y_avg"] = bottom["y"].rolling(3, center=True).mean() / 42.2

    bottom["dist"] = top["y_avg"] - bottom["y_avg"]
    bottom["x_scaled"] = bottom["x"]/42.2

    if i == "002":
        bottom["dist filtered"] = bottom[bottom["dist"]<0.28]["dist"]
    elif i == "003":
        bottom["dist filtered"] = bottom[bottom["dist"]>0.2]["dist"]
        bottom["dist filtered"] = bottom[bottom["dist filtered"]<0.6]["dist filtered"]
    elif i == "004":
        bottom["dist filtered"] = bottom[bottom["dist"]>0.2]["dist"]
    elif i == "005":
        bottom["dist filtered"] = bottom[bottom["dist"]>0.3]["dist"]
    elif i == "006":
        bottom["dist filtered"] = bottom[bottom["dist"]>0.3]["dist"]
    elif i == "007":
        bottom["dist filtered"] = bottom[bottom["dist"]>0.25]["dist"]
    elif i == "008":
        bottom["dist filtered"] = bottom[bottom["dist"]>0.2]["dist"]
    elif i == "009":
        bottom["dist filtered"] = bottom[bottom["dist"]>0.25]["dist"]
    elif i == "010":
        bottom["dist filtered"] = bottom[bottom["dist"]>0.2]["dist"]
    elif i == "011":
        bottom["dist filtered"] = bottom[bottom["dist"]>0.25]["dist"]
    elif i == "012":
        bottom["dist filtered"] = bottom[bottom["dist"]>0.25]["dist"]
    
    avg = bottom["dist filtered"].mean()
    std = bottom["dist filtered"].std()
    print(i +" avg: "+ str(avg))
    print(i +" std: "+ str(std))

    fig, (ax1, ax2) = plt.subplots(1,2,sharey=True)

    bottom[93:778].plot(x="x_scaled", y="dist", ax=ax1)
    ax1.set_title("top - bottom Frame "+i)
    ax1.grid()
    plt.tight_layout()
    ax1.set_xlabel("Distance from left edge (mm)")
    ax1.set_ylabel("Wire width (mm)")
    ax2.hist(bottom["dist"][93:778],orientation="horizontal",bins=25)
    ax2.set_xlabel("Number of points in bin")
    ax2.set_title("Diameter: "+str(np.round(avg, 3))+"+-"+str(np.round(std, 3))+" mm")
    plt.axhline(avg, color="red", ls="--", alpha=0.7)
    plt.axhline(avg-std, color="orange", ls="--", alpha=0.7)
    plt.axhline(avg+std, color="orange", ls="--", alpha=0.7)
    #plt.savefig("wire_width/"+filename+"_traced.png", dpi=300)
    avg_list.append(avg)
    std_list.append(std)
    #plt.show()

fig, ax = plt.subplots()
x = [int(i) for i in frames]
ax.errorbar(x, avg_list, std_list, fmt="x")
ax.grid()
ax.set_title("Wire diameter at given frame")
ax.set_xlabel("Frame")
ax.set_ylabel("Wire diameter (mm)")
plt.show()