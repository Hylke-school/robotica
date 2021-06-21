import RPi.GPIO as GPIO
import pigpio
from time import sleep
import config


class Movement:
    engineLeft = None
    engineRight = None

    def __init__(self):
        self.engineLeft = Motor(config.LEFT_MOTOR_ID)
        self.engineRight = Motor(config.RIGHT_MOTOR_ID)

    def update(self, y_left, y_right):
        # (0 - 1023) -> (0 - 512) = backwards -> (512 - 1023) = Forward
        y_left -= 512
        y_left = -1 * self.map_value(y_left, -512, 512, -255, 255)

        y_right -= 512
        y_right = self.map_value(y_right, -512, 512, -255, 255)
        sleep(0.05)
        print("y_left: {}, y_right: {}".format(y_left, y_right))
        self.engineLeft.set_speed(y_left)
        self.engineRight.set_speed(y_right)

    @staticmethod
    def map_value(value, in_min, in_max, out_min, out_max):
        return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


class Motor:
    def __init__(self, engine_name):
        self.pi = pigpio.pi()
        if engine_name == config.LEFT_MOTOR_ID:
            self.pi.set_PWM_frequency(config.LEFT_MOTOR_PWM, 500)
            self.pwmPin = config.LEFT_MOTOR_PWM
            self.inA = config.LEFT_MOTOR_A
            self.inB = config.LEFT_MOTOR_B

        elif engine_name == config.RIGHT_MOTOR_ID:
            self.pi.set_PWM_frequency(config.RIGHT_MOTOR_PWM, 500)
            self.pwmPin = config.RIGHT_MOTOR_PWM
            self.inA = config.RIGHT_MOTOR_A
            self.inB = config.RIGHT_MOTOR_B

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pwmPin, GPIO.OUT)
        GPIO.setup(self.inA, GPIO.OUT)
        GPIO.setup(self.inB, GPIO.OUT)
        self.pi.set_PWM_dutycycle(self.pwmPin, 0)

    
    def set_speed(self, speed):
        if speed > 5:
            # forwards
            GPIO.output(self.inA, GPIO.LOW)
            GPIO.output(self.inB, GPIO.HIGH)
        elif speed < -5:
            # backwards
            GPIO.output(self.inA, GPIO.HIGH)
            GPIO.output(self.inB, GPIO.LOW)

        current_pwm = self.pi.get_PWM_dutycycle(self.pwmPin)
        speed = abs(speed)
        difference = speed - current_pwm
        if difference < 0:
            difference = 0

        if abs(difference) > 20:
            current_pwm += difference / 5
        else:
            current_pwm = speed
        self.pi.set_PWM_dutycycle(self.pwmPin, current_pwm)  # 0 - 255
