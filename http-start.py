from http.server import BaseHTTPRequestHandler, HTTPServer

hostName = "localhost"
hostPort = 8080

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/logo.png':
            file_path = '/home/serverside/PycharmProjects/interface_for_VBox/Copy_01.png'
            with open(file_path, 'rb') as file:
                self.send_response_only(200)
                self.send_header('Content-type', 'image/png')  # Set the correct content type here
                self.end_headers()
                self.wfile.write(file.read())
        else:
            self.send_response_only(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

myServer = HTTPServer((hostName, hostPort), MyServer)
print("Server started http://%s:%s" % (hostName, hostPort))

try:
    myServer.serve_forever()
except KeyboardInterrupt:
    pass

myServer.server_close()
print("Server stopped.")