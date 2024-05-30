#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import subprocess
import html_pages as HTML

HOST = 'localhost'
PORT = 8080


class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/':
            self.send_response(303)
            self.send_header('Location', '/home')
            self.end_headers()

        if self.path == '/home':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(HTML.html_TAP.encode('utf-8'))

        if self.path == '/home/client':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(HTML.socket_client.encode('utf-8'))

        if self.path == '/choose':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(HTML.choose.encode('utf-8'))

        if self.path == '/home/server':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(HTML.socket_server.encode('utf-8'))

        if self.path == '/home/server/start':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(HTML.server_start.encode('utf-8'))

        else:
            self.send_response_only(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

    def do_POST(self):

        if self.path == '/home':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            form = parse_qs(post_data)
            src_ip = form.get('src_ip', [''])[0]
            dst_ip = form.get('dst_ip', [''])[0]
            password = form.get('password', [''])[0]
            current_dir = form.get('file_path', [''])[0]
            command = (f"echo {password} | sudo -S gnome-terminal --geometry=200x24 -- bash -c './daemon_tap.py "
                       f"--current_dir {current_dir} --src_ip {src_ip} --dst_ip {dst_ip}'")
            subprocess.Popen(command, shell=True)

            self.send_response(303)
            self.send_header('Location', '/choose')
            self.end_headers()

        elif self.path == '/home/server':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            form = parse_qs(post_data)
            socket_ip = form.get('socket_ip', [''])[0]
            socket_port = form.get('socket_port', [''])[0]
            command = (f"gnome-terminal --geometry=100x24 -- bash -c './socket_server.py --ip {socket_ip} --port {socket_port}'")
            subprocess.Popen(command, shell=True)

            self.send_response(303)
            self.send_header('Location', '/home/server/start')
            self.end_headers()

        elif self.path == '/home/client':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            form = parse_qs(post_data)
            client_ip = form.get('client_ip', [''])[0]
            client_port = form.get('client_port', [''])[0]
            file_path = form.get('file_path', [''])[0]
            command = (
                f"gnome-terminal --geometry=100x24 -- bash -c './socket_client.py --ip {client_ip} --port {client_port} --file{file_path}'")
            subprocess.Popen(command, shell=True)

            self.send_response(303)
            self.send_header('Location', '/home/client')
            self.end_headers()



with HTTPServer((HOST, PORT), MyHandler) as server:
    print(f'Server running on http://{HOST}:{PORT}')
    server.serve_forever()
