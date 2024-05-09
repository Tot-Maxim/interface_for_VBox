from scapy.all import *
import time
from array import array
import fcntl
import os
import struct
import subprocess
import threading

CURRENT_DIR = '/media/sf_FilePack'

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
read_lock = threading.Lock()
packet = Ether(dst="0a:1a:de:3c:f0:5d", src="0a:1a:de:3c:f0:5d") / IP(dst="10.1.1.7", src="10.1.1.8") / ICMP(type="echo-request") / Raw(load='Check connect to host')

# Открытие файла, соответствующего устройству TUN, в двоичном режиме чтения/записи без буферизации.
tun = open('/dev/net/tun', 'r+b', buffering=0)
ifr = struct.pack('16sH', b'tap0', IFF_TAP | IFF_NO_PI)
fcntl.ioctl(tun, TUNSETIFF, ifr)
fcntl.ioctl(tun, TUNSETOWNER, 1000)

# Поднятие tap0 и назначение адреса
subprocess.check_call('ifconfig tap0 10.1.1.8 pointopoint 10.1.1.7 up', shell=True)


class bcolors:
    HEADER = '\033[95m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def write_packet_to_file(packet, file_path):
    lock_file_path = file_path + '.lock'

    for _ in range(2):
        try:
            with open(lock_file_path, 'w') as lock_file:
                fcntl.flock(lock_file, fcntl.LOCK_EX)  # Acquire an exclusive lock on the lock file

                with open(file_path, 'ab+') as file:
                    file.write(packet)
                    file.write(b'\t0t')
                    print(bcolors.WARNING + f'Write data in {file_path}: ' + bcolors.ENDC,
                          ''.join('{:02x} '.format(x) for x in packet))
                fcntl.flock(lock_file, fcntl.LOCK_UN)  # Release the lock on the lock file
        except Exception as e:
            time.sleep(0.1)
            print(f"Failed to write to file: {e}. Retrying...")
            continue
        finally:
            if os.path.exists(lock_file_path):
                os.remove(lock_file_path)
                return True
    return False


def read_packet_to_file(path_dir):
    global temp_read
    with open(path_dir, 'rb+') as file:
        content = file.read()
        index = content.find(b'\t0t')

        if index != -1:
            to_TCP = content[:index]
            content = content[index + 3:]

            if temp_read != to_TCP:
                temp_read = to_TCP
                print(bcolors.OKGREEN + f'Read_data in {path_dir}:' + bcolors.ENDC, ''.join('{:02x} '.format(x) for x in to_TCP))
                os.write(tun.fileno(), bytes(to_TCP))
                return False
            else:
                pass
            file.seek(0)
            file.truncate()
            file.write(content)
        else:
            return True


if __name__ == "__main__":
    while True:
        print('1', state)
        if state == 1:
            try:
                read_lock.acquire()
                timeout = time.time() + 2
                while True:
                    readable, _, errors = select.select([tun.fileno()], [], [tun.fileno()], 0.5)
                    if tun.fileno() in readable:
                        from_TCP = array('B', os.read(tun.fileno(), 1522))
                        break
                    if tun.fileno() in errors:
                        print("Error reading from tap")
                        break
                    if time.time() > timeout:
                        sendp(packet, iface="tap0")
                        break
            finally:
                read_lock.release()
            if from_TCP:
                state = 2
        print('2', state)
        if state == 2:
            path_dir = os.path.join(CURRENT_DIR, 'from_virtual.docx')
            if write_packet_to_file(from_TCP, path_dir):
                state = 3
        print('3', state)
        if state == 3:
            path_dir = os.path.join(CURRENT_DIR, 'from_host.docx')
            if read_packet_to_file(path_dir):
                state = 1

tun.close()
