# from shutdown.main import Shutdown
import config
from movement import Movement
from remote_controller import RemoteController
from weight_sensor import WeightSensor
import time
import json
import requests
import config
import os

movement = Movement()
remote_controller = RemoteController()
weight = WeightSensor()
ip = config.TELEMETRY_IP
port = config.TELEMETRY_PORT


# def setup():
#     controller = Controller()
#     movement = Movement()


def loop():
    payload = remote_controller.get_data()
    # r = requests.post("http://" + ip + ":" + port, data=payload)
    print(payload)
    if payload is not None:
        data = json.loads(payload.decode("utf-8"))
        data["weight"] = weight.get_data()
        time.sleep(0.1)

        if data[config.POWER]:
            os.system("sudo shutdown -h now")

        if not data[config.MANUAL]:  # Manual controlling the robot...
            movement.update(data[config.Y_LEFT], data[config.Y_RIGHT])

        else:
            if data[config.AUTO_MODE] == config.AUTO_MODE_SINGLE:
                # Single Dance...
                return
            elif data[config.AUTO_MODE] == config.AUTO_MODE_LINE:
                # Line Dance with hearing...
                return
            elif data[config.AUTO_MODE] == config.AUTO_MODE_CAPS:
                # Pickup caps...
                return
            elif data[config.AUTO_MODE] == config.AUTO_MODE_VISION:
                # Follow blue brick...
                return


# setup()
while True:
    loop()
