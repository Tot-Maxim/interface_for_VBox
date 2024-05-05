import socket

# Server information
server_ip = '10.1.1.8'  # Update with the server's IP address
server_port = 5050  # Update with the server's port number


# Client code to send data to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    for _ in range(3):
        client_socket.connect((server_ip, server_port))

        while True:
            Test_text = input('Enter the text to send to the interface:\n')

            byte_text = b'Hello world!'
            # Send the data to the server
            client_socket.sendall(byte_text)

            # Receive response from the server
            server_response = client_socket.recv(1024).decode('utf-8')
            print(f"Server response: {server_response}")

except ConnectionRefusedError:
    print("Connection to the server refused. Make sure the server is running.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Close the socket connection and TAP interface
    client_socket.close()
