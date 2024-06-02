import fcntl
import os
import struct
import subprocess
import serial
from base64 import b64decode, b64encode


class Bcolors:  # Класс с константами для цветовой кодировки в консоли
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


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
        try:
            self.ser = serial.Serial(self.serial_port, self.baud_rate)
            return self.ser
        except Exception as e:
            print(Bcolors.FAIL + f"Ошибка при попытке создать последовательный порт: {e}" + Bcolors.ENDC)

    def read_from_tcp(self):
        try:
            from_tcp = os.read(self.tun_in.fileno(), 2048)
            return from_tcp
        except OSError as e:
            print(Bcolors.FAIL + f"Ошибка при чтении и tap интерфейса: {e}" + Bcolors.ENDC)

    def read_from_serial(self):
        try:
            receive_base64 = b''
            while True:
                data_rx = self.ser.read(1)
                receive_base64 += data_rx
                if data_rx == b'\x00':
                    break
                if data_rx == b'#':
                    break

            receive_base64 = receive_base64.rstrip(b'#')  # Remove the '#' symbol before decoding
            decoded_data = b64decode(receive_base64)
            return decoded_data
        except Exception as e:
            print(Bcolors.FAIL + f"Ошибка при попытке прочитать из {self.serial_port}: {e}" + Bcolors.ENDC)

    def write_to_tcp(self, receive_base64):
        try:
            os.write(self.tun_in.fileno(), bytes(receive_base64))
            print(Bcolors.WARNING + f'Записанные данные в TAP:' + Bcolors.ENDC,
                  ' '.join('{:02x}'.format(x) for x in receive_base64))
        except OSError as e:
            print(Bcolors.FAIL + f"Ошибка при попытке записать данные в TAP интерфейс: {e}" + Bcolors.ENDC)

    def write_to_uart(self, data_from_tcp):
        try:
            send_base64 = b64encode(data_from_tcp) + b'#'
            self.ser.write(send_base64)
            print(Bcolors.OKGREEN + f'Записанные данные в {self.serial_port}:' + Bcolors.ENDC,
                  ' '.join('{:02x}'.format(x) for x in data_from_tcp))
        except Exception as e:
            print(Bcolors.FAIL + f"Ошибка при попытке записать данные в {self.serial_port}: {e}" + Bcolors.ENDC)
