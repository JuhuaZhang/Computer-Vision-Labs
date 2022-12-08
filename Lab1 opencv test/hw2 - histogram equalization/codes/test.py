import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

img = cv.imread("./GrayImg.jpg", 0)

# calculate hist
hist, bins = np.histogram(img, 256)
# plt.plot(hist, 'b')
# print(sum)
s = np.zeros(256)

sum = 0

for i in range(0, 255):
    sum += hist[i]

s[0] = hist[0]/sum

for i in range(1, 255):
    s[i] = s[i-1] + hist[i]/sum
    # print(p[i])

for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        img[i][j] = int(255 * s[img[i][j]] + 0.5)
# calculate hist
hist, bins = np.histogram(img, 256)
# plot hist
plt.plot(hist, 'r')
plt.show()
# cv.imshow("img", img)
cv.waitKey()
