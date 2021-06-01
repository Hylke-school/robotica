import socket
import threading


class Socket:
    def __init__(self, ip, port):
        self.daemon = True
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.ip, self.port))
        self.thread = None
        self.data = None
        self.locked = False

    def start_loop(self):
        self.thread = threading.Thread(target=self.loop, daemon=True)
        self.thread.start()

    def loop(self):
        while True:
            self.data, addr = self.sock.recvfrom(1024)

    def stop_loop(self):
        self.join()

    def get_data(self):
        #data = self.data
        return self.data
