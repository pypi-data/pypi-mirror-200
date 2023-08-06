from enum import Enum

class state(Enum):

    Handshaking = 0
    Status = 1
    Login = 2
    Play = 3


class bound(Enum):
    
    Server = 0
    Client = 1
