#!/usr/bin/env python3
import os
from socket import *
from struct import unpack
import argparse
import time

parser = argparse.ArgumentParser(description='Server socket manager script')
parser.add_argument('--port', type=int, default=5050, help='TCP port listening')
parser.add_argument('--ip', type=str, default='10.1.1.8', help='Source IP address')

args = parser.parse_args()

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
                    print('Input data ...')
                    bs = connection.recv(8)
                    (length_data,) = unpack('>Q', bs)
                    time_start = time.time()

                    length_name = connection.recv(8)
                    (length_name,) = unpack('>Q', length_name)
                    name = connection.recv(length_name)
                    name_file = name.decode('utf-8')

                    data = b''
                    print(f'File size: {length_data} byte')
                    while len(data) < length_data:
                        to_read = length_data - len(data)
                        data += connection.recv(
                            4096 if to_read > 4096 else to_read)
                        print(len(data))
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


def start_server(address: str, port: int):
    sp = ServerProtocol()
    sp.listen(address, port)
    print(f'Server listen {address, port}')
    sp.handle_images()


if __name__ == '__main__':
    start_server(args.ip, args.port)
