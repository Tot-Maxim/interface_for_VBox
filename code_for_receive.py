import fcntl
import os
import struct
import subprocess
import time

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
subprocess.check_call('ifconfig tap0 192.168.1.1 pointopoint 192.168.1.1 up', shell=True)
# current_dir = os.path.dirname(os.path.abspath(__file__))
current_dir = '/media/sf_FilePack'
path_dir = os.path.join(current_dir, 'data_file.txt')

while True:
    with open(path_dir, 'rb') as file:
        packet = file.read()

    # Вывод содержимое массива пакетов после операции чтения
    print("raw_read_data:", ''.join('{:02x} '.format(x) for x in packet))

    os.write(tun.fileno(), bytes(packet))
    # Вывод содержимое массива пакетов после операции записи
    # print("raw_send_data:", ''.join('{:02x} '.format(x) for x in packet))

    time.sleep(2.5)