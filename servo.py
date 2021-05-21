import serial
import math
from pyax12.connection import Connection
import pyax12.instruction_packet as instruction

linux = 'dev/ttyS0'
windows = 'COM3'

#overbodig?
def getByteArray(id: int, instruction: int, params: list):
    result = 'FF FF {:02X} {:02X} {:02X} {} {:02X}'
    paramstr = ' '.join(['{:02X}'.format(i) for i in params])
    length = len(params) + 2
    total = id+length+instruction+sum(params)
    checksum = (~total)&0xff
    return bytearray.fromhex(result.format(id, length, instruction, paramstr, checksum))

#ongetest! Wees voorzichtig!
def main():
    serial_connection = Connection(linux)
    available = serial_connection.scan()
    print(available)

if __name__ == "__main__":
    main()