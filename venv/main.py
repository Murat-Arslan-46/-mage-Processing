import cv2
import numpy as np

url = "http://192.168.1.6:8080/video"
cap = cv2.VideoCapture(url)
def empty(a):
    pass
cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters",640,240)
cv2.createTrackbar("Threshold1","Parameters",15,255,empty)
cv2.createTrackbar("Threshold2","Parameters",25,255,empty)

cv2.createTrackbar("Area","Parameters",2000,10000,empty)

def getContours(img,imgContour):

    contours, hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)


    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > cv2.getTrackbarPos("Area","Parameters"):
            cv2.drawContours(imgContour,contours,-1,(255,0,255),7)
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02 * peri,True)
            print(len(approx))
            x,y,w,h = cv2.boundingRect(approx)
            cv2.rectangle(imgContour,(x,y),(x+w,y+h),(0,255,0),5)
            cv2.putText(imgContour, "Points: " + str(len(approx)), (x + w + 20, y + 20), cv2.FONT_HERSHEY_COMPLEX, .7, (0, 255, 0), 2)
            cv2.putText(imgContour, "Area: " + str(int(area)), (x + w + 20 , y + 45), cv2.FONT_HERSHEY_COMPLEX, .7, (0, 255, 0), 2)

while (1):
    camera, frame = cap.read()
    imgContour = frame.copy()
    imgGray = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    threshold1 = cv2.getTrackbarPos("Threshold1","Parameters")
    threshold2 = cv2.getTrackbarPos("Threshold2","Parameters")

    low = np.array([10, 60, 20])
    high = np.array([20, 255, 255])

    mask = cv2.inRange(imgGray, low, high)

    edges = cv2.Canny(mask,threshold1, threshold2)
    kernel = np.ones((2,2))
    imgDil = cv2.dilate(edges,kernel,iterations=1)
    getContours(imgDil,imgContour)
    cv2.imshow("Contour",cv2.resize(imgContour, (640, 480)))

    # Wait for Esc key to stop
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()