import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.utils import shuffle
from sklearn import svm

digits = datasets.load_digits()
clf = svm.SVC(gamma=0.001, C=100)

len_data = len(digits.data)
print(len_data)

data, target, images = shuffle(digits.data, digits.target, digits.images)

train_data = data[:len_data//3]
train_target = target[:len_data//3]

test_data = data[len_data//3:]
test_target = target[len_data//3:]

print(test_data[100])

clf.fit(train_data, train_target)

correct = 0
for i, data in enumerate(test_data):
    res = clf.predict([data])
    if res[0] == test_target[i]:
        correct += 1

print("Accuracy =", round((correct/len(test_data))*100, 2) )