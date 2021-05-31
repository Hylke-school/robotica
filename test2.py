from servo import Servo


def main():
    servo = Servo()
    servo.construct_send(0x00, 0x03, 30, 0x00, 0x01)


if __name__ == "__main__":
    main()
