import socket


class Socket:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.buffer_size = 4096
        self.sock = None
        self.conn = None
        self.addr = None

    def connect_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.ip, self.port))
        self.sock.listen(1)
        self.conn, self.addr = self.sock.accept()

    def get_data(self):
        data = self.conn.recv(self.buffer_size)
        return data

    def close_socket(self):
        print("Closing socket")
        self.sock.close()
