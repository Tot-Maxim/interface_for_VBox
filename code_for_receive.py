from array import array
import fcntl
import os
import struct
import subprocess
import time
import tempfile
import shutil

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
            print(bcolors.FAIL + "Break")


def write_packet_to_file(packet, file_path):
    directory = os.path.dirname(file_path)
    flag_file = os.path.join(directory, 'flag_to_host.txt')

    if not os.path.exists(flag_file):
        try:
            with AtomicWrite(file_path, 'wb') as file:
                for x in packet:
                    file.write(bytes([x]))
                # Вывод содержимого массива пакетов после операции записи
                print(bcolors.WARNING + "raw_write_data:" + bcolors.ENDC,
                      ''.join('{:02x} '.format(x) for x in TCP_packet))

            # Создаем файл-флаг после успешной записи
            open(flag_file, 'w').close()
        except Exception as e:
            print(bcolors.FAIL + "Failed to write data. Retrying in 0.1 seconds...")
            time.sleep(0.1)
    else:
        pass


def read_packet_to_file(path_dir):
    directory = os.path.dirname(path_dir)
    flag_file = os.path.join(directory, 'flag_to_vb.txt')

    if os.path.exists(flag_file):
        os.remove(flag_file)
        with open(path_dir, 'rb') as file:
            packet = file.read()
            os.write(tun.fileno(), bytes(packet))
            print(bcolors.OKGREEN + "raw_read_data:" + bcolors.ENDC, ''.join('{:02x} '.format(x) for x in packet))
        return packet
    else:
        print(bcolors.FAIL + "Flag file does not exist. Skipping reading.")
        return None


last_read_time = 0
while True:
    current_dir = '/media/sf_FilePack'
    path_dir = os.path.join(current_dir, 'data_file.txt')
    current_time = os.path.getmtime(path_dir)

    if current_time != last_read_time:
        last_read_time = current_time
        packet = read_packet_to_file(path_dir)
    else:
        TCP_packet = array('B', os.read(tun.fileno(), 2048))
        path_dir = os.path.join(current_dir, 'data_file_from_vb_to_host.txt')
        write_packet_to_file(TCP_packet, path_dir)

    time.sleep(0.1)