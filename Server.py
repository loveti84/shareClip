import socket
import threading
import shareClyp


class socketServer:

    def __init__(self,SERVER_IP,PORT,wait=False):
        self.server_socket = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM)
        self.wait=wait
        self.connections={}
        self.isConnected=False
        self.ip=SERVER_IP
        self.port=PORT
        self.startServer(SERVER_IP, PORT)
        self.loop=True
        self.thread=self.runningserver()
        #
    def listenToClients(self, connection):
              while self.loop:
                try:
                    cont=connection.recv(1024)
                    self.sendToCLients(cont,connection)
                except Exception as e:
                    #x=self.clients.pop(client)
                    return "Error"+(str(e))
    def sendToCLients(self,message,connection):
        for k in self.connections.keys():
            try:
                if connection!=k:k.send(message)
            except:
                pass
    def startServer(self,SERVER_IP,PORT):
        self.server_socket.bind((SERVER_IP, PORT))
        self.server_socket.listen(1)


    def getClientConnection(self):
        return self.connections.keys()


    def stopServer(self):
        for k in self.connections.keys():
            k.close()
        self.server_socket.close()
    def connectionListener(self):#server listen for client
            while self.loop:
                conn,adrr=self.server_socket.accept()
                self.connections[conn] = True
                t = threading.Thread(target=lambda :self.listenToClients(conn))
                t.start()


    def runningserver(self):
        t = threading.Thread(target=self.connectionListener)
        t.start()



def connect(ip,port)->socket.socket():
        while 1:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((ip, port))
                break
            except:
                print("Could Establish connection with server, trying again")
        return sock






