import dance
import time
import config
from servo import Eyebrows

eyebrows = Eyebrows()
dancydance = dance.Dance(eyebrows)
dancydance.line_dance(18)
