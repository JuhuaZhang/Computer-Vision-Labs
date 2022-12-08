import cv2

origin = cv2.imread('RawImg.jpeg')  # 读取图片
gray = cv2.cvtColor(origin, cv2.COLOR_BGR2GRAY)  # 将图片转为灰度图

feature = 300  # 设置特征点数量
sift = cv2.xfeatures2d.SIFT_create(feature)  # 创建SIFT对象
kp = sift.detect(gray, None)  # 寻找关键点
keypoint = cv2.drawKeypoints(
    origin, kp, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)  # 绘制关键点

cv2.imshow("result", keypoint)
cv2.waitKey(0)
cv2.imwrite("sift_result.png", keypoint)
