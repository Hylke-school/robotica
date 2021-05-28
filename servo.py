from time import sleep
import serial
import math
import RPi.GPIO
from pyax12.connection import Connection
import pyax12.instruction_packet as ip
from dynamixel_sdk import *

portName = '/dev/ttyAMA0'


def sendPacket(self, port, txpacket):
    rxpacket = 0
    error = 0
    # GPIO FIXEN! EIGEN RXTXPACKET MAKEN


baudrates = [1000000, 500000, 400000, 250000, 200000, 115200, 57600, 19200, 9600]


# ongetest! Wees voorzichtig!
def main():
    port = PortHandler(portName)
    packet = PacketHandler(1.0)

    if port.openPort():
        print("opened")
    else:
        print("port failed")
        quit()

    if port.setBaudRate(9600):
        print("baudrate set")
    else:
        print("baudrate failed")
        quit()

    model_number, comm_result, error = packet.ping(port, 0)
    if comm_result != COMM_SUCCESS:
        print("%s" % packet.getTxRxResult(comm_result))
    elif error != 0:
        print("%s" % packet.getRxPacketError(error))
    else:
        print("[ID:%03d] ping Succeeded. Dynamixel model number : %d" % (0, model_number))

    # Close port
    port.closePort()
    # ser = Connection(port=portName, baudrate=9600, rpi_gpio=True, waiting_time=0.1)
    # # for i in range(10):
    # #     ser.goto(0x00, i*10, speed=512, degrees=True)
    # #     sleep(1)
    # instruction = ip.InstructionPacket(0, ip.PING)
    # print(instruction.to_printable_string())
    # available = ser.send(instruction)
    # print(available.to_printable_string())
    # # ser.goto(0xFE, 0, speed=512, degrees=True)
    # # sleep(1)
    # # ser.goto(0xFE, 45, speed=512, degrees=True)
    # # sleep(1)
    # # ser.goto(0xFE, 0, speed=512, degrees=True)
    # ser.close()


if __name__ == "__main__":
    main()
