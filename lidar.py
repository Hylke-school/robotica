import time
import adafruit_vl53l0x
import board
import busio
from digitalio import DigitalInOut
import config


class LIDAR:
    def _init_(self):
        # Initialize I2C bus and sensor.
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_vl53l0x.VL53L0X(self.i2c)

        self.xshut = [
            DigitalInOut(board.D23),
            DigitalInOut(board.D24),
            DigitalInOut(board.D25)
        ]

        for power_pin in self.xshut:
            # switch pin to output
            power_pin.switch_to_output(value=True)

        self.vl53 = []

        # change the addresses of the VL53L0X sensors
        for i, power_pin in enumerate(self.xshut):
            # turn on the VL53L0X to allow hardware check
            power_pin.value = True
            self.vl53.insert(i, self.sensor)  # adafruit_vl53l0x.VL53L0X(i2c))
            print(i)
            # no need to change the address of the last VL53L0X sensor
            if i < len(self.xshut) - 1:
                if True:
                    # default address is 0x29. Change that to something else
                    self.vl53[i].set_address(i + 0x30)  # address assigned should NOT be already in use

    def detect_range(self):
        for index, sensor in enumerate(self.vl53):
            print("Sensor {} Range: {}mm".format(index + 1, sensor.range))
        time.sleep(1.0)
        return sensor.range
