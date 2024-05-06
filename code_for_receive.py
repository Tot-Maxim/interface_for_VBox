from array import array
import fcntl
import os
import struct
import subprocess
import tempfile
import shutil

# Заданные переменные
source_port = 0x0a1a
destination_port = 0xde3c
sequence_number = 0xf05d0a1a
acknowledgment_number = 0xde3cf05d
flags = 0x800
checksum = 0x6f7
state = 1
current_dir = '/media/sf_FilePack'
path_dir = os.path.join(current_dir, 'data_file.docx')

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


class AtomicWrite():
    def __init__(self, path, mode='w', encoding='utf-8'):
        self.path = path
        self.mode = mode if mode == 'wb' else 'w'
        self.encoding = encoding

    def __enter__(self):
        self.temp_file = tempfile.NamedTemporaryFile(
            mode=self.mode,
            encoding=self.encoding if self.mode != 'wb' else None,
            delete=False
        )
        return self.temp_file

    def __exit__(self, exc_type, exc_message, traceback):
        self.temp_file.close()
        if exc_type is None:
            with open(self.temp_file.name, 'rb') as src, open(self.path, 'wb') as dest:
                shutil.copyfileobj(src, dest)
            os.unlink(self.temp_file.name)
            os.chmod(self.path, 0o664)
        else:
            os.unlink(self.temp_file.name)
            print(bcolors.FAIL + "Break" + bcolors.ENDC)


def write_packet_to_file(packet, file_path):
    global state
    directory = os.path.dirname(file_path)
    flag_file = os.path.join(directory, 'flag_to_host.txt')
    if os.path.exists(flag_file):
        try:
            with AtomicWrite(file_path, 'wb') as file:
                for x in packet:
                    file.write(bytes([x]))
                # Вывод содержимого массива пакетов после операции записи
                print(bcolors.WARNING + "raw_write_data:" + bcolors.ENDC,
                      ''.join('{:02x} '.format(x) for x in packet))
                state = 3
        except:
            print(bcolors.FAIL + "Failed to write data" + bcolors.ENDC)
    return state


def read_packet_to_file(path_dir):
    directory = os.path.dirname(path_dir)
    flag_file = os.path.join(directory, 'flag_to_vb.txt')
    if os.path.exists(flag_file):
        with open(path_dir, 'rb') as file:
            to_TCP = file.read()
            print(bcolors.OKGREEN + "raw_read_data:" + bcolors.ENDC, ''.join('{:02x} '.format(x) for x in to_TCP))
        os.remove(flag_file)
        return to_TCP


while True:
    print(state)
    if state == 1:
        from_TCP = array('B', os.read(tun.fileno(), 2048))
        if from_TCP:
            state = 2
    if state == 2:
        state = write_packet_to_file(from_TCP, path_dir)
    if state == 3:
        to_TCP = read_packet_to_file(path_dir)
        print(to_TCP)
        if to_TCP:
            state =4
    if state == 4:
        os.write(tun.fileno(), bytes(to_TCP))
        state = 1


tun.close()
