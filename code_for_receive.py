import time
from array import array
import fcntl
import os
import struct
import subprocess


current_dir = '/media/sf_FilePack'

# Некоторые константы
TUNSETIFF = 0x400454ca
TUNSETOWNER = TUNSETIFF + 2
IFF_TUN = 0x0001
IFF_TAP = 0x0002
IFF_NO_PI = 0x1000
state = 1
temp_read = b''
temp_write = b''
ast_read_time = 0

# Открытие файла, соответствующего устройству TUN, в двоичном режиме чтения/записи без буферизации.
tun = open('/dev/net/tun', 'r+b', buffering=0)
ifr = struct.pack('16sH', b'tap0', IFF_TAP | IFF_NO_PI)
fcntl.ioctl(tun, TUNSETIFF, ifr)
fcntl.ioctl(tun, TUNSETOWNER, 1000)

# Поднятие tap0 и назначение адреса
subprocess.check_call('ifconfig tap0 10.1.1.8 pointopoint 10.1.1.7 up', shell=True)


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def write_packet_to_file(packet, file_path):
    global temp_write, state
    with open(file_path, 'wb') as file:
        if temp_write != packet:
            temp_write = packet
            file.write(packet)
            print(bcolors.WARNING + "raw_write_data:" + bcolors.ENDC, ''.join('{:02x} '.format(x) for x in packet))
            state = 3
    return state


def read_packet_to_file(path_dir):
    global temp_read
    with open(path_dir, 'rb') as file:
        to_TCP = file.read()
        if temp_read != to_TCP:
            temp_read = to_TCP
            print(bcolors.OKGREEN + "raw_read_data:" + bcolors.ENDC, ''.join('{:02x} '.format(x) for x in to_TCP))
    return to_TCP


if __name__ == "__main__":
    while True:
        print('1',state)
        if state == 1:
            from_TCP = array('B', os.read(tun.fileno(), 2048))
            if from_TCP:
                state = 2
        print('2',state)
        if state == 2:
            path_dir = os.path.join(current_dir, 'from_virtual.docx')
            state = write_packet_to_file(from_TCP, path_dir)
        print('3',state)
        if state == 3:
            path_dir = os.path.join(current_dir, 'from_host.docx')
            to_TCP = read_packet_to_file(path_dir)
            if to_TCP:
                state = 4
            else:
                state = 1
        print('4',state)
        if state == 4:
            os.write(tun.fileno(), bytes(to_TCP))
            state = 1
        time.sleep(0.1)

tun.close()
