import RPi.GPIO as GPIO
import pigpio
from time import sleep, time
import config
from servo import Neck, Lift, Hand, Eyebrows
from movement import Movement

neck = Neck()
hand = Hand()
lift = Lift()
eyebrows = Eyebrows()
movement = Movement()

class Dance:
    def __init__(self):
        pass

    def single_dance():
        pass

    def line_dance():
        pass

    def intro():
        neck.change_position(50)
        sleep(1)
        eyebrows.change_position(50)


        pass

    def pirouette(duration: float, clockwise: bool):
        end = time() + duration
        while time() < end:
            if clockwise:
                movement.update(0, 1023) # Turn Left
            else:
                movement.update(1023, 0) # Turn Right
            pass

    def wiggle(self):
        self.pirouette(.2, True)
        sleep(.2)
        self.pirouette(.4, False)
        sleep(.4)
        self.pirouette(.2, True)
        sleep(.2)
        pass

    def headbang(times: int):
        for i in range(times):
            neck.move_head(45)
            sleep(.7)
            neck.move_head(0)
            sleep(.7)

    def neckbang(times: int):
        for i in range(times):
            neck.change_position(50)
            sleep(.7)
            neck.change_position(100)
            sleep(.7)

    def clapping():
        hand.closeHand()
        sleep(.1)
        hand.openHand()
        pass
    