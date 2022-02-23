from skimage import data, filters
from skimage.viewer import ImageViewer
from skimage import filters
from skimage import feature
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
edgeIMG1 += 127

edgeIMG2=scipy.ndimage.convolve(image, edge2)
edgeIMG2 += 127

smoothIMG=scipy.ndimage.convolve(image, smooth_mean)
laplacian=scipy.ndimage.convolve(smoothIMG, laplacian)
laplacian += 127

fig, ax = plt.subplots(3, 4, figsize=(12, 8))

ax[0,0].imshow(image, cmap='gray')
ax[0,0].set_title("Original, self made filters >>>")

ax[0,1].imshow(edgeIMG1, cmap='gray')
ax[0,1].set_title("edge x axis")

ax[0,2].imshow(edgeIMG2, cmap='gray')
ax[0,2].set_title("edge y axis")

ax[0,3].imshow(laplacian, cmap='gray')
ax[0,3].set_title("laplacian")

#################################

ax[1,0].imshow(image, cmap='gray')
ax[1,0].set_title("Original, standard filters >>>")

a = filters.roberts_neg_diag(image)
b = filters.roberts_pos_diag(image)

ax[1,1].imshow((a+b), cmap='gray')
ax[1,1].set_title("roberts")

a = filters.prewitt_h(image)
b = filters.prewitt_v(image)

ax[1,2].imshow((a+b), cmap='gray')
ax[1,2].set_title("prewitt")

a = filters.farid_h(image)
b = filters.farid_v(image)

ax[1,3].imshow((a+b), cmap='gray')
ax[1,3].set_title("farid")


#################################

ax[2,0].imshow(image, cmap='gray')
ax[2,0].set_title("Original, canny filters >>>")

ax[2,1].imshow(feature.canny(image, sigma=1), cmap='gray')
ax[2,1].set_title("canny sigma 1")

ax[2,2].imshow(feature.canny(image, sigma=3), cmap='gray')
ax[2,2].set_title("canny sigma 3")

ax[2,3].imshow(feature.canny(image, sigma=2, low_threshold=40, high_threshold=120), cmap='gray')
ax[2,3].set_title("canny sigma 2. lowT=40, highT=120")


for a in ax:
    for b in a:
        b.axis('off')

plt.tight_layout(pad=0.5)
plt.subplots_adjust(hspace=0.166)

plt.show()
