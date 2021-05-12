from receive_remote import Socket

class JSON:
    def __init__(self):
        self.ip = "141.252.29.5"
        self.port = 5535
        self.socket = Socket(self.ip, self.port)
        try:
            self.socket.connect_socket()
            while True:
                self.data = self.socket.get_data()
        finally:
            self.socket.close_socket()

    def get_json(self):
        return self.data

