from time import sleep
import serial
import RPi.GPIO as GPIO


class Servo:
    def __init__(self):
        self.serial = serial.Serial(port='/dev/ttyS0', baudrate=57600, bytesize=serial.EIGHTBITS,
                                    parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, write_timeout=10)

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(18, GPIO.OUT)

    def send(self, array):
        array = self.get_array(array)
        GPIO.output(18, GPIO.HIGH)
        self.serial.reset_input_buffer()
        self.serial.reset_output_buffer()
        self.serial.write(bytearray(array))
        sleep(0.05)
        GPIO.output(18, GPIO.LOW)
        print(self.serial.read_all())

    @staticmethod
    def get_array(array):
        header = [0xFF, 0xFF]
        total = 0
        for i in array:
            total += i
        checksum = (~total) & 0xFF
        header.extend(array)
        header.append(checksum)
        return header

    def construct_send(self, servo_id, instruction, address, par1, par2):
        self.send([servo_id, 0x05, instruction, address, par1, par2])

    # def construct_send(self, servo_id, instruction, address, par1):
    #     self.send([servo_id, 0x05, instruction, address, par1])
