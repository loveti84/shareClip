import socket
import threading
import time
import bluetooth

# Bluetooth address of the receiving device
def client(target_address,port):


    # Create a Bluetooth socket
    client_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

    client_socket.connect((target_address, port))

    # Connect to the target device

    print("Connected to", target_address)


    return  client_socket

def server(target_address,port):

    # Create a Bluetooth socket

    server_socket=bluetooth.BluetoothSocket(bluetooth.RFCOMM)

    server_socket.bind(('', port))
    server_socket.listen(1)

    client_socket, address = server_socket.accept()
    print("Accepted connection from", address)

    return client_socket



def l(s):
    while 1:
# Receive data
        data = s.recv(1024)
        print("Received:", data.decode())

target_address = "04:7F:0E:7D:D0:D9"
target_address = "D0:39:57:F1:E7:92"



s=client(target_address.lower(),10)
t=threading.Thread(target=lambda :l(s))
t.start()
c=0
while 1:
    i=f"test{c}"
    time.sleep(1)
    c+=1
    s.send(i)
