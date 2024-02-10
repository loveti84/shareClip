import threading


def threadWrapper(func):
    t=threading.Thread(target=func)
    t.start()


def chronRun(*args):
    return [r() for r in args]

def replacePara(func,paradata,*paratoChange,ignoreKeyError=True,**kwargs):
    c=0
    for arg in paratoChange:
        if ignoreKeyError | arg in kwargs:
            kwargs[arg]=paradata[arg]
    return func(**kwargs)

def wrapFunction(func,topParaName,**kwargs):
    def wrapper(para):
        kwargs[topParaName] = para
        return func(kwargs)
    return wrapper

