import fcntl
import os
import struct
import subprocess


class Bcolors:  # Класс с константами для цветовой кодировки в консоли
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


class TAP_Manager:
    def __init__(self, src_ip, dst_ip):  # Инициализируем значения переменных
        self.tun_in = None
        self.src_ip = src_ip
        self.dst_ip = dst_ip
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

    def read_from_tcp(self, current_dir, file_path):
        path_dir = os.path.join(current_dir, file_path)

        try:
            from_tcp = os.read(self.tun_in.fileno(), 2048)
        except OSError as e:
            print(Bcolors.FAIL + f"Ошибка при записи в tap интерфейс: {e}" + Bcolors.ENDC)
        else:
            with open(path_dir, 'ab+') as file:
                file.write(from_tcp)
                print(Bcolors.OKGREEN + f'Записанные данные в {path_dir}: ' + Bcolors.ENDC,
                      ''.join('{:02x} '.format(x) for x in from_tcp))

    def read_from_file(self, current_dir, file_path):
        path_dir = os.path.join(current_dir, file_path)

        with open(path_dir, 'rb+') as file:
            content = file.read()
            file.seek(0)
            file.truncate()

        if content:
            try:
                print(Bcolors.WARNING + f'Прочитанные данные из {path_dir}:' + Bcolors.ENDC,
                      ' '.join('{:02x}'.format(x) for x in content))
                os.write(self.tun_in.fileno(), bytes(content))
            except OSError as e:
                print(Bcolors.FAIL + f"Ошибка при прочтении tap интерфейса: {e}" + Bcolors.ENDC)
