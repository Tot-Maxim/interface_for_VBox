import socket
import fcntl
import argparse
import os
import struct
import subprocess
from scapy.all import *

# Server information
server_ip = '127.0.0.1'  # Update with the server's IP address
server_port = 12345  # Update with the server's port number

# Open TAP interface
TUNSETIFF = 0x400454ca
TUNSETOWNER = TUNSETIFF + 2
IFF_TUN = 0x0001
IFF_TAP = 0x0002
IFF_NO_PI = 0x1000

parser = argparse.ArgumentParser(description='Process file types list.')
parser.add_argument('--IP-dst', type=str, default='192.168.1.1', help='IP address. Default 192.168.1.1')
parser.add_argument('--Eth-dst', type=str, default='0a:1a:de:3c:f0:5d', help='Ether address. Default 0a:1a:de:3c:f0:5d')
parser.add_argument('--TCP-port', type=int, default=12345, help='input TCP port')
args = parser.parse_args()
IP_dst = args.IP_dst
Eth_dst = args.Eth_dst
TCP_port = args.TCP_port
Test_text = 'Hello world'

tap = open('/dev/net/tun', 'r+b', buffering=0)
ifr = struct.pack('16sH', b'tap0', IFF_TAP | IFF_NO_PI)
fcntl.ioctl(tap, TUNSETIFF, ifr)
fcntl.ioctl(tap, TUNSETOWNER, 1000)

# Bring up the TAP interface and assign IP addresses
subprocess.check_call('ifconfig tap0 192.168.1.2 pointopoint 192.168.1.1 up', shell=True)

# Client code to send data to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    for _ in range(3):
        client_socket.connect((server_ip, server_port))

        while True:
            Test_text = input('Enter the text to send to the interface:\n')

            packet = Ether(dst=f'{Eth_dst}', src=f'{Eth_dst}') / IP(dst=f'{IP_dst}', src=f'{IP_dst}') / TCP(dport=12345,
                                                                                                            sport=54321) / Raw(
                load=f'{Test_text}')

            # Read data from the TAP interface
            sendp(packet, iface='tap0')
            packet = os.read(tap.fileno(), 2048)
            print('Packet read from TAP interface:', packet)

            # Send the data to the server
            client_socket.sendall(packet)

            # Receive response from the server
            server_response = client_socket.recv(1024).decode()
            print(f"Server response: {server_response}")

except ConnectionRefusedError:
    print("Connection to the server refused. Make sure the server is running.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Close the socket connection and TAP interface
    client_socket.close()
    tap.close()