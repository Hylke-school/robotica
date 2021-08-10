import dance
import time
import config
from servo import Eyebrows

eyebrows = Eyebrows()
dancydance = dance.Dance(eyebrows)
dancydance.single_dance()
