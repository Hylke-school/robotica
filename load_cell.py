import time
from lib.hx711 import HX711
import config

class LoadCell:
    # Set the right pins and values for the loadcell
    def __init__(self):
        self.hx = HX711(config.SCALE_DAT, config.SCALE_CLK, gain=128)
        self.hx.set_offset(config.SCALE_OFFSET)
        self.hx.set_scale(config.SCALE_RATIO)

    # Read the scale in grams and return the value.
    def read_scale(self):
        val = self.hx.get_grams()
        return val
