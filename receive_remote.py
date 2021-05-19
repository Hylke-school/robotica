import socket
import threading
from threading import Lock


class Socket:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.ip, self.port))
        self.data = None
        self.thread = None
        self.lock = Lock()

    def start_loop(self):
        self.thread = threading.Thread(target=self.loop)

    def loop(self):
        while True:
            self.lock.acquire()
            self.data, addr = self.sock.recvfrom(1024)
            self.lock.release()

    def stop_loop(self):
        self.thread.join()

    def get_data(self):
        self.lock.acquire()
        return self.data
        self.lock.release()
