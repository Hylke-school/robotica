import random

from receive_remote import Socket


class JSON:
    def __init__(self):
        self.ip = "141.252.29.30"
        self.port = 5535
        self.data = None
        self.socket = Socket(self.ip, self.port)
        self.socket.connect_socket()

    def get_json(self):
        self.data = self.socket.get_data()
        # self.data = "{\"pot\": " + str(random.randrange(0, 1023)) + "}"
        return self.data
