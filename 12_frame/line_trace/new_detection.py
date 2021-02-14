import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage as ndi

from skimage import feature

x_lim_min = 570
x_lim_max = 640
y_lim_min = 150
y_lim_max = 1020

fig_rgb = plt.imread("s1117_20_Shot_003_rotated.png")

fig = np.dot(fig_rgb[...,:3], [0.2989, 0.5870, 0.1140])
im = fig[x_lim_min:x_lim_max,y_lim_min:y_lim_max]

# Compute the Canny filter for two values of sigma
edges1 = feature.canny(im, sigma=0.5)
edges2 = feature.canny(im, sigma=3)

# display results
fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(8, 3),
                                    sharex=True, sharey=True)

ax1.imshow(im, cmap=plt.cm.gray)
ax1.axis('off')
ax1.set_title('noisy image', fontsize=20)

ax2.imshow(edges1, cmap=plt.cm.gray)
ax2.axis('off')
ax2.set_title(r'Canny filter, $\sigma=1$', fontsize=20)

ax3.imshow(edges2, cmap=plt.cm.gray)
ax3.axis('off')
ax3.set_title(r'Canny filter, $\sigma=3$', fontsize=20)

fig.tight_layout()

plt.show()