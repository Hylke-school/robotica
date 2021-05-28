from dynamixel_sdk import *
import RPi.GPIO as GPIO

class ax12:
    def __init__(self, port, protocol, baudrate):
        self.port = PortHandler(port)
        self.packet = PacketHandler(protocol)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(18, GPIO.OUT)

        if port.openPort():
            print("opened")
        else:
            print("port failed")
            quit()

        if port.setBaudRate(baudrate):
            print("baudrate set")
        else:
            print("baudrate failed")
            quit()

    def write(self, port, txpacket):
        GPIO.output(18, GPIO.HIGH)

