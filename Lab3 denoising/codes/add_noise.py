# -*- coding: utf-8 -*-
import cv2
import random
import numpy as np
import convert


def sp_noise(image, prob):
    '''
    添加椒盐噪声
    image:原始图片
    prob:噪声比例
    '''
    image = cv2.imread(image)
    # print(image.shape)
    output = np.zeros(image.shape, np.uint8)
    noise_out = np.zeros(image.shape, np.uint8)
    thres = 1 - prob
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            rdn = random.random()  # 随机生成0-1之间的数字
            if rdn < prob:  # 如果生成的随机数小于噪声比例则将该像素点添加黑点，即椒噪声
                output[i][j] = 0
                noise_out[i][j] = 0
            elif rdn > thres:  # 如果生成的随机数大于（1-噪声比例）则将该像素点添加白点，即盐噪声
                output[i][j] = 255
                noise_out[i][j] = 255
            else:
                output[i][j] = image[i][j]  # 其他情况像素点不变
                noise_out[i][j] = 100
    # result = [noise_out, output]  # 返回椒盐噪声和加噪图像
    print(output.shape)
    return output


def gasuss_noise(image, mean=0, var=0.001):
    ''' 
        添加高斯噪声
        image:原始图像
        mean : 均值 
        var : 方差,越大，噪声越大
    '''
    image = cv2.imread(image)
    print(image.shape)
    image = np.array(image/255, dtype=float)  # 将原始图像的像素值进行归一化，除以255使得像素值在0-1之间
    # 创建一个均值为mean，方差为var呈高斯分布的图像矩阵
    noise = np.random.normal(mean, var ** 0.5, image.shape)
    # print(image.shape)
    # print(noise.shape)
    out = image + noise  # 将噪声和原始图像进行相加得到加噪后的图像
    if out.min() < 0:
        low_clip = -1.
    else:
        low_clip = 0.
    # clip函数将元素的大小限制在了low_clip和1之间了，小于的用low_clip代替，大于1的用1代替
    out = np.clip(out, low_clip, 1.0)
    out = np.uint8(out*255)  # 解除归一化，乘以255将加噪后的图像的像素值恢复
    #cv.imshow("gasuss", out)
    noise = noise*255
    return out


img_sp_noise = sp_noise('./RawImg.jpeg', 0.01)
img_gasuss_noise = gasuss_noise('./RawImg.jpeg')

cv2.imwrite('img_sp_noise.jpg', convert.RGB2GRAY(img_sp_noise))
cv2.imwrite('img_gasuss_noise.jpg', convert.RGB2GRAY(img_gasuss_noise))
