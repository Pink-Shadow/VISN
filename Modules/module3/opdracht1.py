from skimage import data, filters
from skimage.viewer import ImageViewer
import scipy
from scipy import ndimage
import matplotlib.pyplot as plt

smooth_mean=[ [1/9,1/9,1/9],
              [1/9,1/9,1/9],
              [1/9,1/9,1/9]]

############################
edge1 = [[-1, -1, -1],
         [0, 0, 0],
         [1, 1, 1]]

edge2 = [[-1, 0, 1],
         [-1, 0, 1],
         [-1, 0, 1]]

laplacian=[ [0.5,1,0.5],
            [1,-6,1],
            [0.5,1,0.5]]
############################

image = data.camera()

edgeIMG1=scipy.ndimage.convolve(image, edge1)

edgeIMG2=scipy.ndimage.convolve(image, edge2)

smoothIMG=scipy.ndimage.convolve(image, smooth_mean)
laplacian=scipy.ndimage.convolve(smoothIMG, laplacian)
laplacian += 127

fig, ax = plt.subplots(2, 2, figsize=(10, 8))

ax[0,0].imshow(image, cmap='gray')
ax[0,0].set_title("Original")

ax[0,1].imshow(edgeIMG1, cmap='gray')
ax[0,1].set_title("edge x axis")

ax[1,0].imshow(edgeIMG2, cmap='gray')
ax[1,0].set_title("edge y axis")

ax[1,1].imshow(laplacian, cmap='gray')
ax[1,1].set_title("laplacian")


for a in ax:
    for b in a:
        b.axis('off')
plt.tight_layout()
plt.show()