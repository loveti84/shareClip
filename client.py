import asyncio
import socket
import threading
from copy import deepcopy

class client:
    def __init__(self,connection=None):
        self.isConnected=False
        self._event=threading.Event
        if connection==None:
            self.connection=self.connect()
            self.isConnected = True
        else:
            self.connection=connection


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


