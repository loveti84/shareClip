import _thread
import threading

import event

events={}

def addPublisher(name:event.Event,*args):
    events[name]=list(args)
def addListeners(name, *args):
    if name in events.keys():
        events[name].extend(list(args))
    else:
        events[name]=list(args)



threadpool=[]
def publishWhenFunctionFinished(func,event:event.Event,loop=True,*args,onFinished=None):
    def wrapper():
        while loop:
            res=func()
            _invokeSubscribers(event,*args,result=res)
            if onFinished:
                onFinished()
    t = threading.Thread(target=wrapper)
    threadpool.append(t)
    t.start()


def _invokeSubscribers(name:event.Event,*args,**kwargs):
    dic={}
    if name not in events.keys():
        print("Name not found")
    elif len(events[name])>0:
        for i in events[name]:
            dic[i]=i(*args,**kwargs)
    else:
        print("No functions found")
    return dic


def publish(name,*args,wait=False):
    if wait:
        return _invokeSubscribers(name,*args)
    else:
        t=threading.Thread(target=lambda:_invokeSubscribers(name,*args))
        t.start()

