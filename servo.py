import config
from time import sleep
import math
from lib.ax12 import Ax12
import RPi.GPIO as GPIO
import pigpio

servos = Ax12()


def angleToPosition(angle):
    """map angle van -150° naar 150° --> 0 naar 1023"""
    return math.floor((angle + 150.) / 300. * 1023.)


def map_value(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


class Neck:
    def __init__(self):
        self.bottomID = config.NECK_ID
        self.topID = config.HEAD_ID
        self.currentLevel = 100
        self.headPos = 0
        self.neckPos = 0
        servos.moveSpeed(self.bottomID, 50)
        servos.moveSpeed(self.topID, 50)
        self.move_head(0)
        self.change_position(100)

    def stepNeck(self, dLevel):
        """
        beweegt de nek ten opzichte van huidige level
        
        nieuwe level = huidige level + dLevel
        """
        self.change_position(self.currentLevel + dLevel)

    def change_position(self, level):
        """
        level van 0 tot 100

        0 = liggend, 100 = staand
        """
        self.currentLevel = level
        angle = 0.9 * level - 90
        self.neckPos = angle
        servos.move(self.bottomID, angleToPosition(angle))
        servos.move(self.topID, angleToPosition(angle + self.headPos))

    def move_head(self, angle):
        self.headPos = angle
        servos.move(self.topID, angleToPosition(angle + self.neckPos))

    def stepHead(self, dAngle):
        """
        beweegt hoofd ten opzichte van huidige hoek

        nieuwe angle = huidige angle + dAngle
        """
        self.move_head(self.headPos + dAngle)


class Hand:
    def __init__(self):
        self.handID = config.HAND_ID
        servos.setCWAngleLimit(self.handID, config.HAND_CLOSED)
        servos.setCCWAngleLimit(self.handID, config.HAND_OPEN)
        servos.moveSpeed(self.handID, config.HAND_MOVE_SPEED)
        self.currentPos = config.HAND_OPEN
        servos.move(self.handID, config.HAND_OPEN)

    def readLoad(self):
        """leest en print de huidige torque van de servo"""
        print("current load is: {}".format(servos.readLoad(self.handID)))

    def readPos(self):
        """leest en print de huidige positie van de servo"""
        print(servos.readPosition(self.handID))

    # open = 620
    # dicht = 210

    def open_fully(self):
        servos.move(self.handID, config.HAND_OPEN)

    def close_fully(self):
        servos.move(self.handID, config.HAND_CLOSED)

    def closeHand(self, movespeed):
        # if (self.currentPos - movespeed) >= config.HAND_CLOSED:
        #     # if self.loadCheck -1024 / 1024 < 0.98:
        #     self.currentPos -= movespeed
        #     servos.move(self.handID, int(self.currentPos))
        servos.move(self.handID, 450)

    def openHand(self, movespeed):
        if (self.currentPos + movespeed) <= config.HAND_OPEN:
            if self.loadCheck / 1024 < 0.9:
                self.currentPos += movespeed
                servos.move(self.handID, int(self.currentPos))

    def move_hand(self, input):
        """
        input van 0 - 1023
        
        gemapt naar -16 - 16

        0 - -16 ==> langzaam -> snel dicht

        0 - 16 ==> langzaam -> snel open
        """
        # print (input)
        self.loadCheck = servos.readLoad(self.handID)
        self.currentPos = servos.readPosition(self.handID)
        if (self.loadCheck is not None) and (self.currentPos is not None):
            mappedInput = (input - 512) / 20
            if mappedInput < -4:
                self.closeHand(abs(mappedInput))
            elif mappedInput > 0:
                self.openHand(mappedInput)


class Lift:
    def __init__(self):
        self.liftID = config.LIFT_ID
        # servos.setAngleLimit(self.liftID, 0, 0)
        servos.moveSpeed(self.liftID, 0)
        servos.setCWAngleLimit(self.liftID, 0)
        servos.setCCWAngleLimit(self.liftID, 0)

    def move_lift(self, speed):
        speed = abs(1023 - speed)
        if speed < 0 or speed > 1023:
            raise IndexError("speed out of range")
        # map speed from 0-1023 to 0-2047. Voor de servos 0 is CCW max snelheid aflopend naar 512. 513 is bewegend in de CW richting oplopend tot 1023
        if speed // 512:
            speed *= 2
        else:
            speed = -2 * speed + 1023
        # self.checkLoad = servos.readLoad(self.liftID)
        # if self.checkLoad is not None:
        #     if self.checkLoad - 1024 < 512:
        servos.moveSpeed(self.liftID, int(speed))
        #     else:
        #         servos.moveSpeed(self.liftID, 1024)


class Eyebrows:
    def __init__(self):
        # Declare PWM usage on non-hardware PWM pins. (PWM(Pin_Number, Frequency))\
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(config.EYEBROW_ID_LEFT, GPIO.OUT)
        GPIO.setup(config.EYEBROW_ID_RIGHT, GPIO.OUT)
        self.p1 = GPIO.PWM(config.EYEBROW_ID_LEFT, 50)
        self.p2 = GPIO.PWM(config.EYEBROW_ID_RIGHT, 50)
        self.p1.start(0.2)
        self.p2.start(0.2)

    def change_position(self, position):
        # """
        #     0 = eyebrows completely down
        #     100 = eyebrows completely up
        # """
        """
            Dutycycle starts at 2, finishing at 12. 
            2 = Eyebrows duty cycle at 0%
            12 = Eyebrows duty cycle at 100%
            2-12 = 10 'DutyCycle Microseconds'

            Eyebrow 1 takes normal position, eyebrow 2 is a mirrored version of p1. 
        """
        new_position = map_value(position, 0, 100, 2, 12)
        # print (new_position)
        self.p1.ChangeDutyCycle(new_position)
        new_position = 12 + 2 - new_position
        # print (new_position)
        self.p2.ChangeDutyCycle(new_position)
        sleep(0.2)
        self.p1.ChangeDutyCycle(0)
        self.p2.ChangeDutyCycle(0)
        sleep(0.2)
