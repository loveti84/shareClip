import bluetooth
import threading
import shareClyp


class socketServer:

    def __init__(self,SERVER_IP,PORT,wait=False):
        self.server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.wait=wait
        self.connections={}
        self.isConnected=False
        self.ip=SERVER_IP
        self.port=PORT
        self.startServer(SERVER_IP, PORT)
        self.loop=True
        self.thread=self.runningserver()
        self.status="init"
        self.connection=None
        return

    def setstatus(self,mes):
        self.status=mes
        print(self.status)

    def startServer(self,SERVER_IP,PORT):
        self.server_socket.bind(('', PORT))
        self.server_socket.listen(1)
        self.setstatus("listening")

    def getClientConnection(self):
        return self.connections.keys()


    def stopServer(self):
        for k in self.connections.keys():
            k.close()
        self.server_socket.close()
    def connectionListener(self):#server listen for client
                conn,adrr=self.server_socket.accept()
                self.connection=conn

def connect(ip,port)->bluetooth.BluetoothSocket():
        while 1:
            try:
                sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
                sock.connect((ip, port))
                print("client connected")

                break
            except:
                print("Could Establish connection with server, trying again")
        return sock






