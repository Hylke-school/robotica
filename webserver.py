# Python 3 server example
import socket

ip = "141.252.29.5"
port = 5535
buffer_size = 4096

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((ip, port))
sock.listen(1)

# print('Connection address:', ip)
while True:
    conn, addr = sock.accept()
    while True:
        data = conn.recv(buffer_size)
        if not data: break
        print(data)

conn.close()
