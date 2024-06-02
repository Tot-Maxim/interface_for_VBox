from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import json

HOST = 'localhost'
PORT = 7070
temp = 1


class MyServer(BaseHTTPRequestHandler):
    progress = 0

    def do_GET(self):
        global temp
        parsed_path = urlparse(self.path)

        if self.path == '/home':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = """
<!DOCTYPE html>
<html lang='ru'>
<head>
<meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Server receive</title>
    <style>
        body {
            background-color: black;
            margin: 0;
            padding: 0;
            font-family: sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }

        form {
            display: grid;
            gap: 10px;
            justify-items: center;
            margin-top: 20px;
        }

        button {
            background-color: white;
            color: black;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
        }
        
        input {
            padding: 5px;
        }

        label {
            color: white;
            text-align: right;
            padding-right: 10px;
            grid-column: 1 / 2;
        }
    </style>
</head>
<body>
    <h1>Server receive</h1>
    <form method="post">
        <label for="src_ip">Введите IP-адрес источника:</label>
        <input type="text" id="src_ip" name="src_ip" value="10.1.1.7">
        
        <label for="dst_ip">Введите IP-адрес назначения:</label>
        <input type="text" id="dst_ip" name="dst_ip" value="10.1.1.8">
        
        <label for="password">Введите пароль:</label>
        <input type="password" id="password" name="password" value="547172" oninput="maskPassword()">
        
        <label for="file_path">Введите путь к папке обмена:</label>
        <input type="text" id="file_path" name="file_path" value='/home/tot/FilePack'>
        
        <button onclick="window.location.href='/run_tuntap'">Запуск TAP интерфейса</button>
    </form>
    
    <progress id="progress-bar" value="{self.progress}" max="10"></progress>
    <br><br>
    <button id="btn">Click me</button>
    
    <div id="text_output"></div>
    <script>
        var btn = document.getElementById('btn');
        var progressBar = document.getElementById('progress-bar');

        btn.addEventListener('click', function() {{
            fetch('/update_progress')
                .then(response => response.json())
                .then(data => {{
                    progressBar.value = data.progress;
                    if (data.progress === 10) {{
                        setTimeout(function() {{
                            progressBar.value = 0;
                        }}, 1000);
                    }}
                }});
        }});
    </script>
    
</body>
</html>
"""
            self.wfile.write(html.encode('utf-8'))

        elif parsed_path.path == '/update_progress':

            self.progress = (self.progress + temp) % 11
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'progress': self.progress}
            self.wfile.write(json.dumps(response).encode('utf-8'))
            temp += 1

        elif self.path == '/logo':
            print('here')
            file_path = '/home/oem/PycharmProjects/interface_for_VBox/logo.png'
            with open(file_path, 'rb') as file:
                self.send_response_only(200)
                self.send_header('Content-type', 'image/png')  # Set the correct content type here
                self.end_headers()
                self.wfile.write(file.read())
        else:
            self.send_response_only(404)
            self.end_headers()
            self.wfile.write(b'Not Found')


myServer = HTTPServer((HOST, PORT), MyServer)
print(f'Server running on http://{HOST}:{PORT}')

try:
    myServer.serve_forever()
except KeyboardInterrupt:
    pass

myServer.server_close()
print("Server stopped.")
