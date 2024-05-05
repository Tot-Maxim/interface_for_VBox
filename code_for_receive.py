from array import array
import fcntl
import os
import struct
import subprocess
import time

# Заданные переменные
source_port = 0x0a1a
destination_port = 0xde3c
sequence_number = 0xf05d0a1a
acknowledgment_number = 0xde3cf05d
flags = 0x800
checksum = 0x6f7

# Некоторые константы, используемые для ioctl файла устройства. Я получил их с помощью простой программы на Cи
TUNSETIFF = 0x400454ca
TUNSETOWNER = TUNSETIFF + 2
IFF_TUN = 0x0001
IFF_TAP = 0x0002
IFF_NO_PI = 0x1000

# Открытие файла, соответствующего устройству TUN, в двоичном режиме чтения/записи без буферизации.
tun = open('/dev/net/tun', 'r+b', buffering=0)
ifr = struct.pack('16sH', b'tap0', IFF_TAP | IFF_NO_PI)
fcntl.ioctl(tun, TUNSETIFF, ifr)
fcntl.ioctl(tun, TUNSETOWNER, 1000)

# Поднятие tap0 и назначение адреса
subprocess.check_call('ifconfig tap0 10.1.1.8 pointopoint 10.1.1.8 up', shell=True)


def write_packet_to_file(packet, file_path):
    with open(file_path, 'wb') as file:
        file.write(bytes(packet))


def read_packet_to_file(path_dir):
    with open(path_dir, 'rb') as file:
        packet = file.read()
        print("raw_read_data:", ''.join('{:02x} '.format(x) for x in packet))
    return packet


last_read_time = 0
while True:
    current_dir = '/media/sf_FilePack'
    path_dir = os.path.join(current_dir, 'data_file_from_host_to_vb.txt')
    current_time = os.path.getmtime(path_dir)

    if current_time != last_read_time:

        last_read_time = current_time
        packet = read_packet_to_file(path_dir)
        os.write(tun.fileno(), bytes(packet))
    else:
        pass    # print("Файл не был изменен")

    # TCP_packet = array('B', os.read(tun.fileno(), 2048))
    # print("raw_read_data:", ''.join('{:02x} '.format(x) for x in TCP_packet))
    #
    # path_dir = os.path.join(current_dir, 'data_file_from_vb_to_host.txt')
    #
    # write_packet_to_file(TCP_packet, path_dir)

    time.sleep(0.1)