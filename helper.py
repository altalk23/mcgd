import tkinter as tk
import socket
from threading import Thread


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip = s.getsockname()[0]
s.close()

def control_panel(client, server):
    address = None
    server_address = None

    window = tk.Tk()
    host_text = tk.Label(window, text=f"Host IP: {ip}")
    host_text.pack()
    ip_text = tk.Label(window, text="Connection IP:")
    ip_entry = tk.Entry(window)
    ip_text.pack()
    ip_entry.pack()
    port_text = tk.Label(window, text="Connection Port:")
    port_entry = tk.Entry(window)
    port_text.pack()
    port_entry.pack()

    def set_address():
        global address
        global server_address
        address = (ip_entry.get(), int(port_entry.get()))
        server_address = (ip, int(port_entry.get()))
        print(server_address)
        print("set address")

    address_button = tk.Button(window, text="Set Address", command=set_address)
    address_button.pack()


    def run_client():
        global address
        Thread(target=client, args=[address]).start()
        client_button['state'] = 'disabled'


    def run_server():
        global server_address
        Thread(target=server, args=[server_address]).start()
        server_button['state'] = 'disabled'

    client_button = tk.Button(window, text="Run Client", command=run_client)
    server_button = tk.Button(window, text="Run Server", command=run_server)
    client_button.pack()
    server_button.pack()
    window.mainloop()
