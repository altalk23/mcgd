import socket
from threading import Thread
TCP_IP = '192.168.0.30'
TCP_PORT = 55000
BUFFER_SIZE = 64
MESSAGE = b"Hello, World!"

def client():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(MESSAGE)

    data = s.recv(BUFFER_SIZE)
    s.close()
    print("received data (client):", data)

def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)

    conn, addr = s.accept()
    print('Connection address:', addr)
    while 1:
        data = conn.recv(BUFFER_SIZE)
        print("received data (server):", data)
        if not data: break
        conn.send(data)  # echo
    conn.close()


Thread(target=server).start()
