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
        self.currentLevel = 0
        self.headPos = 0
        self.neckPos = 0
        servos.moveSpeed(self.bottomID, 100)
        servos.moveSpeed(self.topID, 100)
        self.move_head(0)
        self.change_position(0)

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
        self.currentPos = config.HAND_OPEN
        self.openHand(config.HAND_OPEN_SPEED)
        servos.moveSpeed(self.handID, config.HAND_MOVE_SPEED)

    def readLoad(self):
        """leest en print de huidige torque van de servo"""
        print(servos.readLoad(self.handID))

    def readPos(self):
        """leest en print de huidige positie van de servo"""
        print(servos.readPosition(self.handID))

    # open = 650
    # dicht = 1023

    def openHand(self, movespeed):
        if (self.currentPos - movespeed) >= config.HAND_OPEN:
            servos.move(self.handID, self.currentPos - movespeed)
        else:
            servos.move(self.handID, config.HAND_OPEN)
        self.currentPos = servos.readPosition(self.handID)

    def closeHand(self, movespeed):
        if servos.readLoad(self.handID) - 1023 < 900:
            if (self.currentPos + movespeed) <= config.HAND_CLOSED:
                servos.move(self.handID, self.currentPos + movespeed)
            else:
                servos.move(self.handID, config.HAND_CLOSED)
        self.currentPos = servos.readPosition(self.handID)

    def moveHand(self, input):
        """
        input van 0 - 1023
        
        gemapt naar -16 - 16

        0 - -16 ==> langzaam -> snel dicht

        0 - 16 ==> langzaam -> snel open
        """

        mappedInput = (input - 512) / 32
        if mappedInput < 0:
            self.closeHand(abs(mappedInput))
        elif mappedInput > 0:
            self.openHand(mappedInput)
        self.currentPos = servos.readPosition(self.handID)


class Lift:
    def __init__(self):
        self.liftID = config.LIFT_ID

    def move_lift(self, speed):
        speed = map_value(speed, 0, 1023, 0, 2047)
        if abs(servos.readLoad(self.liftID) - 1023) < 900:
            servos.moveSpeed(self.liftID, speed)
        else:
            servos.moveSpeed(self.liftID, 1024)


class Eyebrows:
    def __init__(self):
        self.left_eyebrow = Eyebrow(config.EYEBROW_ID_LEFT)
        self.right_eyebrow = Eyebrow(config.EYEBROW_ID_RIGHT)

    def set_position(self, position):
        """
            0 = eyebrows completely down
            100 = eyebrows completely up
        """
        self.left_eyebrow.set_position(position)
        self.right_eyebrow.set_position(-1 * position)


class Eyebrow:
    def __init__(self, eyebrow_id):
        self.pi = pigpio.pi()
        if eyebrow_id == config.EYEBROW_ID_LEFT:
            self.pwmPin = config.LEFT_EYEBROW_PWM
            self.pi.set_PWM_frequency(config.LEFT_EYEBROW_PWM, config.EYEBROW_PWM_FREQUENCY)

        elif eyebrow_id == config.EYEBROW_ID_RIGHT:
            self.pwmPin = config.RIGHT_EYEBROW_PWM
            self.pi.set_PWM_frequency(config.RIGHT_EYEBROW_PWM, config.EYEBROW_PWM_FREQUENCY)

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pwmPin, GPIO.OUT)

    def set_position(self, position):
        # TODO: make position actually move eyebrows to right position
        self.pi.set_PWM_dutycycle(self.pwmPin, position)
