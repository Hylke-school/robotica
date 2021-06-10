from config import *
from time import sleep
import math
from lib.ax12 import Ax12

servos = Ax12()

class Neck:
    def __init__(self):
        self.bottomID = NECK_ID
        self.topID = HEAD_ID
        servos.moveSpeed(0, 100)
        servos.moveSpeed(1, 100)
        self.move_head(-90)
        self.change_position(0)

    def stepNeck(self, dLevel):
        """
        beweegt de nek ten opzichte van huidige level
        
        nieuwe level = huidige level + dLevel
        """
        self.change_position(self.currentLevel+dLevel)

    def change_position(self, level):
        """
        level van 0 tot 100
        
        0 = liggend, 100 = staand
        """
        self.currentLevel = level
        angle = 0.9 * level - 90
        self.neckPos = angle
        servos.move(self.bottomID, angleToPosition(angle))
        servos.move(self.topID, angleToPosition(angle+self.headPos))

    def move_head(self, angle):
        self.headPos = angle
        servos.move(self.topID, angleToPosition(angle+self.neckPos))

    def stepHead(self, dAngle):
        """
        beweegt hoofd ten opzichte van huidige hoek

        nieuwe angle = huidige angle + dAngle
        """
        self.move_head(self.headPos+dAngle)

def angleToPosition(angle):
    "map angle from -150° to 150° --> 0 to 1023"
    return math.floor((angle + 150.)/300. * 1023.)

class Hand:
    def __init__(self):
        self.handID = HEAD_ID
        servos.moveSpeed(self.handID, 80)

    def readLoad(self):
        "leest en print de huidige torque van de servo"
        print(servos.readLoad(self.handID))

    def readPos(self):
        "leest en print de huidige positie van de servo"
        print(servos.readPosition(self.handID))
    #open = 650
    #dicht = 1023

    def openHand(self):
        servos.move(self.handID, HAND_OPEN)

    def closeHand(self):
        servos.move(self.handID, HAND_CLOSED)

    def moveHand(self, pos):
        servos.move(self.handID, pos)