# ROBOT IP-ADDRESS
ROBOT_IP = "141.252.29.30"

# TELEMETRY VARIABLES
TELEMETRY_IP = "212.204.150.138"
TELEMETRY_PORT = "5356"

# LEFT MAIN ENGINE
LEFT_MOTOR_ID = 0
LEFT_MOTOR_PWM = 27
LEFT_MOTOR_A = 22
LEFT_MOTOR_B = 23

# RIGHT MAIN ENGINE
RIGHT_MOTOR_ID = 1
RIGHT_MOTOR_PWM = 17    
RIGHT_MOTOR_A = 24
RIGHT_MOTOR_B = 25

# REMOTE CONTROLLER INPUTS
X_LEFT = "x_l"                  # 0 - 1023
Y_LEFT = "y_l"                  # 0 - 1023
X_RIGHT = "x_r"                 # 0 - 1023
Y_RIGHT = "y_r"                 # 0 - 1023
CLICK_LEFT = "c_l"              # bool
CLICK_RIGHT = "c_r"             # bool
POWER = "p"                     # bool
MANUAL = "m"                    # bool
HAND = "claw"                   # bool
NECK = "neck"                   # bool
AUTO_MODE = "mode"              # string

# DIFFERENT STRING VALUES FOR AUTO_MODE
AUTO_MODE_SINGLE = "single"
AUTO_MODE_LINE = "line"
AUTO_MODE_CAPS = "caps"
AUTO_MODE_VISION = "vision"

# ADDITIONAL TELEMETRY OUTPUTS
WEIGHT = "weight"
MICROPHONE = "microphone"

# SERVO VARIABLES
HEAD_ID = 0
NECK_ID = 12
HAND_ID = 3 #11
LIFT_ID = 9
NECK_STATUS = True
HAND_OPEN = 630
HAND_CLOSED = 375
HAND_STEP_SPEED = 25
HAND_OPEN_SPEED = 25
HAND_MOVE_SPEED = 80

EYEBROW_PWM_FREQUENCY = 50
EYEBROW_ID_LEFT = 12
EYEBROW_ID_RIGHT = 13

# LOAD CELL VARIABLES
SCALE_DAT = 20
SCALE_CLK = 21
SCALE_OFFSET = 8027144.375    # TODO: Change to correct value.
SCALE_RATIO = -1078.9052287581699     # TODO: Change to correct value. (Measured weight / real item weight)

# MICROPHONE VARIABLES
ADC_CHANNEL = 0
SPI_BUS = 0
SPIDEV_BAUD_RATE = 1200000
MIC_SAMPLE_SIZE = 256
MIC_SAMPLING_PERIOD = 1 / 16384

# DANCING CONSTANTS
PIROUETTE_TIME = 4.75
BIG_CIRCLE_TIME = 13.5