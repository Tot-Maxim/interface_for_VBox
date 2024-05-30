import fcntl
import os
import struct
import subprocess
import serial
import base64
import time


class Bcolors:  # Класс с константами для цветовой кодировки в консоли
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def add_padding(data):
    missing_padding = len(data) % 4
    if missing_padding:
        data += b'=' * (4 - missing_padding)
    return data


class TAP_Manager:
    def __init__(self, src_ip, dst_ip, serial_port, baud_rate):  # Инициализируем значения переменных
        self.ser = None
        self.tun_in = None
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.serial_port = serial_port
        self.baud_rate = baud_rate
        self.tun_setup()
        self.serial_setup()

    def tun_setup(self):
        # Коды для настройки интерфейса
        TUNSETIFF = 0x400454ca
        TUNSETOWNER = TUNSETIFF + 2
        IFF_TUN = 0x0001
        IFF_TAP = 0x0002
        IFF_NO_PI = 0x1000

        self.tun_in = open('/dev/net/tun', 'r+b', buffering=0)
        ifr = struct.pack('16sH', b'tap0', IFF_TAP | IFF_NO_PI)
        fcntl.ioctl(self.tun_in, TUNSETIFF, ifr)
        fcntl.ioctl(self.tun_in, TUNSETOWNER, 1000)
        subprocess.check_call(f'ifconfig tap0 {self.src_ip} pointopoint {self.dst_ip} up', shell=True)
        return self.tun_in

    def serial_setup(self):
        self.ser = serial.Serial(self.serial_port, self.baud_rate)
        return self.ser

    def read_from_tcp(self):
        try:
            from_tcp = os.read(self.tun_in.fileno(), 2048)
            print(Bcolors.WARNING + 'len_tcp:' + Bcolors.ENDC, len(from_tcp))
            return from_tcp
        except OSError as e:
            print(Bcolors.FAIL + f"Ошибка при записи в tap интерфейс: {e}" + Bcolors.ENDC)

    def read_from_serial(self):
        try:
            len_rx = self.ser.in_waiting
            data_rx = self.ser.read(len_rx)
            receive_base64 = base64.b64decode(add_padding(data_rx))
            print('len_rx:', len_rx)
            return receive_base64
        except Exception as e:
            print(Bcolors.FAIL + f"Ошибка при попытке прочитать из {self.serial_port}: {e}" + Bcolors.ENDC)

    def write_to_tcp(self, receive_base64):
        os.write(self.tun_in.fileno(), bytes(receive_base64))
        print(Bcolors.WARNING + f'Записанные данные в TAP:' + Bcolors.ENDC,
              ' '.join('{:02x}'.format(x) for x in receive_base64))

    def write_to_uart(self, data_from_tcp):
        try:
            send_base64 = base64.b64encode(data_from_tcp)
            len_tx = self.ser.write(send_base64)
            ts = (10 / self.baud_rate) * (len_tx + 100) * 10
            time.sleep(ts)
            print(Bcolors.OKGREEN + f'Записанные данные в {self.serial_port}:' + Bcolors.ENDC,
                  ' '.join('{:02x}'.format(x) for x in data_from_tcp))
        except Exception as e:
            print(Bcolors.FAIL + f"Ошибка при попытке записать данные в {self.serial_port}: {e}" + Bcolors.ENDC)