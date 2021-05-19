import cv2
import numpy as np
import math

def visiontest():
    cap = cv2.VideoCapture(0)
    while(True):
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (9,9), 0)
        ret, thrash = cv2.threshold(blur, 133, 200, cv2.THRESH_BINARY_INV)
        contours, hierarchy = cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
            if cv2.contourArea(c) <=500:
                continue
            x,y,w,h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x,y),(x+w,y+h), (0,255,0),2)
        cv2.drawContours(frame, contours, -1, (0,0,255),2)
        cv2.imshow('window', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

def blauwBlokje():
    cap = cv2.VideoCapture(0)
    cap_width_middle = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)/2)
    cap_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    while(True):
        _, frame = cap.read()

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower_blue = np.array([100,80,50])
        upper_blue = np.array([110,255,255])
        mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

        blue_res = cv2.bitwise_and(frame, frame, mask= mask_blue)

        gray = cv2.cvtColor(blue_res, cv2.COLOR_BGR2GRAY)
        _,trash = cv2.threshold(gray, 0,255,0)

        contours, _ = cv2.findContours(trash, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            if cv2.contourArea(cnt) <= 500:
                continue
            x,y,w,h = cv2.boundingRect(cnt)
            if x > cap_width_middle:
                print("right")
            elif x+w < cap_width_middle:
                print("left")
            else:
                print("middle")
            cv2.rectangle(frame, (x,y),(x+w,y+h), (0,255,0),2)
        cv2.line(frame, (cap_width_middle, 0), (cap_width_middle, cap_height), (0,255,0),2)
        cv2.imshow('window', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def findCap():
    cap = cv2.VideoCapture(0)

    while(True):
        _, frame = cap.read()
        frame = cv2.flip(frame,1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #edges ofzo
        bilateral = cv2.bilateralFilter(frame, 5, 175, 175)
        edges = cv2.Canny(bilateral, 75, 200)
        contours,_ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        cntlist = []
        for cnt in contours:
            perimeter = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.01*perimeter, True)
            area = cv2.contourArea(cnt)
            if perimeter ==0:
                continue
            factor = 4*math.pi*area/perimeter**2
            if ((len(approx) > 8) & (area > 400) & (factor > 0.7)):
                cntlist.append(cnt)
        cv2.drawContours(frame, cntlist, -1, (255,0,0),2)

        #hough circles
        # circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2, 100)

        # if circles is not None:
        #     circles = np.round(circles[0, :]).astype("int")
        #     for (x,y,r) in circles:
        #         cv2.circle(frame, (x,y), r, (0,255,0),2)

        #manual
        # blur = cv2.GaussianBlur(gray, (9,9),0)

        # _,th = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY_INV)
        # contours, hierarchy = cv2.findContours(th, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # for cnt in contours:
        #     area = cv2.contourArea(cnt)
        #     if area < 100:
        #         continue
        #     perimeter = cv2.arcLength(cnt, True)
        #     if perimeter == 0:
        #         continue
        #     factor = 4 * math.pi * area / perimeter**2
        #     if factor > 0.7:
        #         cv2.drawContours(frame, cnt, -1, (255,0,0),2)
        #     else:
        #         cv2.drawContours(frame, cnt, -1, (0,255,0),2)

        # cv2.imshow("gray",gray)
        # cv2.imshow("threshold",th)
        cv2.imshow('window', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def main():
    findCap()

if __name__ == "__main__":
    main()
