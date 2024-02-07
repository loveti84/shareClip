import socket
import threading


# Bluetooth address of the receiving device
def server(target_address,port):


    # Create a Bluetooth socket
    client_socket = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)

    # Connect to the target device
    client_socket.connect((target_address, port))
    print("Connected to", target_address)

    # Send data
    message = "Hello, world!"
    client_socket.send(message.encode())
    print("Sent:", message)

    return  client_socket

def client(target_address,port):

    # Create a Bluetooth socket
    server_socket = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)


    # Bind the socket to the local Bluetooth adapter and specified port
    server_socket.bind((target_address, port))
    print("Listening for connections on RFCOMM channel", port)

    # Listen for incoming connections
    server_socket.listen(1)

    # Accept the connection
    client_socket, address = server_socket.accept()
    print("Accepted connection from", address)

    return client_socket



def l(s):
    while 1:
# Receive data
        data = s.recv(1024)
        print("Received:", data.decode())

#target_address = "D0:39:57:F1:E7:92"
target_address = "04:7F:0E:7D:D0:D9"
s=client(target_address,1)
t=threading.Thread(target=lambda :l(s))
t.start()
while 1:
    i=input()
    s.send(i.encode())
