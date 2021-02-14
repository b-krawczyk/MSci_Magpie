import numpy as np
import matplotlib.pyplot as plt

data_first = [8,7,8,9,10,9]
shots_first = [7,8,9,10,11,12]

data_last = [5,6,5,10,6,7]
shots_last = [6,8,9,10,11,12]

plt.plot(shots_first,data_first,"x", label="First instability")
plt.plot(shots_last,data_last,"x", label="Last instability")

plt.legend()
plt.grid()
plt.xlabel("Shot number")
plt.ylabel("Max to min difference of instability")
plt.show()