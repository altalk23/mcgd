class GD:
    def __init__(self, buffersize):
        self.buffersize = buffersize
        self.stop = False

    def client(self, address):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(address)

        def on_press(key):
            if key == Key.delete:
                print("send data (client): stop")
                s.send(b"stop")
                self.stop = True
                return False

        with Listener(on_press=on_press) as listener:
            listener.join()

        while not self.stop:
            col = ImageGrab.grab(bbox =(1000, 1000, 1001, 1001)).getpixel((0, 0))
            if col == (135, 44, 234):
                print("send data (client): kill")
                s.send(b"kill")
        s.close()

    def server(self, address):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(address)
        s.listen(1)
        conn, addr = s.accept()
        print('Connection address:', addr)

        keyboard = Controller()
        pressed = False
        while not self.stop:
            data = conn.recv(self.buffersize)
            print("received data (server):", data)

            if data == b"stop":
                self.stop = True
                break

            if data == b"press" and not pressed:
                keyboard.press(Key.space)
                print("press")
                pressed = True
            elif data == b"release" and pressed:
                keyboard.release(Key.space)
                print("release")
                pressed = False
        conn.close()
        s.close()

class MC:
    def __init__(self, buffersize):
        self.buffersize = buffersize
        self.stop = False

    def client(self, address):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(address)

        def on_press(key):
            if key == Key.space:
                print("send data (client): press")
                s.send(b"press")

            elif key == Key.delete:
                print("send data (client): stop")
                s.send(b"stop")
                self.stop = False
                return False

        def on_release(key):
            if key == Key.space:
                print("send data (client): release")
                s.send(b"release")

        with Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()

        while not self.stop:
            pass
        s.close()

    def server(self, address):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(address)
        s.listen(1)
        conn, addr = s.accept()
        print('Connection address:', addr)

        while not self.stop:
            data = conn.recv(self.buffersize)
            print("received data (server):", data)

            if data == b"stop": break

            if data == b"kill":
                print("club penguin is kil")

        conn.close()
        s.close()

class Control:
    def set_address(self):
        self.client_address = (ip_entry.get(), int(port_entry.get()))
        self.server_address = (ip, int(port_entry.get()))
        print("set address")

    def run_client():
        Thread(target=self.process.client, args=[self.client_address]).start()
        client_button['state'] = 'disabled'

    def run_server():
        Thread(target=self.process.server, args=[self.server_address]).start()
        server_button['state'] = 'disabled'

    def stop():
        self.process.stop = True
