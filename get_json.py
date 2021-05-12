from receive_remote.py import MySocket

ip = "141.252.29.5"
port = 5535

socket = MySocket(ip, port)
try:
    socket.connect_socket()
    while True:
        data = socket.get_data()
        print(data)
finally:
    socket.close_socket()
