from mytuntap import TAP_Manager
import select
import argparse


parser = argparse.ArgumentParser(description='TAP Manager Script')
parser.add_argument('--current_dir', type=str, default='/media/sf_FilePack',
                    help='Shared folder path')
parser.add_argument('--file_from_host', type=str, default='from_host', help='Shared file from host')
parser.add_argument('--file_from_virtual', type=str, default='from_virtual', help='Shared file from virtual')
parser.add_argument('--src_ip', type=str, default='10.1.1.8', help='Source IP address')
parser.add_argument('--dst_ip', type=str, default='10.1.1.7', help='Destination IP address')
args = parser.parse_args()

tap_manager = TAP_Manager(args.src_ip, args.dst_ip)  # Инициализация класса TAP_Manager
tun = tap_manager.tun_setup()  # Инициализация tap интерфейса

while True:
    read_tun, write_tun, _ = select.select([tun.fileno()], [tun], [])
    if tun.fileno() in read_tun:
        tap_manager.read_from_tcp(args.current_dir, args.file_from_virtual)

    if tun in write_tun:
        tap_manager.read_from_file(args.current_dir, args.file_from_host)
