from skimage import transform, io, data
from skimage.viewer import ImageViewer
import matplotlib.pyplot as plt
import numpy as np

image = data.camera()
rot, translate, stretch = 10, 100, 30

rotation    = transform.AffineTransform(rotation=np.deg2rad(rot))
translation = transform.AffineTransform(translation=translate)
stretched   = transform.AffineTransform(shear=np.deg2rad(stretch))

rotated     = transform.warp(image, rotation)
translated  = transform.warp(image, translation)
stretched   = transform.warp(image, stretched)


image_titles = ["Original", f"Rotated {rot} degrees.", f"translated {translate} pixels.", f"stretched {stretch} degrees."]
image_names = [image, rotated, translated, stretched]

fig, ax = plt.subplots(1, 4, figsize=(12, 8))

for i, title in enumerate(image_titles):
    ax[i].imshow(image_names[i], cmap='gray')
    ax[i].set_title(title)
    ax[i].axis('off')

plt.tight_layout(pad=0.5)
plt.subplots_adjust(hspace=0.166)


plt.show()