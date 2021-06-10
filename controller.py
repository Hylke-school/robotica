# from shutdown.main import Shutdown
from load_cell import LoadCell
import config
from movement import Movement
from remote_controller import RemoteController
from microphone import Microphone
from distance_sensor import DistanceSensor
from vision import Vision

import RPi.GPIO as GPIO
import time
import json
import requests
import config
import os

remote_controller = RemoteController()
movement = Movement()
microphone = Microphone()
distance_sensor = DistanceSensor()
loadcell = LoadCell()
vision = Vision()

ip = config.TELEMETRY_IP
port = config.TELEMETRY_PORT


def loop():
    payload = remote_controller.get_data()
    print(payload)
    if payload is not None:
        data = json.loads(payload.decode("utf-8"))
        data[config.WEIGHT] = loadcell.read_scale()
        data[config.MICROPHONE] = microphone.get_data()
        time.sleep(0.1)

        if data[config.POWER]:
            os.system("sudo shutdown -h now")

        if not data[config.MANUAL]:  # Manually controlling the robot...
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
                position = vision.get_blue_brick_position()
                movement.update(abs(position - 1023), position)

    # r = requests.post("http://" + ip + ":" + port, data=json.dumps(data))


# setup()
try:
    while True:
        loop()
finally:
    movement.update(512, 512)
    GPIO.cleanup()
