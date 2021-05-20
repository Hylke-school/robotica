import serial

def main():
    port = serial.Serial('dev/ttyUSB0')
    print(port.name)
    port.close()

if __name__ == "__main__":
    main()