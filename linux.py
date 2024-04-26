import fcntl
import os
import struct
import subprocess
import time
from array import array


# Some constants used to ioctl the device file. I got them by a simple C program.
TUNSETIFF = 0x400454ca
TUNSETOWNER = TUNSETIFF + 2
IFF_TUN = 0x0001
IFF_TAP = 0x0002
IFF_NO_PI = 0x1000

# Open file corresponding to the TUN device in read/write binary mode with no buffering.
tun = open('/dev/net/tun', 'r+b', buffering=0)
ifr = struct.pack('16sH', b'tap0', IFF_TAP | IFF_NO_PI)
fcntl.ioctl(tun, TUNSETIFF, ifr)
fcntl.ioctl(tun, TUNSETOWNER, 1000)

# Bring it up and assign addresses.
subprocess.check_call('ifconfig tap0 192.168.1.1 pointopoint 192.168.1.1 up', shell=True)
path_dir = '/home/oem/PycharmProjects/virtual_interface/data_file.txt'

while True:
    # Create a NumPy array filled with values from 0 to 29 for testing purposes.
    #packet = array('B', os.read(tun.fileno(), 2048))
    with open(path_dir, 'rb') as file:
        packet = file.read()
        print(packet)
        time.sleep(0.5)

    # Swap bytes at positions 12-15 with bytes at positions 16-19 in the packet array
    #packet[12:16], packet[16:20] = packet[16:20], packet[12:16]

    # Print the content of the packet array after the swap operation
    print('Packet after byte swap:', packet)

    # Write the modified packet into the TUN device.
    os.write(tun.fileno(), bytes(packet))
