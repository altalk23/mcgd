import socket
from PIL import ImageGrab
from pynput.keyboard import Key, Controller, Listener
from helper import *


pr = False

def client():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(address)

    def on_press(key):
        if key == Key.esc:
            global br
            print("send data (client): stop")
            s.send(b"stop")
            br = False
            return False

    with Listener(on_press=on_press) as listener:
        listener.join()

    while br:
        col = ImageGrab.grab(bbox =(1000, 1000, 1001, 1001)).getpixel((0, 0))
        if col == (135, 44, 234):
            print("send data (client): kill")
            s.send(b"kill")
    s.close()

def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(server_address)
    s.listen(1)
    conn, addr = s.accept()
    print('Connection address:', addr)

    keyboard = Controller()

    while br:
        data = conn.recv(buffersize)
        print("received data (server):", data)

        if data == b"stop": break

        if data == b"press" and not pr:
            keyboard.press(Key.space)
            print("press")
            pr = True
        elif data == b"release" and pr:
            keyboard.release(Key.space)
            print("release")
            pr = False
    conn.close()
    s.close()

control_panel(client, server)
