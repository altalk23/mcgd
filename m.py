import socket
from pynput.keyboard import Key, Listener
from threading import Thread

address = ("192.168.1.30", 2049)
print("Starting connection up on %s port %s" % address)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(address)
sock.listen(1)

def on_press(key):
    if key == Key.space:
        try:
            sock.send(b"p")
        except:
            pass
    elif key == Key.esc:
        sock.close()
def on_release(key):
    if key == Key.space:
        try:
            sock.send(b"r")
        except:
            pass
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
def g_listener():
    while True:
        try:
            data = socket.recv(8)
            print(f"Received: {data}")
            if data == "k":
                print("kkkkkkkk")
        except:
            pass

Thread(target=g_listener).start()
