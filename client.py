import asyncio
import socket
import threading
from copy import deepcopy
#pip install git+https://github.com/pybluez/pybluez.git#egg=pybluez
class client:
    def __init__(self,connection=None):
        self.isConnected=False
        self.connection = None
        self.setConnection(connection)

    def setConnection(self,connection):
        if connection:
            self.connection=connection
            self.isConnected = True
            return True
        return False

    def recv(self):
        try:
            return self.connection.recv(1024)
        except:
            self.isConnected = False
        return None
    def send(self,message):
        try:
            self.connection.send(message)
        except:
            self.isConnected=False

    def connect(self)->socket.socket():
        while 1:
            try:
                sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
                sock.connect("", self.port)
                break
            except:
                print("Could Establish connection with server, trying again")
        return sock


