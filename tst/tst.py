import socket

# Bluetooth address of the receiving device
def send():
    target_address = "D0:39:57:F1:E7:92"
    target_address = "04:7F:0E:7D:D0:D9"
    port = 1

    # Create a Bluetooth socket
    client_socket = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)

    try:
        # Connect to the target device
        client_socket.connect((target_address, port))
        print("Connected to", target_address)

        # Send data
        message = "Hello, world!"
        client_socket.sendall(message.encode())
        print("Sent:", message)

    finally:
        # Close the socket
        client_socket.close()

def rec():
    port = 1

    # Create a Bluetooth socket
    server_socket = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)

    try:
        # Bind the socket to the local Bluetooth adapter and specified port
        server_socket.bind(("", port))
        print("Listening for connections on RFCOMM channel", port)

        # Listen for incoming connections
        server_socket.listen(1)

        # Accept the connection
        client_socket, address = server_socket.accept()
        print("Accepted connection from", address)

        # Receive data
        data = client_socket.recv(1024)
        print("Received:", data.decode())

    finally:
        # Close the sockets
        client_socket.close()
        server_socket.close()