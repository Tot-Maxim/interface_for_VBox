from mytuntap import TAP_Manager
from scapy.all import *
import threading
import select
import os
import time


state = 1
temp_read = b''
CURRENT_DIR = '/media/sf_FilePack'
file_from_virtual = 'from_virtual'
file_from_host = 'from_host'
DST_IP = '10.1.1.7'
SRC_IP = '10.1.1.8'
PACK = Ether(dst="0a:1a:de:3c:f0:5d", src="0a:1a:de:3c:f0:5d") / IP(dst=DST_IP, src=SRC_IP) / ICMP(
    type="echo-request") / Raw(load='Check connect to host')

read_lock = threading.Lock()
tap_manager = TAP_Manager()
tun = tap_manager.tun_setup()

while True:
    if state == 1:
        try:
            read_lock.acquire()
            timeout = time.time() + 2
            while True:
                readable, _, errors = select.select([tun.fileno()], [], [tun.fileno()], 0.5)
                if tun.fileno() in readable:
                    from_TCP = os.read(tun.fileno(), 1522)
                    break
                if tun.fileno() in errors:
                    print("Error reading from tap")
                    break
                if time.time() > timeout:
                    sendp(PACK, iface="tap0")
                    break
        finally:
            read_lock.release()
        if from_TCP:
            state = 2
    if state == 2:
        path_dir = os.path.join(CURRENT_DIR, file_from_virtual)
        if tap_manager.write_packet_to_file(from_TCP, path_dir):
            state = 3
    if state == 3:
        path_dir = os.path.join(CURRENT_DIR, file_from_host)
        if tap_manager.read_packet(path_dir):
            state = 1