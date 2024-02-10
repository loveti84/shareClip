from enum import Enum


class Event(Enum):
    CONNECTING = 1
    CONNECTED = 2
    DISCONNECTED = 3
    COPYFILE=4
    RECIEVING=5
    RECIEVED=6
    SENDING=7
    SENDED=8
    SENDFILEREQUEST=9
    ERROR=10
    CLOSE=11