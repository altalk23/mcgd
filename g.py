import socket
from PIL import ImageGrab
from pynput.keyboard import Key, Controller, Listener
from threading import Thread

keyboard = Controller()

address = ("192.168.1.35", 2050)
print("Starting connection up on %s port %s" % address)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(address)
sock.listen(1)


def on_press(key):
    if key == Key.esc:
        sock.close()
with Listener(on_press=on_press) as listener:
    listener.join()

def m_listener():
    while True:
        try:
            data = socket.recv(8)
            print(f"Received: {data}")
            if data == b"p":
                keyboard.press(Key.space)
            elif data == b"r":
                keyboard.release(Key.space)
        except:
            pass

def g_sender():
    while True:
        col = ImageGrab.grab(bbox =(1000, 1000, 1001, 1001)).getpixel((0, 0))
        if col == (135, 44, 234):
            try:
                sock.send(b"k")
            except:
                pass

Thread(target=m_listener).start()
Thread(target=g_sender).start()
