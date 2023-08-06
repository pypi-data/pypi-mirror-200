from ...types import *
from ...p import Night
from cubelib.proto.version_independent.ServerBound import ClassicLogin


class Login(ClassicLogin):
    pass

class Play:

    class ChatMessage(Night):
        Message: String

    map = {0x02: ChatMessage}
    inv_map = {v: k for k, v in map.items()}
