from datetime import datetime
history={}
log = False


def addLog(type,content):
    if log:
        t=datetime.now()
        history[t.strftime("%H:%M:%S")]={"type":type,"content":f'{content}'}

def add(k,type,content):
    history[k] = {"type": type, "content": content}
