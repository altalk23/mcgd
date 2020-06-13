import socket
from PIL import ImageGrab
from pynput.keyboard import Key, Controller, Listener
from threading import Thread

ip = "192.168.1.35"
address = (ip, 55000)
buffersize = 16
br = True

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
    s.bind(address)
    s.listen(2)
    conn, addr = s.accept()
    print('Connection address:', addr)

    while br:
        data = conn.recv(buffersize)
        print("received data (server):", data)

        if data == b"stop": break
        elif data == b"press":
            keyboard.press(Key.space)
            print("press")

        elif data == b"release":
            keyboard.release(Key.space)
            print("release")
    conn.close()
    s.close()


Thread(target=server).start()
Thread(target=client).start()
