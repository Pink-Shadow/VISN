import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.utils import shuffle
from sklearn import svm

digits = datasets.load_digits()
clf = svm.SVC(gamma=0.001, C=100)

len_data = len(digits.data)

data, target, images = shuffle(digits.data, digits.target, digits.images)

train_data = data[:len_data//3]
train_target = target[:len_data//3]

test_data = data[len_data//3:]
test_target = target[len_data//3:]


x,y = train_data, train_target
clf.fit(x,y)

print(clf.predict(test_data[-4:-3]))
plt.imshow(images[-4], cmap=plt.cm.gray_r, interpolation='nearest')
plt.show()