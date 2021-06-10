import time
from lib.hx711 import HX711
import config


class LoadCell:
    def __init__(self):
        self.hx = HX711(config.SCALE_DAT, config.SCALE_CLK)
        self.hx.set_offset(config.SCALE_OFFSET)
        self.hx.set_scale(config.SCALE_RATIO)

    # Read the scale in grams and return the value.
    def read_scale(self):
        val = self.hx.get_grams()

        # --- TODO: CHECK IF THIS IS NECESSARY...
        self.hx.power_down()
        time.sleep(.001)
        self.hx.power_up()
        # --- 

        return val

# def cleanAndExit():
#     print("Cleaning...")
#     GPIO.cleanup()
#     print("Bye!")
#     sys.exit()


# def setup():
#     """
#     code run once
#     """
#     hx.set_offset(config.SCALE_OFFSET)
#     hx.set_scale(config.SCALE_RATIO)


# def loop():
#     """
#     code run continuosly
#     """

#     try:
#         val = hx.get_grams()
#         print(val)


#         time.sleep(2)
#     except (KeyboardInterrupt, SystemExit):
#         cleanAndExit()
