# Create / read TCP pakage
import tempfile
import subprocess
import os
import struct
import threading
import math
import logging
import fcntl
import time

print('Starting interface ...')

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
            os.rename(self.temp_file.name, self.path)
            os.chmod(self.path, 0o664)
        else:
            os.unlink(self.temp_file.name)

def TunTap(nic_type, nic_name=None):
    tap = Tap(nic_type, nic_name)
    tap.create()
    return tap

class Tap(object):
    def __init__(self, nic_type, nic_name=None):
        self.nic_type = nic_type
        self.name = nic_name
        self.mac = b"\x00"*6
        self.handle = None
        self.ip = None
        self.mask = None
        self.gateway = None
        self.read_lock = threading.Lock()
        self.write_lock = threading.Lock()
        self.quitting = False

    def create(self):
        TUNSETIFF = 0x400454ca
        IFF_TAP = 0x0002
        IFF_NO_PI = 0x1000
        O_RDWR = 0x2
        TUNSETOWNER = 0x400454cc

        tun = os.open('/dev/net/tun', O_RDWR)
        if not tun:
            return None
        if self.nic_type == "Tap":
            flags = IFF_TAP | IFF_NO_PI
        if self.name:
            ifr_name = self.name.encode() + b'\x00'*(16-len(self.name.encode()))
        else:
            ifr_name = b'\x00'*16
        ifr = struct.pack('16sH22s', ifr_name , flags,b'\x00'*22)
        ret = fcntl.ioctl(tun, TUNSETIFF, ifr)
        logging.debug("%s %s"%(ifr,ret))
        dev, _ = struct.unpack('16sH', ret[:18])
        dev = dev.decode().strip("\x00")
        self.name = dev

        fcntl.ioctl(tun, TUNSETOWNER, struct.pack("H",1000))
        self.handle = tun

        if self.handle:
            return self
        else:
            return None

    def _get_maskbits(self,mask):
        masks = mask.split(".")
        maskbits = 0
        if len(masks)==4:
            for i in range(4):
                nbit = math.log(256-int(masks[i]),2)
                if nbit == int(nbit):
                    maskbits += 8-nbit
                else:
                    return
        return int(maskbits)

    def config(self,ip,mask,gateway="192.168.1.1"):
        self.ip = ip
        self.mask = mask
        self.gateway = gateway
        nmask = self._get_maskbits(self.mask)
        try:
            subprocess.check_call('ip link set '+self.name+' up', shell=True)
            subprocess.check_call('ip addr add '+self.ip+'/%d '%nmask + " dev "+ self.name , shell=True)
        except:
            logging.warning("error when config")
            self.close()
            return None
        return  self

    def close(self):

        self.quitting = False
        os.close(self.handle)
        try:
            mode_name = 'tun' if self.nic_type=="Tun" else 'tap'
            subprocess.check_call('ip addr delete '+self.ip+'/%d '%self._get_maskbits(self.mask) + " dev "+ self.name , shell=True)
            subprocess.check_call('ip tuntap delete mode '+ mode_name + " "+ self.name , shell=True)
            print('V. interface is close')
        except Exception as e:
            logging.debug(e)
            pass
        pass

    def read(self, size=1522):
        self.read_lock.acquire()
        data = os.read(self.handle, size)
        self.read_lock.release()
        return data
        pass

    # def write_tun(tun_path, data='Hello world!'):
    #     result = 0
    #     tun = open(tun_path, 'r+b', buffering=0)
    #
    #     try:
    #         result = os.write(tun.fileno(), bytes(data))
    #     except:
    #         print('except')
    #
    #     return result


tap = TunTap(nic_type="Tap", nic_name="tap0")
tap.config("192.168.1.3", "255.255.255.0")
tun = open('/dev/net/tun', 'r+b', buffering=0)
subprocess.check_call('ifconfig tap0 192.168.1.1 pointopoint 192.168.1.1 up', shell=True)

while not tap.quitting:
    # Получаем путь директории, в которой запущен файл Python
    current_dir = os.path.dirname(os.path.abspath(__file__))
    path_dir = os.path.join(current_dir, 'data_file.txt')

    with open(path_dir, 'rb') as file:
        packet = file.read()
        time.sleep(0.5)

    os.write(tun.fileno(), bytes(packet))

    p = tap.read()
    print("raw_read_data:", ''.join('{:02x} '.format(x) for x in p))


    with AtomicWrite(path_dir, 'wb') as file:
        for x in p:
            file.write(bytes([x]))
    time.sleep(0.5)