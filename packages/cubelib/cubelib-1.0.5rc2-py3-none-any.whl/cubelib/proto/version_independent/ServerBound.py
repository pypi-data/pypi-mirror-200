from cubelib.types import VarInt, String, UnsignedShort, NextState, Long, ByteArray, FiniteLengthByteArray
from cubelib.p import Night

class Handshaking:

    class Handshake(Night):

        ProtoVer: VarInt
        ServerName: String[255]
        ServerPort: UnsignedShort
        NextState: NextState

    map = {0: Handshake}
    inv_map = {Handshake: 0}

class Status:

    class Request(Night):
        pass

    class Ping(Night):

        Uniq: Long

    map = {0: Request, 1: Ping}
    inv_map = {Request: 0, Ping: 1}

class ClassicLogin:

    class LoginStart(Night):

        Username: String[16]

    class EncryptionResponse(Night):

        SharedSecret: FiniteLengthByteArray        
        VerifyToken: FiniteLengthByteArray 

    map = {0: LoginStart, 1: EncryptionResponse}
    inv_map = {LoginStart: 0, EncryptionResponse: 1}
