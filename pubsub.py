events={}
def createEvent(name):
    events[name]=[]
def setEvent(name,*args):
    if name in events.keys():
        events[name].extend(list(args))
    else:
        events[name]=list(args)


def invoke(name,*args):
    dic={}
    if name not in events.keys():
        print("Name not found")
    elif len(events[name])>0:
        for i in events[name]:
            dic[i]=i(*args)
    else:
        print("No functions found")
    return dic
