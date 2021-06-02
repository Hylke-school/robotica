from time import sleep

from servo import Neck, ServoSerial, Servo
import serial as piserial


def main():
    # serial = ServoSerial()
    neck = Neck()
    neck.change_position(0)
    sleep(2)
    neck.change_position(50)
    # servo = Servo(0, serial)
    # servo2 = Servo(1)
    # servo = ServoSerial()
    # servo.construct_send(0x01, 0x03, 30, 0x00, 0x03)

    # servo.set_position(0)
    # servo2.set_position(90)


if __name__ == "__main__":
    main()
