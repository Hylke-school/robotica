import time
from dynamixel_sdk import *
import RPi.GPIO as GPIO

TXPACKET_MAX_LEN = 250
RXPACKET_MAX_LEN = 250

# for Protocol 1.0 Packet
PKT_HEADER0 = 0
PKT_HEADER1 = 1
PKT_ID = 2
PKT_LENGTH = 3
PKT_INSTRUCTION = 4
PKT_ERROR = 4
PKT_PARAMETER0 = 5

# Protocol 1.0 Error bit
ERRBIT_VOLTAGE = 1  # Supplied voltage is out of the range (operating volatage set in the control table)
ERRBIT_ANGLE = 2  # Goal position is written out of the range (from CW angle limit to CCW angle limit)
ERRBIT_OVERHEAT = 4  # Temperature is out of the range (operating temperature set in the control table)
ERRBIT_RANGE = 8  # Command(setting value) is out of the range for use.
ERRBIT_CHECKSUM = 16  # Instruction packet checksum is incorrect.
ERRBIT_OVERLOAD = 32  # The current load cannot be controlled by the set torque.
ERRBIT_INSTRUCTION = 64  # Undefined instruction or delivering the action command without the reg_write command.

class ax12:
    def __init__(self, portName, protocol, baudrate):
        self.port = PortHandler(portName)
        self.packet = PacketHandler(protocol)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(18, GPIO.OUT)

        if self.port.openPort():
            print("opened")
        else:
            print("port failed")
            quit()

        if self.port.setBaudRate(baudrate):
            print("baudrate set")
        else:
            print("baudrate failed")
            quit()

    def getResult(self, result):
        if result == COMM_SUCCESS:
            return "[TxRxResult] Communication success!"
        elif result == COMM_PORT_BUSY:
            return "[TxRxResult] Port is in use!"
        elif result == COMM_TX_FAIL:
            return "[TxRxResult] Failed transmit instruction packet!"
        elif result == COMM_RX_FAIL:
            return "[TxRxResult] Failed get status packet from device!"
        elif result == COMM_TX_ERROR:
            return "[TxRxResult] Incorrect instruction packet!"
        elif result == COMM_RX_WAITING:
            return "[TxRxResult] Now receiving status packet!"
        elif result == COMM_RX_TIMEOUT:
            return "[TxRxResult] There is no status packet!"
        elif result == COMM_RX_CORRUPT:
            return "[TxRxResult] Incorrect status packet!"
        elif result == COMM_NOT_AVAILABLE:
            return "[TxRxResult] Protocol does not support this function!"
        else:
            return ""
    
    def getError(self, error):
        if error & ERRBIT_VOLTAGE:
            return "[RxPacketError] Input voltage error!"

        if error & ERRBIT_ANGLE:
            return "[RxPacketError] Angle limit error!"

        if error & ERRBIT_OVERHEAT:
            return "[RxPacketError] Overheat error!"

        if error & ERRBIT_RANGE:
            return "[RxPacketError] Out of range error!"

        if error & ERRBIT_CHECKSUM:
            return "[RxPacketError] Checksum error!"

        if error & ERRBIT_OVERLOAD:
            return "[RxPacketError] Overload error!"

        if error & ERRBIT_INSTRUCTION:
            return "[RxPacketError] Instruction code error!"

        return ""

    def writePacket(self, txpacket):
        GPIO.output(18, GPIO.HIGH)
        time.sleep(0.01)
        return self.packet.txPacket(self.port, txpacket)
    
    def readPacket(self):
        GPIO.output(18, GPIO.LOW)
        time.sleep(0.01)
        return self.packet.rxPacket(self.port)

    def readAndWritePacket(self, txpacket):
        rxpacket = None
        error = 0

        # tx packet
        result = self.writePacket(txpacket)
        if result != COMM_SUCCESS:
            return rxpacket, result, error

        # (Instruction == BulkRead) == this function is not available.
        if txpacket[PKT_INSTRUCTION] == INST_BULK_READ:
            result = COMM_NOT_AVAILABLE

        # (ID == Broadcast ID) == no need to wait for status packet or not available
        if (txpacket[PKT_ID] == BROADCAST_ID):
            self.port.is_using = False
            return rxpacket, result, error

        # set packet timeout
        if txpacket[PKT_INSTRUCTION] == INST_READ:
            self.port.setPacketTimeout(txpacket[PKT_PARAMETER0 + 1] + 6)
        else:
            self.port.setPacketTimeout(6)  # HEADER0 HEADER1 ID LENGTH ERROR CHECKSUM

        # rx packet
        while True:
            rxpacket, result = self.readPacket()
            if result != COMM_SUCCESS or txpacket[PKT_ID] == rxpacket[PKT_ID]:
                break

        if result == COMM_SUCCESS and txpacket[PKT_ID] == rxpacket[PKT_ID]:
            error = rxpacket[PKT_ERROR]

        return rxpacket, result, error
    
    def write(self, dxl_id, address, length):
        txpacket = [0]*8

        if dxl_id >= BROADCAST_ID:
            return COMM_NOT_AVAILABLE
        
        txpacket[PKT_ID] = dxl_id
        txpacket[PKT_LENGTH] = 4
        txpacket[PKT_INSTRUCTION] = INST_READ
        txpacket[PKT_PARAMETER0 + 0] = address
        txpacket[PKT_PARAMETER0 + 1] = length

        result = self.writePacket(txpacket)

        # set packet timeout
        if result == COMM_SUCCESS:
            port.setPacketTimeout(length + 6)

        return result
    
    def read(self, dxl_id, length):
        result = COMM_TX_FAIL
        error = 0

        rxpacket = None
        data = []

        while True:
            rxpacket, result = self.readPacket()

            if result != COMM_SUCCESS or rxpacket[PKT_ID] == dxl_id:
                break

        if result == COMM_SUCCESS and rxpacket[PKT_ID] == dxl_id:
            error = rxpacket[PKT_ERROR]

            data.extend(rxpacket[PKT_PARAMETER0: PKT_PARAMETER0 + length])

        return data, result, error

    def readAndWrite(self, dxl_id, address, length):
        txpacket = [0] * 8
        data = []

        if dxl_id >= BROADCAST_ID:
            return data, COMM_NOT_AVAILABLE, 0

        txpacket[PKT_ID] = dxl_id
        txpacket[PKT_LENGTH] = 4
        txpacket[PKT_INSTRUCTION] = INST_READ
        txpacket[PKT_PARAMETER0 + 0] = address
        txpacket[PKT_PARAMETER0 + 1] = length

        rxpacket, result, error = self.readAndWritePacket(txpacket)
        if result == COMM_SUCCESS:
            error = rxpacket[PKT_ERROR]

            data.extend(rxpacket[PKT_PARAMETER0: PKT_PARAMETER0 + length])

        return data, result, error

    def ping(self, dxl_id):
        model_nr = 0
        error = 0

        txpacket = [0]*6

        if dxl_id >= BROADCAST_ID:
            return model_nr, COMM_NOT_AVAILABLE, error

        txpacket[PKT_ID] = dxl_id
        txpacket[PKT_LENGTH] = 2
        txpacket[PKT_INSTRUCTION] = INST_PING

        rxpacket, result, error = self.readAndWritePacket(txpacket)

        if result == COMM_SUCCESS:
            data_read, result, error = self.readAndWrite(dxl_id, 0, 2)
            if result == COMM_SUCCESS:
                model_nr = DXL_MAKEWORD(data_read[0], data_read[1])

        return model_nr, result, error


    def close(self):
        self.port.closePort()
        GPIO.cleanup()

