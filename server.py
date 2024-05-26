import os
import time
from tkinter import *
from socket import *
from struct import unpack

ip_address = '10.1.1.8'
TCP_port = 5050


class ServerProtocol:

    def __init__(self):
        self.socket = None
        self.output_dir = '/home/serverside/PycharmProjects/interface_for_VBox/serv_recevie'
        self.file_num = 1

    def listen(self, server_ip, server_port):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind((server_ip, server_port))
        self.socket.listen(1)

    def handle_images(self):

        try:
            while True:
                (connection, addr) = self.socket.accept()
                try:
                    print('Input data')
                    bs = connection.recv(8)
                    (length,) = unpack('>Q', bs)
                    time_start = time.time()

                    lname = connection.recv(8)
                    (lenname,) = unpack('>Q', lname)
                    name = connection.recv(lenname)
                    name_file = name.decode('utf-8')

                    data = b''
                    print(f'File size: {length} byte')
                    while len(data) < length:
                        to_read = length - len(data)
                        data += connection.recv(
                            4096 if to_read > 4096 else to_read)
                        print(f'Receive data {len(data)} / {length}')
                    time_end = time.time()
                    print(f'File {name_file} save in {self.output_dir}')
                    print(f'Time transfer: {time_end - time_start} c')
                finally:
                    connection.shutdown(SHUT_WR)
                    connection.close()

                with open(os.path.join(self.output_dir, name.decode('utf-8')), 'wb') as fp:
                    fp.write(data)
                    print('File write success')

                self.file_num += 1
        finally:
            self.close()

    def close(self):
        self.socket.close()
        self.socket = None


def start_server():
    print('START SERVER')
    sp = ServerProtocol()
    sp.listen(ip_address, TCP_port)
    print(f'Server listen {ip_address, TCP_port}')
    sp.handle_images()

def center_button(event=None):
    x_coordinate = (window.winfo_width() - start_button.winfo_reqwidth()) // 2
    y_coordinate = (window.winfo_height() - start_button.winfo_reqheight()) // 2
    start_button.place(x=x_coordinate, y=y_coordinate)

window = Tk()
window.geometry("820x450")
window.configure(background='black')

start_button = Button(window, text='Start server', command=start_server, bg='white', fg='black')

window.bind("<Configure>", center_button)

window.mainloop()
