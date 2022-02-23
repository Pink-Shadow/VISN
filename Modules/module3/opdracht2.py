from skimage import data, filters
from skimage.viewer import ImageViewer
from skimage import filters
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

fig, ax = plt.subplots(2, 4, figsize=(12, 8))

ax[0,0].imshow(image, cmap='gray')
ax[0,0].set_title("self made filters >>>\n\nOriginal")

ax[0,1].imshow(edgeIMG1, cmap='gray')
ax[0,1].set_title("edge x axis")

ax[0,2].imshow(edgeIMG2, cmap='gray')
ax[0,2].set_title("edge y axis")

ax[0,3].imshow(laplacian, cmap='gray')
ax[0,3].set_title("laplacian")

#################################

ax[1,0].imshow(image, cmap='gray')
ax[1,0].set_title("standard filters >>>\n\nOriginal")

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


''' 
    Wat valt me op:
    ~~~~~~~~~~~~~~~~~~~

    Wat me opvalt is dat de standaard filters allemaal (zover ik heb getest)
    een soort ruisreductie eroverheen halen. dit kun je goed zien aan dat de 1e en 2e filter van mijzelf geen ruisreductie toepast
    hier zie je duidelijk dan ruis in het resultaat. iets wat je niet terug ziet in de standaard filters.

    Ook valt me op dat bij de farid en prewitt filters er een verschil zit tussen hoe intens de outlines zijn. die van prewitt is scherper dan die van farid.
    ik weet alleen niet waardoor dit zou komen aangezien ik niet kan vinden welke mask farid gebruikt.

    Tot slot valt me op dat de roberts filter geen verticale lijnen kan detecteren. Dit komt natuurlijk doordat de filters [-1, 0] en [0, -1] worden gebruikt.
                                                                                                                           [ 0, 1]    [1,  0]
    hierdoor worden alleen verandereingen diagonaal gedetecteerd, en dus worden verticale lijnen niet gedetecteerd.
'''

for a in ax:
    for b in a:
        b.axis('off')
plt.tight_layout()
plt.show()
