from scapy.all import *
import json

#file_path = "count.json"

#with open(file_path, 'r') as file:
#    json_data = json.load(file)

packets = []
packet = Ether(dst="0a:1a:de:3c:f0:5d", src = "0a:1a:de:3c:f0:5d") / IP(dst = "192.168.1.1", src= "192.168.1.1") / TCP(dport = 12345, sport = 54321) / Raw(load = 'Test text from VBOX')
    
# Отправка пакета на интерфейс TAP
sendp(packet, iface="tap0")
