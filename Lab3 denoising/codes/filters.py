import cv2
import numpy as np
import math
import matplotlib.pyplot as plt


def mean_filter(img, size):
    # set image kernal
    kernal = 1/(size[0]*size[1])*np.ones(size, np.float32)
    # store the new image
    img_new = np.zeros(
        [int(img.shape[0]-2*(size[0]-1)/2), int(img.shape[1]-2*(size[1]-1)/2)])
    # convolution
    # in convolution area
    for x in range(int((size[0]-1)/2), int(img.shape[0]-(size[0]-1)/2)):
        for y in range(int((size[1]-1)/2), int(img.shape[1]-(size[1]-1)/2)):
            window = img[int(x-(size[0]-1)/2):int(x+(size[0]-1)/2+1),
                         int(y-(size[1]-1)/2):int(y+(size[1]-1)/2+1)]
            img_new[x-int((size[0]-1)/2)][y-int((size[0]-1)/2)
                                          ] = np.sum(window*kernal)
    return img_new


def median_filter(img, size):
    # store the new image
    img_new = np.zeros(
        [int(img.shape[0]-2*(size[0]-1)/2), int(img.shape[1]-2*(size[1]-1)/2)])
    # convolution
    # in convolution area
    for x in range(int((size[0]-1)/2), int(img.shape[0]-(size[0]-1)/2)):
        for y in range(int((size[1]-1)/2), int(img.shape[1]-(size[1]-1)/2)):
            window = img[int(x-(size[0]-1)/2):int(x+(size[0]-1)/2+1),
                         int(y-(size[1]-1)/2):int(y+(size[1]-1)/2+1)]
            img_new[x-int((size[0]-1)/2)][y-int((size[0]-1)/2)
                                          ] = np.median(window)
    return img_new


def bilateral_filter(img, size=(5, 5), sigma_s=10, sigma_r=10):
    kernal = np.ones(size, np.float32)
    # store the new image
    img_new = np.zeros(
        [int(img.shape[0]-2*(size[0]-1)/2), int(img.shape[1]-2*(size[1]-1)/2)])
    # convolution
    # in convolution area
    for x in range(int((size[0]-1)/2), int(img.shape[0]-(size[0]-1)/2)):
        for y in range(int((size[1]-1)/2), int(img.shape[1]-(size[1]-1)/2)):
            window = img[int(x-(size[0]-1)/2):int(x+(size[0]-1)/2+1),
                         int(y-(size[1]-1)/2):int(y+(size[1]-1)/2+1)]
            for i in range(window.shape[0]):
                for j in range(window.shape[1]):
                    dist = ((i-(window.shape[0]-1)/2)**2 +
                            (j-(window.shape[0]-1)/2)**2)/2/sigma_s
                    dValue = ((float(window[i][j]) - float(
                        window[int((window.shape[0]-1)/2)][int((window.shape[1]-1)/2)]))**2)/2/sigma_r
                    kernal[i][j] = math.exp(-dist)*math.exp(-dValue)
            kernal /= np.sum(kernal)
            img_new[x-int((size[0]-1)/2)][y-int((size[0]-1)/2)
                                          ] = np.sum(window*kernal)
    return img_new


if __name__ == '__main__':
    # read image
    img_gasuss_noise = cv2.imread('img_gasuss_noise.jpg', 0)
    img_sp_noise = cv2.imread('img_sp_noise.jpg', 0)

    # mean filter
    img_mean_gasuss_noise = mean_filter(img_gasuss_noise, (5, 5))
    cv2.imwrite("img_mean_gasuss_noise.jpg", img_mean_gasuss_noise)
    img_mean_sp_noise = mean_filter(img_sp_noise, (5, 5))
    cv2.imwrite("img_mean_sp_noise.jpg", img_mean_sp_noise)

    # median filter
    img_median_gasuss_noise = median_filter(img_gasuss_noise, (5, 5))
    cv2.imwrite("img_median_gasuss_noise.jpg", img_median_gasuss_noise)
    img_median_sp_noise = median_filter(img_sp_noise, (5, 5))
    cv2.imwrite("img_median_sp_noise.jpg", img_median_sp_noise)

    # bilateral filter
    img_bilateral_gasuss_noise = bilateral_filter(
        img_gasuss_noise, (5, 5), 500**2, 150**2)
    cv2.imwrite("img_bilateral_gasuss_noise.jpg", img_bilateral_gasuss_noise)
    img_bilateral_sp_noise = bilateral_filter(
        img_sp_noise, (5, 5), 500**2, 150**2)
    cv2.imwrite("img_bilateral_sp_noise.jpg", img_bilateral_sp_noise)
