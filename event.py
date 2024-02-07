from enum import Enum


class Event(Enum):
    WAIT = 1
    CONNECTED = 2
    DISCONNECTED = 3