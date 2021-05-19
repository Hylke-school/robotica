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
        threading.Thread.__init__(self)
        self.start()

    def run(self):
        while True:
            data, addr = self.sock.recvfrom(1024)
            print(data)
            f = open("data.json", "w")
            f.write(data.decode('utf-8'))
            f.close()

    def stop_loop(self):
        self.join()
