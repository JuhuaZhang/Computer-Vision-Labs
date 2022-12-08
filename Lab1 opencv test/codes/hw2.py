import cv2
import numpy as np

cap = cv2.VideoCapture('./hw2.mp4')
saver = cv2.VideoWriter("./hw2_result.mp4",cv2.VideoWriter_fourcc(*'XVID'),24,(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

font                   = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (20,100)
fontScale              = 1
fontColor              = (0,0,0)
thickness              = 3
lineType               = 3

while(True):
    ret, frame = cap.read()
    cv2.putText(frame, 'ZHANG Jiahao, Student ID: 3190103683',bottomLeftCornerOfText, font, fontScale, fontColor, thickness, lineType)
	# Display the resulting frame
    cv2.imshow('video', frame)
    saver.write(frame)
	# creating 'q' as the quit
	# button for the video
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# release the cap object
cap.release()
# close all windows
cv2.destroyAllWindows()
