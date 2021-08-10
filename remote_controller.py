import socket
import threading


class RemoteController:
    def __init__(self):
        self.ip = "141.252.29.30"
        self.port = 5355
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.ip, self.port))
        self.data = None
        self.thread = None
        self.thread = threading.Thread(target=self.__loop, daemon=True)
        self.thread.start()

    def __loop(self):
        """"""
        while True:
            self.data, address = self.sock.recvfrom(1024)

    def stop_loop(self):
        self.thread.join()

    def get_data(self):
        return self.data
