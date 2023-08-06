from cubelib.types import String, Long, VarInt, ByteArray, FiniteLengthByteArray
from cubelib.p import Night

class Status:
    class Response(Night):

        JsonRsp: String

    class Pong(Night):

        Uniq: Long

    map = {0: Response, 1: Pong}
    inv_map = {Response: 0, Pong: 1}

class ClassicLogin:

    class Disconnect(Night):

        Reason: String

    class SetCompression(Night):

        Threshold: VarInt

    class LoginSuccess(Night):

        UUID: String[[36]]
        Username: String[16]

    class EncryptionRequest(Night):

        ServerID: String[20]        
        PublicKey: FiniteLengthByteArray        
        VerifyToken: FiniteLengthByteArray

    map = {0: Disconnect, 1: EncryptionRequest, 2: LoginSuccess, 3: SetCompression}
    inv_map = {v: k for k, v in map.items()}
