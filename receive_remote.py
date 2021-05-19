import socket
import threading
from threading import Lock


class Socket:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.ip, self.port))
        self.thread = None

    def start_loop(self):
        self.thread = threading.Thread(target=self.loop)

    def loop(self):
        while True:
            data, addr = self.sock.recvfrom(1024)
            print(data)
            f = open("data.json")
            f.write(data, "w")
            f.close()

    def stop_loop(self):
        self.thread.join()

    @staticmethod
    def get_data():
        f = open("data.json")
        value = f.read()
        f.close()
        return value
