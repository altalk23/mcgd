import socket
from pynput.keyboard import Key, Listener
from helper import *
from config import *

def client():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(address)

    def on_press(key):
        if key == Key.space:
            print("send data (client): press")
            s.send(b"press")

        elif key == Key.esc:
            global br
            print("send data (client): stop")
            s.send(b"stop")
            br = False
            return False

    def on_release(key):
        if key == Key.space:
            print("send data (client): release")
            s.send(b"release")

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    while br:
        pass
    s.close()


def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(server_address)
    s.listen(1)
    conn, addr = s.accept()
    print('Connection address:', addr)

    while br:
        data = conn.recv(buffersize)
        print("received data (server):", data)

        if data == b"stop": break

        if data == b"kill":
            print("club penguin is kil")

    conn.close()
    s.close()

control_panel(client, server)
