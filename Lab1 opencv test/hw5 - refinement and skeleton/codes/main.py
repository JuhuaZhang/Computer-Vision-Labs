import cv2
import numpy as np

# for filter


def erode(img):
    h, w = img.shape
    kernal = np.array(((0, 1, 0), (1, 0, 1), (0, 1, 0)), dtype=int)
    out = img.copy()
    tmp = out.copy()
    for x in range(1, h-1):
        for y in range(1, w-1):
            if np.sum(kernal * tmp[x-1:x+2, y-1:y+2]) < 255*4:
                out[x, y] = 0
    return out


def dilate(img):
    h, w = img.shape
    kernal = np.array(((0, 1, 0), (1, 0, 1), (0, 1, 0)), dtype=int)
    out = img.copy()
    tmp = out.copy()
    for x in range(1, h-1):
        for y in range(1, w-1):
            if np.sum(kernal * tmp[x-1:x+2, y-1:y+2]) >= 255:
                out[x, y] = 255
    return out


def refine(img):
    h, w = img.shape
    out = np.zeros((h, w), dtype=int)
    out[img > 0] = 1      # chage scare to [0,1]
    out = 1-out           # reverse

    while True:
        delet_node1 = []
        delet_node2 = []

        # step 1
        for x in range(1, h-1):
            for y in range(1, w-1):
                if out[x, y] == 1:  # 如果是前景点
                    num_of_one = np.sum(out[x-1:x+2, y-1:y+2])-1  # p1的非零邻点个数
                    if num_of_one >= 2 and num_of_one <= 6:  # 如果p1的非零邻点个数在2到6之间
                        if count(out, x, y) == 1:  # 若从0到1的变化次数为1
                            if out[x-1, y]*out[x+1, y]*out[x, y+1] == 0 and out[x, y-1]*out[x+1, y]*out[x, y+1] == 0:
                                delet_node1.append((x, y))  # 将当前点加入删除点list

        for node in delet_node1:  # 对删除点list进行遍历
            out[node] = 0  # 将删除点设置为0

        # step 2
        for x in range(1, h-1):
            for y in range(1, w-1):
                if out[x, y] == 1:  # 如果是前景点
                    num_of_one = np.sum(out[x-1:x+2, y-1:y+2])-1  # p1的非零邻点个数
                    if num_of_one >= 2 and num_of_one <= 6:  # 如果p1的非零邻点个数在2到6之间
                        if count(out, x, y) == 1:  # 若从0到1的变化次数为1
                            if out[x-1, y]*out[x, y-1]*out[x+1, y] == 0 and out[x-1, y]*out[x, y-1]*out[x, y+1] == 0:
                                delet_node2.append((x, y))  # 将当前点加入删除点list

        for node in delet_node2:  # 对删除点list进行遍历
            out[node] = 0  # 将删除点设置为0

        if len(delet_node1) == 0 and len(delet_node2) == 0:
            break

    out = 1 - out  # 取反
    out = out.astype(np.uint8) * 255  # 转换为0和255

    return out


def count(img, x, y):
    num = 0
    if (img[x-1, y-1] - img[x-1, y]) == 1:  # p2到p3
        num += 1
    if (img[x, y-1] - img[x-1, y-1]) == 1:  # p3到p4
        num += 1
    if (img[x+1, y-1] - img[x, y-1]) == 1:  # p4到p5
        num += 1
    if (img[x+1, y] - img[x+1, y-1]) == 1:  # p5到p6
        num += 1
    if (img[x+1, y+1] - img[x+1, y]) == 1:  # p6到p7
        num += 1
    if (img[x, y+1] - img[x+1, y+1]) == 1:  # p7到p8
        num += 1
    if (img[x-1, y+1] - img[x, y+1]) == 1:  # p8到p9
        num += 1
    if (img[x-1, y] - img[x-1, y+1]) == 1:  # p9到p2
        num += 1
    return num


img = cv2.imread("./image.jpg", 0)
blur = cv2.GaussianBlur(img, (5, 5), 0)

# otsu part

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
print("{} {}".format(thresh, ret))
# convert
result_img = img.copy()
for x in range(0, img.shape[0]):
    for y in range(0, img.shape[1]):
        if result_img[x][y] < thresh:
            result_img[x][y] = 0
        else:
            result_img[x][y] = 255
# save image
# cv2.imshow("otsu_result", result_img)
cv2.imwrite("otsu_result.jpg", result_img)

# dilate and erode
dilate_result = dilate(result_img)
erode_result = erode(dilate_result)
erode_result = erode(erode_result)
erode_result = erode(erode_result)
dilate_result = dilate(erode_result)
dilate_result = dilate(dilate_result)

# cv2.imshow("res", dilate_result)
cv2.imwrite("filter_result.jpg", dilate_result)


result = refine(dilate_result)

cv2.imshow("res", result)
cv2.waitKey(0)
cv2.imwrite("refined_img.jpg", result)
