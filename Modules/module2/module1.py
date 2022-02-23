import os
import copy
import numpy as np
import matplotlib.pyplot as plt
from winreg import HKEY_PERFORMANCE_DATA
import skimage
from skimage.viewer import ImageViewer
import random

fire_changed_rgb = skimage.io.imread('house_fire.jpg')
fire_hsv = skimage.color.rgb2hsv(fire_changed_rgb)

for col in range(0, fire_hsv.shape[0]):
    for row in range(0, fire_hsv.shape[1]):
        h = fire_hsv[col][row][0]
        s = fire_hsv[col][row][1]
        v = fire_hsv[col][row][2]

        if not ( (0.13 < (h) < 0.16) and ( 0.01 < (s) < 0.95) and (0.7 <= (v) <= 1) ):
            fire_changed_rgb[col][row] = (int(fire_changed_rgb[col][row][0])+int(fire_changed_rgb[col][row][1])+int(fire_changed_rgb[col][row][2]))/3


original_hsv = fire_hsv
changed_hsv  = skimage.color.rgb2hsv(fire_changed_rgb)

lst_normal  = []
lst_changed = []

for col in range(0, original_hsv.shape[0]):
    for row in range(0, original_hsv.shape[1]):
        lst_normal.append(original_hsv[col][row][0])

for col in range(0, changed_hsv.shape[0]):
    for row in range(0, changed_hsv.shape[1]):
        lst_changed.append(changed_hsv[col][row][0])

fig, axs = plt.subplots(2, 2, figsize=(10, 5))

original = skimage.color.hsv2rgb(original_hsv)
changed  = skimage.color.hsv2rgb(changed_hsv)

axs[0,0].hist(np.array(lst_normal), 100, facecolor='blue', alpha=0.5)
axs[0,1].imshow(original)
axs[1,0].hist(np.array(lst_changed), 100, facecolor='red', alpha=0.5)
axs[1,1].imshow(changed)

plt.show()
