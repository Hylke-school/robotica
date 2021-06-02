from lib.ax12 import Ax12
import time

servos = Ax12()

while True:
    print("Move to 1023")
    servos.move(12, 800)
    time.sleep(3)
    print("Move to 0")
    servos.move(12, 200)
    time.sleep(3)
    print(servos.readTemperature(12))

