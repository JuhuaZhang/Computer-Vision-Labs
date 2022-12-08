import cv2
import numpy as np

image = cv2.imread("./hw1.png")

font                   = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (20,120)
fontScale              = 3
fontColor              = (0,0,0)
thickness              = 3
lineType               = 3

cv2.putText(image,'ZHANG Jiahao, Student ID: 3190103683', 
    bottomLeftCornerOfText, 
    font, 
    fontScale,
    fontColor,
    thickness,
    lineType)

cv2.imshow("image",image)

cv2.imwrite("./hw1_result.png",image)

cv2.waitKey()