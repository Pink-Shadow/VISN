import json
import mnist
import random
import scipy

import numpy as np
import matplotlib.pyplot as plt

from skimage import color
from skimage import io
from skimage import filters, feature

from sklearn.utils import shuffle
from sklearn import svm

from matplotlib import image

from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, AveragePooling2D
from keras.datasets import cifar10

from tensorflow.keras.utils import to_categorical    

from scripts.load_data import load_train, load_test


images = []
bunnies = []

data = None

print("start data loading... ")
with open("../../Boundary_Box/coordinates.json", 'r+') as file:
    data = json.loads(file.read())
    
    for jpg in data:
        for coords in data[jpg]:
            im = color.rgb2gray(io.imread(f"../../Boundary_Box/assets/{jpg}"))
            x_coords = [coords['begin'][0], coords['end'][0]]
            y_coords = [coords['begin'][1], coords['end'][1]]

            images.append(im)
            bunnies.append(im[ min(y_coords) : max(y_coords) , min(x_coords) : max(x_coords) ])

print("done\n")


print("start patch sampling... ")

patch_size = 20 # (N x N) pixels
patches, labels = [], []

smooth_filter = [ 
    [1/16,1/16,1/16],
    [1/16,1/5,1/16],
    [1/16,1/16,1/16]
]

for i in range(len(images)):
    im = images[i]
    bunny = bunnies[i]

    smooth_bunny=scipy.ndimage.convolve(bunny, smooth_filter)
    bunny=filters.laplace(smooth_bunny)

    smooth_image=scipy.ndimage.convolve(im, smooth_filter)
    im=filters.laplace(smooth_image)

    for j in range(50):

        # boundary box coordinates
        x_b = random.randint((patch_size//2)+1, bunny.shape[0]-(patch_size//2))
        y_b = random.randint((patch_size//2)+1, bunny.shape[1]-(patch_size//2))

        x_coords_b = [x_b-patch_size//2, x_b+patch_size//2]
        y_coords_b = [y_b-patch_size//2, y_b+patch_size//2]

        patch_b = bunny[  min(x_coords_b) : max(x_coords_b), min(y_coords_b) : max(y_coords_b) ]
        patches.append(patch_b)
        labels.append(1)
        
        ##############################################################################################################

        # outside boundary box coordinates range
        x_range = [x for x in range((patch_size//2), im.shape[0]-(patch_size//2))]
        y_range = [y for y in range((patch_size//2), im.shape[1]-(patch_size//2))]

        # remove subsection of the boundary box from the list with all coordinates
        name = list(data.keys())[i]
        y_coords_data_arrays = [data[name][0]['begin'][0], data[name][0]['end'][0]]
        x_coords_data_arrays = [data[name][0]['begin'][1], data[name][0]['end'][1]]

        del x_range[min(x_coords_data_arrays)-(patch_size//2)+1 : max(x_coords_data_arrays)+(patch_size//2)]
        del y_range[min(y_coords_data_arrays)-(patch_size//2)+1 : max(y_coords_data_arrays)+(patch_size//2)]

        #pick random coordinate
        x = random.choice(y_range)
        y = random.choice(x_range)

        x_coords = [x-patch_size//2, x+patch_size//2]
        y_coords = [y-patch_size//2, y+patch_size//2]

        patch_pic = im[ min(y_coords) : max(y_coords), min(x_coords) : max(x_coords) ]
        patches.append(patch_pic)
        labels.append(0)

print("patches created!\n")

data, label = np.array(patches), np.array(labels)

data, label = shuffle(data, label)

len_data = len(data)

train_data = data[:len_data//3 *2]
train_labels = label[:len_data//3 *2]

test_data = data[len_data//3 *2:]
test_labels = label[len_data//3 *2:]

# Normalizeren van de images
train_data = (train_data / 255) - 0.5
test_data = (test_data / 255) - 0.5

x = len(train_data[0])
y = len(train_data[0][0])

train_data2 = np.reshape(train_data, (len(train_data), x*y) )
test_data2 = np.reshape(test_data, (len(test_data), x*y) )


print("start SVM... ")
clf = svm.SVC(gamma='scale', C=1)

print("start clf.fit... ")
clf.fit(train_data2, train_labels)
print("fitting done!\n")

correct = 0
for i, data in enumerate(test_data2):
    res = clf.predict([data])
    if res[0] == test_labels[i]:
        correct += 1

print("Accuracy =", round((correct/len(test_data2))*100, 2) )