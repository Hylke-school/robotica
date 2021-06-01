import time

import adafruit_vl53l0x
import board
import busio
from digitalio import DigitalInOut

# Initialize I2C bus and sensor.
i2c = busio.I2C(board.SCL, board.SDA)

xshut = [
    DigitalInOut(board.D17)
]

for power_pin in xshut:
    # make sure these pins are a digital output, not a digital input
    power_pin.switch_to_output(value=False)
    # These pins are active when Low, meaning:
    #   if the output signal is LOW, then the VL53L0X sensor is off.
    #   if the output signal is HIGH, then the VL53L0X sensor is on.
# all VL53L0X sensors are now off

vl53 = []

# now change the addresses of the VL53L0X sensors
for i, power_pin in enumerate(xshut):
    # turn on the VL53L0X to allow hardware check
    power_pin.value = True
    vl53.insert(i, adafruit_vl53l0x.VL53L0X(i2c))
    # no need to change the address of the last VL53L0X sensor
    if i < len(xshut) - 1:
    # if True:
        # default address is 0x29. Change that to something else
        vl53[i].set_address(i + 0x30)  # address assigned should NOT be already in use

# Optionally adjust the measurement timing budget to change speed and accuracy.
# See the example here for more details:
#   https://github.com/pololu/vl53l0x-arduino/blob/master/examples/Single/Single.ino
# For example a higher speed but less accurate timing budget of 20ms:
# vl53.measurement_timing_budget = 20000
# Or a slower but more accurate timing budget of 200ms:
# vl53.measurement_timing_budget = 200000
# The default timing budget is 33ms, a good compromise of speed and accuracy.

def detect_range(count=500):
    """ take count=5 samples """
    while count:
        for index, sensor in enumerate(vl53):
            print("Sensor {} Range: {}mm".format(index + 1, sensor.range))
        time.sleep(1.0)
        count -= 1

detect_range()