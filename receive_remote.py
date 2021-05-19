import socket
import threading


def get_data():
    f = open("data.json", "r")
    value = f.read()
    f.close()
    return value


class Socket:
    def __init__(self, ip, port):
        self.daemon = True
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.ip, self.port))
        self.thread = None

    def start_loop(self):
        self.thread = threading.Thread(target=self.loop, daemon=True)
        self.thread.start()

    def loop(self):
        while True:
            data, addr = self.sock.recvfrom(1024)
            f = open("data.json", "w")
            f.write(data.decode('utf-8'))
            f.close()

    def stop_loop(self):
        self.join()
