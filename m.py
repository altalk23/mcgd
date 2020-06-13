import socket
from pynput.keyboard import Key, Listener
from threading import Thread

ip = "192.168.1.30"
address = (ip, 55000)
buffersize = 16
br = True

def client():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(address)

    def on_press(key):
        if key == Key.space:
            s.send(b"press")
        elif key == Key.esc:
            s.send(b"stop")
            br = False
            return False

    def on_release(key):
        if key == Key.space:
            s.send(b"release")

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    while br:
        data = s.recv(buffersize)
        if data == b"stop": break
    s.close()

def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(address)
    s.listen(1)
    conn, addr = s.accept()
    print('Connection address:', addr)

    while br:
        data = conn.recv(buffersize)
        print("received data (server):", data)

        if data == b"stop": break
        elif data == b"kill":
            print("club penguin is kil")

    conn.close()

Thread(target=server).start()
Thread(target=client).start()
