import math
import threading
import config
import cv2
import numpy as np
from flask import Response, render_template, Flask

app = Flask(__name__)


class Vision:
    def __init__(self):
        self.blueBrick_Position = None
        self.cap_x = None
        self.cap_y = None
        app.run(debug=False, host=config.ROBOT_IP)
        self.thread = None
        self.thread = threading.Thread(target=self.blueBrick(), daemon=True)
        self.thread.start()

    def blueBrick(self):
        cap = cv2.VideoCapture(0)
        cap_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        cap_width_middle = cap_width / 2
        cap_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        while True:
            _, frame = cap.read()
            # Convert to HSV color space
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            # Setting the lower and upper color border
            lower_blue = np.array([100, 80, 50])
            upper_blue = np.array([110, 255, 255])
            # Making a mask
            mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
            # Gets only the objects that are blue
            blue_res = cv2.bitwise_and(frame, frame, mask=mask_blue)
            # Convert to grayscale
            gray = cv2.cvtColor(blue_res, cv2.COLOR_BGR2GRAY)
            # Making a treshold
            _, trash = cv2.threshold(gray, 0, 255, 0)
            # Finding the contours
            contours, _ = cv2.findContours(trash, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            for cnt in contours:
                if cv2.contourArea(cnt) <= 500:
                    continue
                # Gets the position of the contour through drawing a rectangle around it
                x, y, w, h = cv2.boundingRect(cnt)
                self.blueBrick_Position = ((x + (w / 2)) / cap_width) * 1023

                # Draws a rectangle
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # Draws a vertical line
            cv2.line(frame, (cap_width_middle, 0), (cap_width_middle, cap_height), (0, 255, 0), 2)
            cv2.imshow('window', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def stop_vision_bluebrick(self):
        self.thread.join()

    def get_blue_brick_position(self):
        return self.blueBrick_Position

    def findCap(self):
        cap = cv2.VideoCapture(0)
        cap_width_middle = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) / 2)
        cap_height_middle = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) / 2)

        while (True):
            # read current frame
            _, frame = cap.read()
            # convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # apply filter
            bilateral = cv2.bilateralFilter(frame, 5, 175, 175)
            # apply Canny edge detection, all edges become white, rest becomes black
            edges = cv2.Canny(bilateral, 75, 200)
            # find contours in the edges
            contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            cntlist = []
            for cnt in contours:
                # calculate circumference
                perimeter = cv2.arcLength(cnt, True)
                # approximate if object is circle-like
                approx = cv2.approxPolyDP(cnt, 0.01 * perimeter, True)
                # calculate area
                area = cv2.contourArea(cnt)
                if perimeter == 0:
                    continue
                # calculate roundness factor
                factor = 4 * math.pi * area / perimeter ** 2
                if ((len(approx) > 8) & (area > 400) & (factor > 0.7)):
                    cntlist.append(cnt)
            # find the object lowest on the screen
            if cntlist != []:
                # 0: lowest y of object contour, 1: object contour itself
                target = [0, None]
                for cnt in cntlist:
                    # get rectangle of contour
                    x, y, w, h = cv2.boundingRect(cnt)
                    # check if contour is lower than the current lowest (the lower, the higher the value)
                    if (y + h) > target[0]:
                        target[0] = y + h
                        target[1] = cnt
                # null check
                if target[1] is not None:
                    # draw contour of lowest object
                    cv2.drawContours(frame, target[1], -1, (255, 0, 0), 2)
                # get rectangle of lowest object
                x, y, w, h = cv2.boundingRect(target[1])
                # calculate coordinates of its middle
                mid_x = int(x + w / 2)
                mid_y = int(y + h / 2)
                values = [0, 0]
                # calculate its position relative to middle of screen
                # 0.00 , 0.00 is in the middle
                #            0.00 , -1.00
                #                 |
                # -1.00 , 0.00 ----+---- 1.00 , 0.00
                #                 |
                #            0.00 , 1.00
                values[0] = round(-1 + mid_x / cap_width_middle, 2)
                values[1] = round(-1 + mid_y / cap_height_middle, 2)
                # draw circle in middle of found object
                cv2.circle(frame, (mid_x, mid_y), 5, (0, 255, 0), 1)
                # print the relative position in console
                print("dx: " + str(values[0]) + " dy: " + str(values[1]))
            # draw plus line on screen
            cv2.line(frame, (cap_width_middle - 50, cap_height_middle), (cap_width_middle + 50, cap_height_middle),
                     (0, 255, 0), 1)
            cv2.line(frame, (cap_width_middle, cap_height_middle - 50), (cap_width_middle, cap_height_middle + 50),
                     (0, 255, 0), 1)

            # cv2.imshow('window', frame)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break

            # encode to jpg bytes to send to webbrowser
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'

    @app.route('/')
    def index(self):
        return render_template('index.html')

    @app.route('/video_feed')
    def video_feed(self):
        return Response(self.findCap(), mimetype='multipart/x-mixed-replace; boundary=frame')
