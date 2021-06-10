import cv2
import numpy as np

cap = cv2.VideoCapture("http://192.168.1.6:8080/video")

def empty(a):
    pass
cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters",640,480)
cv2.createTrackbar("LR","Parameters",10,255,empty)
cv2.createTrackbar("LG","Parameters",60,255,empty)
cv2.createTrackbar("LB","Parameters",20,255,empty)
cv2.createTrackbar("HR","Parameters",20,255,empty)
cv2.createTrackbar("HG","Parameters",250,255,empty)
cv2.createTrackbar("HB","Parameters",250,255,empty)

while True:
    camera, frame = cap.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lr = cv2.getTrackbarPos("LR","Parameters")
    lg = cv2.getTrackbarPos("LG","Parameters")
    lb = cv2.getTrackbarPos("LB","Parameters")
    hr = cv2.getTrackbarPos("HR","Parameters")
    hg = cv2.getTrackbarPos("HG","Parameters")
    hb = cv2.getTrackbarPos("HB","Parameters")

    low = np.array([lr, lg, lb])
    high = np.array([hr, hg, hb])

    mask = cv2.inRange(hsv_frame, low, high)
    edit = cv2.bitwise_and(frame, frame, mask=mask)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel)

    cv2.imshow("Frame", cv2.resize(frame, (640, 480)))
    cv2.imshow("Edit", cv2.resize(edit, (640, 480)))
    cv2.imshow("Mask", cv2.resize(mask, (640, 480)))

    key = cv2.waitKey(1)
    if key == 27:
        break
