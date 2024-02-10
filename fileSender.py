import queue
import time

import win32clipboard
import win32con
import socket
import threading
import var
import pubsub
import event
import clipboardHistory
lock = threading.Lock()
DEBUG=False
import socket
class filesender:
    def __init__(self, connection):
        self.connection =connection
        self.loop=True
        #self.queue = queue.Queue()
        self.run()

    def que(self):
        while self.loop:
            content = self.connection.recv(1024)
            if len(content) > 0:
                self.queue.put(content)
            if len(content)==3:
                self.rec()
    def rec(self):
         while self.loop:
                content=self.connection.recv(1024)
                if(len(content)>0):
                    try:
                        content = content.decode()
                        path=content.split("/")[-1]
                        loc = var.PATH
                        print(loc + "/" + path)
                        f = open(loc + "/" + path, "wb")
                        print("Revieving")
                        self.recFile(f)
                    except Exception as e:
                        print(e)


    def recFile(self,f):
        run=True
        content=""
        while run:
            content = self.connection.recv(1024)
            if len(content)<100:
                try:
                    if content.decode()=='end':
                        run = False
                    else:
                        f.write(content)
                except Exception as e:
                    f.write(content)
            else:
                f.write(content)
            self.connection.send('rec'.encode())
        f.close()
        clipboardHistory.addLog("file sended", content)

        # except Exception as e:
                #    print("Error while recieving",e)




    def send(self):
        def sbsend():
            print("sending")
            path="C:\\Users\\Florian\\Desktop\\recfile.exe"
            path=self.get_file_path_from_clipboard()
            print(path)
            if path==None:
                print("no valid path on clipboard")
                return
            f = open(path, 'rb')
            self.connection.send(path.split('\\')[-1].encode())
            l = f.read(1024)
            while (l):
                self.connection.send(l)
                l = f.read(1024)
            f.close()
            self.connection.send("end".encode())
            clipboardHistory.addLog("file sended",path)

        t=threading.Thread(target=sbsend)
        t.start()



    def run(self):
            recT=threading.Thread(target=self.rec)
            recT.start()
           # queT = threading.Thread(target=self.que)
            #queT.start()
            pubsub.addListeners(event.Event.SENDFILEREQUEST, self.send)
    def get_file_path_from_clipboard(self):
        win32clipboard.OpenClipboard()
        try:
            if win32clipboard.IsClipboardFormatAvailable(win32con.CF_HDROP):
                data = win32clipboard.GetClipboardData(win32con.CF_HDROP)
                if data:
                    file_path = data[0]  # Retrieve the path of the first file
                    return file_path
        finally:
            win32clipboard.CloseClipboard()
        return None

