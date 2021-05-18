import cv2
import numpy as np

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

def main():
    visiontest()

if __name__ == "__main__":
    main()
