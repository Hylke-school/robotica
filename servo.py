from time import sleep
import math
import RPi.GPIO as GPIO
import serial


class Neck:
    def __init__(self):
        self.bottom = Servo(0)
        self.top = Servo(1)

    def change_position(self, level):
        # level van 0 tot 100
        # 0 = liggend, 100 = staand
        position = 0.9 * level - 90
        self.top.set_position(position)
        self.bottom.set_position(position)


class Servo:
    def __init__(self, servo_id):
        self.serial = ServoSerial.getInstance()
        self.id = servo_id

    def set_position(self, degrees):
        self.serial.set_position(self.id, degrees)


class ServoSerial:
    def __init__(self):
        self.serial = serial.Serial(port='/dev/ttyS0', baudrate=57600, bytesize=serial.EIGHTBITS,
                                    parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, write_timeout=10)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(18, GPIO.OUT)
        ServoSerial.__instance = self

    def send(self, array, debug=False):
        array = self.get_array(array)
        print(array)
        GPIO.output(18, GPIO.HIGH)
        self.serial.reset_input_buffer()
        self.serial.reset_output_buffer()
        self.serial.write(bytearray(array))
        sleep(0.1)
        GPIO.output(18, GPIO.LOW)
        if debug:
            print(self.serial.read_all())

    def get_array(self, array):
        header = [0xFF, 0xFF]
        total = 0
        for i in array:
            total += i
        checksum = (~total) & 0xFF
        header.extend(array)
        header.append(checksum)
        return header

    def set_position(self, servo_id, degrees):
        position = math.floor((degrees + 150.) / 300. * 1023.)
        upper_pos = position // 256
        lower_pos = position % 256
        self.send([servo_id, 0x05, 0x03, 30, lower_pos, upper_pos])

    def construct_send(self, servo_id, instruction, address, par1, par2):
        self.send([servo_id, 0x05, instruction, address, par1, par2])

    # storage for the instance reference
    __instance = None

    def getInstance():
        if ServoSerial.__instance == None:
            ServoSerial()
        return ServoSerial.__instance
    # def __init__(self):
    #     """ Create singleton instance """
    #     # Check whether we already have an instance
    #     if ServoSerial.__instance is None:
    #         # Create and remember instance
    #         ServoSerial.__instance = ServoSerial.__impl()

    #     # Store instance reference as the only member in the handle
    #     self.__dict__['_Singleton__instance'] = ServoSerial.__instance

    # def __getattr__(self, attr):
    #     """ Delegate access to implementation """
    #     return getattr(self.__instance, attr)

    # def __setattr__(self, attr, value):
    #     """ Delegate access to implementation """
    #     return setattr(self.__instance, attr, value)
