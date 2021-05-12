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
        data = str(self.conn.recv(self.buffer_size))
        start_index = data.rfind('{')
        last_json = data[start_index:]
        end_index = last_json.rfind('}')
        return_data = last_json[:end_index+1]
        return return_data

    def close_socket(self):
        print("Closing socket")
        self.sock.close()
