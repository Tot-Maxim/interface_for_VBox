import fcntl
import os
import struct
import subprocess

# Объявление глобальных переменных
DST_IP = '10.1.1.7'
SRC_IP = '10.1.1.8'


class bcolors:  # Класс с константами для цветовой кодировки в консоли
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


class TAP_Manager:
    def __init__(self):  # Инициализируем значения переменных
        self.src_ip = SRC_IP
        self.dst_ip = DST_IP
        self.tun_setup()

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

    def read_from_TCP(self, tap_lock, current_dir, file_path):
        path_dir = os.path.join(current_dir, file_path)

        while True:
            try:
                from_TCP = os.read(self.tun_in.fileno(), 1522)
            except OSError as e:
                print(bcolors.FAIL + f"Error writing to tap: {e}" + bcolors.ENDC)
            else:
                with open(path_dir, 'ab+') as file:
                    try:
                        tap_lock.acquire()
                        fcntl.lockf(file, fcntl.LOCK_EX | fcntl.LOCK_NB)
                        file.write(from_TCP)
                        print(bcolors.OKGREEN + 'Записанные данные в {path_dir}: ' + bcolors.ENDC,
                              ''.join('{:02x} '.format(x) for x in from_TCP))
                    finally:
                        fcntl.lockf(file, fcntl.LOCK_UN)
                        tap_lock.release()

    def read_from_file(self, tap_lock, current_dir, file_path):
        path_dir = os.path.join(current_dir, file_path)

        while True:
            with open(path_dir, 'rb+') as file:
                content = file.read()
                file.seek(0)
                file.truncate()

            if content:
                try:
                    print(bcolors.WARNING + f'Read data from {path_dir}:' + bcolors.ENDC,
                          ' '.join('{:02x}'.format(x) for x in content))
                    tap_lock.acquire()
                    os.write(self.tun_in.fileno(), bytes(content))
                except OSError as e:
                    print(bcolors.FAIL + f"Error writing to tap: {e}" + bcolors.ENDC)
                finally:
                    tap_lock.release()
