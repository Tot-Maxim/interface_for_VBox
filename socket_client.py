#!/usr/bin/env python3
from socket import *
from struct import pack
import os
import argparse

parser = argparse.ArgumentParser(description='Client socket manager script')
parser.add_argument('--port', type=int, default=5050, help='TCP port')
parser.add_argument('--ip', type=str, default='10.1.1.7', help='TCP ip address for client')
parser.add_argument('--file', type=str, default='logo.png', help='File Name for send')
args = parser.parse_args()


class ClientProtocol:

    def __init__(self):
        self.socket = None

    def connect(self, server_ip, server_port):
        self.socket = socket(AF_INET, SOCK_STREAM)
        try:
            self.socket.settimeout(100)
            self.socket.connect((server_ip, server_port))
        except:
            print('Connection timed out')

    def close(self):
        self.socket.shutdown(SHUT_WR)
        self.socket.close()
        self.socket = None

    def send_image(self, image_data, file_name):
        # use struct to make sure
        length = pack('>Q', len(image_data))
        self.socket.sendall(length)
        lenname = pack('>Q', len(file_name))
        self.socket.sendall(lenname)

        self.socket.sendall(bytes(file_name.encode()))
        self.socket.sendall(image_data)
        print('Файл успешно отправлен')


def send_file(file_copy: str, address: str, port: int):
    cp = ClientProtocol()
    if file_copy:
        print(f'Отправка файла {file_copy}')
    else:
        print('Введите имя файла')

    current_dir = os.path.dirname(os.path.abspath(__file__))
    path_dir = os.path.join(current_dir, file_copy)


    image_data = None
    try:
        with open(path_dir, 'rb') as file:
            image_data = file.read()
        assert (len(image_data))
    except:
        print('Файл не найден')

    if address:
        print(f'Ip-адрес: {address}')
    else:
        print(f'Введите IP-адрес')
    if port:
        print(f'Порт: {port}')
    else:
        print(f'Введите TCP-порт')

    cp.connect(address, int(port))
    cp.send_image(image_data, file_copy)
    cp.close()
    print('Отправка завершена')


if __name__ == '__main__':
    send_file(args.file, args.ip, args.port)

