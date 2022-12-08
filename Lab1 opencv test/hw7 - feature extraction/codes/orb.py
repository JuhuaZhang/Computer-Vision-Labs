import cv2

image = cv2.imread('RawImg.jpeg')  # 读取图片

fearure = 300  # 设置特征点数量
orb = cv2.ORB_create(fearure)  # 创建ORB对象
kp = orb.detect(image, None)  # 寻找关键点
keypoint = cv2.drawKeypoints(
    image, kp, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)  # 绘制关键点

cv2.imshow("result", keypoint)
cv2.waitKey(0)
cv2.imwrite("orb_result.png", keypoint)
