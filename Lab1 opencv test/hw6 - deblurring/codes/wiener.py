import cv2
import math
import numpy as np

image = cv2.imread("./hw.bmp", 0)
length = 30 
angle = 11
angle = angle * math.pi / 180 

# calculate PSF
PSF = np.zeros(image.shape) 
h, w = image.shape
x_center = int((h - 1) / 2)
y_center = int((w - 1) / 2)

for i in range(length):
    delta_x = round(math.sin(angle) * i)
    delta_y = round(math.cos(angle) * i)
    PSF[int(x_center - delta_x), int(y_center + delta_y)] = 1

PSF = PSF / np.sum(PSF)  # normalizatio

G = np.fft.fft2(image)  # fast fourier transform 
H = np.fft.fft2(PSF)
K = 0.015 # set K

# wiener filiter
wiener_fft = np.conj(H) / (np.abs(H) ** 2 + K) 
F = wiener_fft * G
f = np.fft.ifftshift(np.fft.ifft2(F))  
f = f.real
f = f.astype(np.uint8)  

cv2.imshow("restoreImag",f)
cv2.waitKey(0)
cv2.imwrite("restoreImage.png", f)
