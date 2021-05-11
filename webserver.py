# Python 3 server example
import socket

ip = "141.252.29.5"
port = 80
buffer_size = 20

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((ip, port))
sock.listen(1)

conn, addr = sock.accept()
print('Connection address:', addr)
while 1:
    while 1:
        data = conn.recv(buffer_size)
        if not data: break
        print(data)
conn.close()
