from tkinter import YView
import cv2
import numpy as np


def update_xy(dir, flag):
    x = dir[0]
    y = dir[1]

    if flag == 0:
        return x, y+1
    elif flag == 1:
        return x-1, y+1
    elif flag == 2:
        return x-1, y
    elif flag == 3:
        return x-1, y-1
    elif flag == 4:
        return x, y-1
    elif flag == 5:
        return x+1, y-1
    elif flag == 6:
        return x+1, y
    elif flag == 7:
        return x+1, y+1


img = cv2.imread(
    '/Users/zhangjiahao/Library/Mobile Documents/com~apple~CloudDocs/MyFiles/4_数字图像处理与机器视觉/Homeworks/hw4/codes/gray_img.jpg', 0)
blur = cv2.GaussianBlur(img, (5, 5), 0)

# find normalized_histogram, and its cumulative distribution function
hist = cv2.calcHist([blur], [0], None, [256], [0, 256])
hist_norm = hist.ravel()/hist.sum()
Q = hist_norm.cumsum()
bins = np.arange(256)
fn_min = np.inf
thresh = -1
for i in range(1, 256):
    p1, p2 = np.hsplit(hist_norm, [i])  # probabilities
    q1, q2 = Q[i], Q[255]-Q[i]  # cum sum of classes
    if q1 < 1.e-6 or q2 < 1.e-6:
        continue
    b1, b2 = np.hsplit(bins, [i])  # weights
    # finding means and variances
    m1, m2 = np.sum(p1*b1)/q1, np.sum(p2*b2)/q2
    v1, v2 = np.sum(((b1-m1)**2)*p1)/q1, np.sum(((b2-m2)**2)*p2)/q2
    # calculates the minimization function
    fn = v1*q1 + v2*q2
    if fn < fn_min:
        fn_min = fn
        thresh = i
# find otsu's threshold value with OpenCV function
ret, otsu = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
# print("{} {}".format(thresh, ret))

result_img = img.copy()
for x in range(0, img.shape[0]):
    for y in range(0, img.shape[1]):
        if result_img[x][y] < thresh:
            result_img[x][y] = 0
        else:
            result_img[x][y] = 255

# cv2.imshow("res", result_img)
# cv2.imwrite("result_img.jpg", result_img)
# cv2.waitKey(0)
# get shape

dirs = []
flag = 0
for x in range(0, result_img.shape[0]):
    for y in range(0, result_img.shape[1]):
        if result_img[x][y] == 0:
            flag = 1
            break
    if flag:
        break
dirs.append([x, y, 5])
print([x, y, 5])
i = 0
flag = dirs[i][2]

while(1):
    x_new, y_new = update_xy(dirs[i], flag)
    res = result_img[x_new, y_new]
    if res == 0 and np.sum(result_img[x_new-1:x_new+2, y_new-1:y_new+2]) >= 255:
        break
    flag = (flag + 1) % 8

i = i + 1
dirs.append([x_new, y_new, flag])

while(1):
    # while(i < 50):
    print("i = ", i)
    flag_0 = dirs[i][2]
    if flag_0 % 2 == 0:
        flag = (flag_0 + 7) % 8
    else:
        flag = (flag_0 + 6) % 8
    while(1):
        x_new, y_new = update_xy(dirs[i], flag)
        res = result_img[x_new, y_new]
        if res == 0 and np.sum(result_img[x_new-1:x_new+2, y_new-1:y_new+2]) >= 255:
            break
        flag = (flag + 1) % 8
    dirs.append([x_new, y_new, flag])
    print("Final: ", x_new, y_new, flag)
    i = i + 1
    if x_new == dirs[0][0] and y_new == dirs[0][1]:
        break
img_1 = img.copy()
for x in range(0, result_img.shape[0]):
    for y in range(0, result_img.shape[1]):
        img_1[x][y] = 255
for k in range(0, 410):
    print(dirs[k][2], end=" ")
    img_1[dirs[k][0]][dirs[k][1]] = 0
cv2.imshow("result", img_1)
cv2.waitKey(0)
