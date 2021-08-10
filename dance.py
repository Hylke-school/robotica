import RPi.GPIO as GPIO
import pigpio
from time import sleep, time
import config
from servo import Neck, Lift, Hand, Eyebrows
from movement import Movement

neck = Neck()
hand = Hand()
lift = Lift()
movement = Movement()


class Dance:
    def __init__(self, eyebrows):
        self.eyebrows = eyebrows

    def line_dance(self):
        self.clapping()

    def single_dance(self):
        self.startPosition()
        self.intro()
        self.wiggle(8)
        self.pirouette(config.PIROUETTE_TIME, True)
        self.clapping(4)
        self.pirouette(config.PIROUETTE_TIME, False)
        self.headbang(3)
        self.neckbang(2)
        self.neckAndHeadbang(3)
        self.pirouette(config.PIROUETTE_TIME, False)
        self.clapping(4)
        self.bigCircle(config.BIG_CIRCLE_TIME, True)
        self.bigCircle(config.BIG_CIRCLE_TIME, False)
        self.startPosition()
        self.intro()

    def line_dance(self, times):
        self.intro()
        self.clapping_and_headbang(times)

    def startPosition(self):
        neck.change_position(25)
        neck.move_head(60)
        sleep(1)
        self.eyebrows.change_position(50)
        sleep(1)

    def intro(self):
        neck.change_position(100)
        neck.move_head(0)
        sleep(2)

    def pirouette(self, duration: float, clockwise=True):
        end = time() + duration
        while time() < end:
            neck.change_position(100)
            if clockwise:
                movement.update(0, 1023)  # Turn Left
            else:
                movement.update(1023, 0)  # Turn Right
        movement.update(512, 512)

    def bigCircle(self, duration: float, clockwise=True):
        end = time() + duration
        while time() < end:
            neck.change_position(100)
            if clockwise:
                movement.update(500, 1023)  # Turn Left
            else:
                movement.update(1023, 500)  # Turn Right
        movement.update(512, 512)

    def wiggle(self, times: int):
        for i in range(times):
            neck.change_position(100)
            self.pirouette(.5, True)
            sleep(.2)
            self.pirouette(.5, False)
            sleep(.4)

    def headbang(self, times: int):
        for i in range(times):
            neck.move_head(45)
            sleep(.7)
            neck.move_head(0)
            sleep(.7)

    def neckbang(self, times: int):
        for i in range(times):
            neck.change_position(50)
            sleep(.7)
            neck.change_position(100)
            sleep(.7)

    def neckAndHeadbang(self, times: int):
        for i in range(times):
            neck.change_position(50)
            neck.move_head(90)
            sleep(.7)
            neck.change_position(100)
            neck.move_head(0)
            sleep(.7)

    def clapping(self, times: int):
        hand.open_fully()
        sleep(1)
        for i in range(times):
            hand.open_fully()
            sleep(1.5)
            hand.close_fully()
            sleep(1.5)
        hand.open_fully()

    def clapping_and_headbang(self, times: int):
        hand.open_fully()
        sleep(1)
        for i in range(times):
            neck.change_position(100)
            self.eyebrows.change_position(50)
            hand.open_fully()
            sleep(1.2)
            hand.close_fully()
            sleep(1.2)
            neck.change_position(50)
            self.eyebrows.change_position(80)
            hand.open_fully()
            sleep(1.2)
            hand.close_fully()
            sleep(1.2)
