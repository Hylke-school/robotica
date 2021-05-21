import serial
import math

linux = 'dev/ttyUSB0'
windows = 'COM3'
def getByteArray(id: int, instruction: int, params: list):
    result = 'FF FF {:02X} {:02X} {:02X} {} {:02X}'
    paramstr = ' '.join(['{:02X}'.format(i) for i in params])
    length = len(params) + 2
    total = id+length+instruction+sum(params)
    checksum = (~total)&0xff
    return bytearray.fromhex(result.format(id, length, instruction, paramstr, checksum))

def main():
    # port = serial.Serial(windows)
    # print(port.name)
    # port.close()
    #checksum klopt niet???
    print(getByteArray(0xFE, 0x03, [0x03, 0x01, 0xff]))

if __name__ == "__main__":
    main()