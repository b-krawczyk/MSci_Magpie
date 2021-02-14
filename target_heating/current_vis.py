import numpy as np
import matplotlib.pyplot as plt

data = np.genfromtxt("target_current.csv", delimiter=",")

plt.plot(np.array(data[0]), data[1], "x")
plt.show()