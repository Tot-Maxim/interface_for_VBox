#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import subprocess
import html_pages as html

HOST = 'localhost'
PORT = 8080


class Bcolors:  # Класс с константами для цветовой кодировки в консоли
    WARNING = '\033[93m'
    ENDC = '\033[0m'


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(303)
            self.send_header('Location', '/tap_manager')
            self.end_headers()

        if self.path == '/tap_manager':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html.TAP_manager.encode('utf-8'))

        if self.path == '/socket_client':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html.socket_client.encode('utf-8'))

        if self.path == '/socket_server':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html.socket_server.encode('utf-8'))

    def do_POST(self):
        if self.path == '/tap_manager':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            form = parse_qs(post_data)
            src_ip = form.get('src_ip', [''])[0]
            dst_ip = form.get('dst_ip', [''])[0]
            password = form.get('password', [''])[0]
            serial_port = form.get('serial_port', [''])[0]
            command = (f"echo {password} | sudo -S gnome-terminal --geometry=200x24 -- bash -c 'cd .. && cd src/ && "
                       f"./daemon_tap.py --serial_port {serial_port} --src_ip {src_ip} --dst_ip {dst_ip}'")
            subprocess.Popen(command, shell=True)

            self.send_response(303)
            self.send_header('Location', '/tap_manager')
            self.end_headers()

        elif self.path == '/socket_server':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            form = parse_qs(post_data)
            socket_ip = form.get('socket_ip', [''])[0]
            socket_port = form.get('socket_port', [''])[0]

            command = (f"gnome-terminal --geometry=200x24 -- bash -c 'cd .. && cd socket_file/ && ./socket_server.py "
                       f"--ip {socket_ip} --port {socket_port}'")
            subprocess.Popen(command, shell=True)

            self.send_response(303)
            self.send_header('Location', '/socket_server')
            self.end_headers()

        elif self.path == '/socket_client':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            form = parse_qs(post_data)
            client_ip = form.get('client_ip', [''])[0]
            client_port = form.get('client_port', [''])[0]
            file_path = form.get('file_path', [''])[0]
            command = f"cd .. && cd socket_file/ && ./socket_client.py --ip {client_ip} --port {client_port} --file {file_path}"
            subprocess.Popen(command, shell=True)

            self.send_response(303)
            self.send_header('Location', '/socket_client')
            self.end_headers()


with HTTPServer((HOST, PORT), MyHandler) as server:
    print(Bcolors.WARNING + f'Для настройки TAP интерфейса зайдите в браузере: ' + Bcolors.ENDC + f'http://{HOST}:{PORT}' )
    server.serve_forever()
