import asyncio
import socket
import threading
import time

import pyperclip
import clipboardHistory
import client
import fileSender
import pubsub
event=threading.Event()
lock = threading.Lock()
DEBUG=False
class shareClyp:

    def __init__(self, client):
        self.connection =client.connection
        self.loop=True
        self.run()
        self.currentClip=''

    def revievHandler(self):
        try:
            content=self.connection.recv(1024).decode()
            return content
        except Exception as e:
            clipboardHistory.addLog('Error',str(e))

    def rec(self):
        while True:
            content=self.revievHandler()
            st = ''
            if content=="n-@@@@largestring-@@@@n":
                while True:
                    content=self.revievHandler()
                    x=content
                    if "end"==x:
                        break
                    st += content
                content=st
            if DEBUG:
                print(content)
            else:
                self.setClipboard(content)
                print("clipboard recieved")
            clipboardHistory.addLog("recieved", content)
    def setClipboard(self,txt):
        if txt != self.currentClip:
            pyperclip.copy(txt)
            self.currentClip=txt
            print("New paste")
            clipboardHistory.addLog("Pasted", txt)
            return True
        return False


    def paste(self):
        while True:
            x='<Empty>'
            if DEBUG:
                x = input()
                str=''
                while(x!='→'):
                    str+=x+'\n'
                    x = input()
                print(str)
                x=str
            else:
                x=pyperclip.waitForNewPaste()
            if self.setClipboard(x):
                if len(x)>=1024:
                    self.sendlargestr(x)
                else:
                    self.currentClip=x
                    self.connection.send(x.encode())

    def close(self):
        self.loop=True
        pyperclip.copy('end')

    def sendlargestr(self,st):
        chunkrange = list(range(0, len(st), 1024)) + [len(st)]
        self.connection.send("n-@@@@largestring-@@@@n".encode())
        for i in range(len(chunkrange) - 1):
            self.connection.send(st[chunkrange[i]:chunkrange[i + 1]].encode())
        time.sleep(0.01)
        self.connection.send("end".encode())


    def run(self):
        t=threading.Thread(target=self.rec)
        t2=threading.Thread(target=self.paste)
        t.start()
        t2.start()

