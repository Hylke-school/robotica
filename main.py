import math

import cv2
import numpy as np
from flask import Response, render_template, Flask

app = Flask(__name__)


def visiontest():
    cap = cv2.VideoCapture()
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (9, 9), 0)
        ret, thrash = cv2.threshold(blur, 133, 200, cv2.THRESH_BINARY_INV)
        contours, hierarchy = cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
            if cv2.contourArea(c) <= 500:
                continue
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.drawContours(frame, contours, -1, (0, 0, 255), 2)
        cv2.imshow('window', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


def blauwBlokje():
    cap = cv2.VideoCapture(0)
    cap_width_middle = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) / 2)
    cap_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    while (True):
        _, frame = cap.read()

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower_blue = np.array([100, 80, 50])
        upper_blue = np.array([110, 255, 255])
        mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

        blue_res = cv2.bitwise_and(frame, frame, mask=mask_blue)

        gray = cv2.cvtColor(blue_res, cv2.COLOR_BGR2GRAY)
        _, trash = cv2.threshold(gray, 0, 255, 0)

        contours, _ = cv2.findContours(trash, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            if cv2.contourArea(cnt) <= 500:
                continue
            x, y, w, h = cv2.boundingRect(cnt)
            if x > cap_width_middle:
                print("right")
            elif x + w < cap_width_middle:
                print("left")
            else:
                print("middle")
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.line(frame, (cap_width_middle, 0), (cap_width_middle, cap_height), (0, 255, 0), 2)
        cv2.imshow('window', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


def findCap():
    cap = cv2.VideoCapture(0)
    cap_width_middle = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)/2)
    cap_height_middle = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)/2)

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
        if cntlist != []:
            target = [0,None]
            for cnt in cntlist:
                x,y,w,h = cv2.boundingRect(cnt)
                if(y+h)>target[0]:
                    target[0] = y+h
                    target[1] = cnt
            if target[1] is not None:
                cv2.drawContours(frame, target[1], -1, (255,0,0),2)
            x,y,w,h = cv2.boundingRect(target[1])
            mid_x = int(x+w/2)
            mid_y = int(y+h/2)
            values = [0,0]
            values[0] = round(-1 + mid_x/cap_width_middle, 2)
            values[1] = round(-1 + mid_y/cap_height_middle,2)
            cv2.circle(frame, (mid_x,mid_y),5,(0,255,0),1)
            print("dx: "+str(values[0])+" dy: "+str(values[1]))

        cv2.line(frame, (cap_width_middle-50,cap_height_middle),(cap_width_middle+50,cap_height_middle),(0,255,0),1)
        cv2.line(frame, (cap_width_middle,cap_height_middle-50),(cap_width_middle,cap_height_middle+50),(0,255,0),1)

        # cv2.imshow('window', frame)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'


def main():
    findCap()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(findCap(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True, host="141.252.29.66")
    # main()
