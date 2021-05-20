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
        self.looping = True

    def start_loop(self):
        self.thread = threading.Thread(target=self.loop, daemon=True)
        self.thread.start()

    def loop(self):
        while self.looping:
            self.data, addr = self.sock.recvfrom(1024)
            # self.lock.acquire()
            # self.data = data
            # self.lock.release()
            # f = open("data.json", "w")
            # f.write(data.decode('utf-8'))
            # f.close()

    def stop_loop(self):
        self.join()

    def get_data(self):
        self.looping = False
        data = self.data
        self.looping = True
        # self.lock.acquire()
        # value = self.data
        # self.lock.release()
        # f = open("data.json", "r")
        # value = f.read()
        # f.close()
        return data
