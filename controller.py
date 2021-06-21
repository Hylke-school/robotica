# from shutdown.main import Shutdown
from config import NECK_STATUS, Y_LEFT
from load_cell import LoadCell
import config
from movement import Movement
from remote_controller import RemoteController
from microphone import Microphone
from distance_sensor import DistanceSensor
from vision import Vision
from servo import Hand, Neck, Lift, Eyebrows
# from servo import Neck

import RPi.GPIO as GPIO
import time
import json
import requests
import config
import os

remote_controller = RemoteController()

movement = Movement()
neck = Neck()
hand = Hand()
lift = Lift()
eyebrows = Eyebrows()

# microphone = Microphone()
distance_sensor = DistanceSensor()
loadcell = LoadCell()
vision = Vision()

ip = config.TELEMETRY_IP
port = config.TELEMETRY_PORT


def loop():
    payload = remote_controller.get_data()

    if payload is not None:
        #print(payload)
        pass

    # if False:
        data = json.loads(payload.decode("utf-8"))
        if data[config.AUTO_MODE] == config.AUTO_MODE_SINGLE:
            data[config.WEIGHT] = loadcell.read_scale()
            print(" Weight data:" + str(data[config.WEIGHT]))

        # data[config.MICROPHONE] = microphone.get_data()
        # time.sleep(0.1)

        # if not data[config.POWER]:
        #     os.system("sudo shutdown -h now")

        if (data[config.NECK]) and (config.NECK_STATUS == False):
            neck.change_position(100)
            eyebrows.change_position(80)
            config.NECK_STATUS = True
        
        elif (not data[config.NECK]) and (config.NECK_STATUS == True):
            neck.change_position(0)
            eyebrows.change_position(50)
            config.NECK_STATUS = False

        if data[config.MANUAL]:  # Manually controlling the robot...
            if data[config.HAND]:
                # pass
                hand.move_hand(data[config.Y_RIGHT])
                lift.move_lift(data[config.Y_LEFT])
                
            else:
                # pass
                movement.update(data[config.Y_LEFT], data[config.Y_RIGHT])

        else:
            if data[config.AUTO_MODE] == config.AUTO_MODE_SINGLE:
                # Single Dance... 
                pass
            elif data[config.AUTO_MODE] == config.AUTO_MODE_LINE:
                # Line Dance with hearing...
                pass
            elif data[config.AUTO_MODE] == config.AUTO_MODE_CAPS:
                # Pickup caps...
                pass
            elif data[config.AUTO_MODE] == config.AUTO_MODE_VISION:
                # pass
                position = vision.get_blue_brick_position()
                # print(position)
                movement.update(position, abs(1023-position))
        # r = requests.post("http://" + ip + ":" + port, data=json.dumps(data))

# setup()
try:
    while True:
        loop()
finally:
    # lift.move_lift(512)
    movement.update(512, 512)
    GPIO.cleanup()
