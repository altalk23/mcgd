import socket
from PIL import ImageGrab
from pynput.keyboard import Key, Controller, Listener
from threading import Thread
import tkinter as tk

address = None
server_address = None
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
    s.bind(server_address)
    s.listen(2)
    conn, addr = s.accept()
    print('Connection address:', addr)

    keyboard = Controller()

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


window = tk.Tk()
host_text = tk.Label(window, text="Host IP:")
host_entry = tk.Entry(window)
host_text.pack()
host_entry.pack()
ip_text = tk.Label(window, text="Connection IP:")
ip_entry = tk.Entry(window)
ip_text.pack()
ip_entry.pack()
port_text = tk.Label(window, text="Connection Port:")
port_entry = tk.Entry(window)
port_text.pack()
port_entry.pack()

def set_address():
    global address, server_address
    address = (ip_entry.get(), int(port_entry.get()))
    server_address = (host_entry.get(), int(port_entry.get()))
    print("set address")

address_button = tk.Button(window, text="Set Address", command=set_address)
address_button.pack()

def run_client():
    print("start client")
    Thread(target=client).start()

def run_server():
    global address
    address = (ip_entry.get(), int(port_entry.get()))
    print("start server")
    Thread(target=server).start()

client_button = tk.Button(window, text="Run Client", command=run_client)
server_button = tk.Button(window, text="Run Server", command=run_server)
client_button.pack()
server_button.pack()
window.mainloop()
