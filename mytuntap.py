import fcntl
import os
import struct
import subprocess
import time

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

    def write_packet_to_file(self, packet, file_path):
        lock_file_path = file_path + '.lock'  # Путь к файлу-блокировке

        for _ in range(2):
            try:
                with open(lock_file_path, 'w') as lock_file:
                    #fcntl.flock(lock_file, fcntl.LOCK_EX)  # Получаем эксклюзивную блокировку файла

                    with open(file_path, 'ab+') as file:
                        file.write(packet)
                        file.write(b'\t0t')
                        print(bcolors.WARNING + f'Write data from {file_path}: ' + bcolors.ENDC,
                              ''.join('{:02x} '.format(x) for x in packet))
                #fcntl.flock(lock_file, fcntl.LOCK_UN)  # Снимаем блокировку с файла
            except:
                continue
            finally:
                if os.path.exists(lock_file_path):
                    os.remove(lock_file_path)
                    return True
        return False

    def read_packet(self, path_dir):
        global temp_read  # Объявление глобальной переменной temp_read

        if not os.path.exists(path_dir):
            print(bcolors.FAIL + 'Server not found' + bcolors.ENDC)
            return True

        with open(path_dir, 'rb+') as file:
            content = file.read()
            index = content.find(b'\t0t')  # Находим индекс разделителя пакетов

            if index != -1:  # Если индекс не равен -1 (разделитель найден)
                to_TCP = content[:index]  # Отрезок с данными для TCP до разделителя
                after_content = content[index + 3:]  # Оставшиеся данные после разделителя
                print(bcolors.OKGREEN + f'Read_data in {path_dir}:' + bcolors.ENDC,
                      ''.join('{:02x} '.format(x) for x in to_TCP))
                os.write(self.tun_in.fileno(), bytes(to_TCP))
                file.seek(0)
                file.truncate()
                file.write(after_content)
                return False
            else:
                return True
