import socket
import tempfile
import os
import subprocess

try:
    subprocess.check_call('sudo ip route delete 10.0.0.0/8 dev tap0 proto kernel scope link src 10.1.1.8', shell=True)
except:
    pass
# Server configuration
server_ip = '10.1.1.8'
server_port = 5050

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the server address and port
server_socket.bind((server_ip, server_port))

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

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
            print("Break")


while True:
    # Listen for incoming connections
    server_socket.listen(5)
    print(bcolors.OKCYAN + f"Server is listening on {server_ip}:{server_port}..." + bcolors.ENDC)

    client_socket, client_address = server_socket.accept()
    print(bcolors.WARNING + f"Connection established with {client_address}" + bcolors.ENDC)

    while True:
        try:
            data = b''
            while True:
                try:
                    chunk = client_socket.recv(1756)
                    if not chunk:
                        print("No more data to receive. Client disconnected.")
                        break
                    data += chunk
                    print(f"Received data chunk from client")
                except socket.timeout:
                    print("Socket timed out. No more data to receive.")
                    break

            if data:
                byte_data = bytes.fromhex(data.decode('utf-8'))
                print(len(byte_data))
                print(f'Writing data ... {byte_data}')
                with AtomicWrite('logo_rec.png', 'wb') as file:
                    for x in byte_data:
                        file.write(bytes([x]))
                print(bcolors.WARNING + "File saved successfully." + bcolors.ENDC)

                # Send a response back to the client
                response = "Data received by the server."
                client_socket.sendall(response.encode())
            else:
                print("Empty data received. Closing connection.")
                break
        except Exception as e:
            print(f"Error receiving/sending data: {e}")
            break

    # Close the client socket
    client_socket.close()

# Close the server socket
server_socket.close()