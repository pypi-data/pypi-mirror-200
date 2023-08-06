"""
cubelib.types
=================================================================
Module that contains the minecraft protocol types implementation.
"""

from io import BytesIO
from enum import Enum
from struct import pack, unpack

from cubelib.errors import BufferExhaustedException

from typing import Tuple

class SafeBuff(BytesIO):
    """
    This class make BytesIO object safe for reading.
    It re-defines read() method and add returned bytes length comparison with requested,
    and raises BufferExhaustedException if it not equal.
    """

    def read(self, *a) -> bytes:

        if not a:
            return super().read()

        r = super().read(a[0])
        if len(r) != a[0]:
            raise BufferExhaustedException(f'Buffer returned {len(r)} instead of required {a[0]}')
        return r

class Optional:
    """
    Special type, container for basic types that make them optional,
    decoder must read optional type only if other field, provided in field_name equals (or not quals if inv)
    to excepted_val.
    """

    def __init__(self, field_name, excepted_val, equals=True):

        self.field_name = field_name
        self.excepted_val = excepted_val
        self.equals = equals

    def __getitem__(self, type):

        self.type = type
        return self

    def build(self, value):

        return self.type.build(value)

    def is_legit(self, field_val):

        if self.equals:
            if isinstance(self.excepted_val, tuple):
                if field_val in self.excepted_val:
                    return True
                return False
            if field_val == self.excepted_val:
                return True
            return False
        else:
            if isinstance(self.excepted_val, tuple):
                if field_val in self.excepted_val:
                    return False
                return True
            if field_val == self.excepted_val:
                return False
            return True


class VarInt:
    """
    Most important Minecraft protocol datatype.
    Encodes integer value in range -2_147_483_648 <= val <= 2_147_483_647.
    """

    _max = 2_147_483_647
    _min = -2_147_483_648

    @staticmethod
    def cntd_destroy(buff: SafeBuff) -> Tuple[int, int]:
        """
        Returns number of bytes that occupied by the value and value
        """

        total = 0
        shift = 0
        val = 0x80
        while val & 0x80:
            val = unpack('B', buff.read(1))[0]
            total |= ((val & 0x7F) << shift)
            shift += 7
            if shift // 7 > 5:
                raise RuntimeError('VarInt is too big!')
        if total & (1 << 31):
            total = total - (1 << 32)
        return total, shift // 7

    @staticmethod
    def destroy(buff: SafeBuff) -> int:

        return VarInt.cntd_destroy(buff)[0]

    @staticmethod
    def build(val: int) -> bytes:

        if not VarInt._max >= val >= VarInt._min:
            raise ValueError(f'VarInt must be in range ({VarInt._max} >= value >= {VarInt._min})')

        total = b''
        if val < 0:
            val = (1 << 32) + val
        while val >= 0x80:
            bits = val & 0x7F
            val >>= 7
            total += pack('B', (0x80 | bits))
        bits = val & 0x7F
        total += pack('B', bits)
        return total

class MCEnum(Enum):

    IntegerType: type

    @classmethod
    def destroy(class_, buff: SafeBuff):
        return class_(class_.__annotations__['IntegerType'].destroy(buff))

    def build(self) -> bytes:
        return self.__annotations__['IntegerType'].build(self.value)

class FiniteLengthArray:

    def __class_getitem__(class_, val):

        obj = class_()
        obj.TYPE = val
        return obj

    def destroy(self, buff: SafeBuff) -> list:

        count = VarInt.destroy(buff)
        out = []
        for x in range(0, count):
            try:
                out.append(self.TYPE.destroy(buff))
            except BufferExhaustedException as e:
                raise RuntimeError(f"Buffer exhauseted on {x}/{count} iteration of decoding array of {self.TYPE}") from e
        return out

    def build(self, val: list) -> bytes:

        out = VarInt.build(len(val))
        for i in val:
            out += self.TYPE.build(i)
        return out

class UnsignedShort:

    @staticmethod
    def destroy(buff: SafeBuff) -> int:
        return unpack('!H', buff.read(2))[0]

    @staticmethod
    def build(val: int) -> bytes:
        return pack('!H', val)

class String:

    @staticmethod
    def build(val: str) -> bytes:

        o = b""
        o += VarInt.build(len(val))
        o += val.encode()
        return o

    @staticmethod
    def destroy(buff: SafeBuff) -> str:

        l = VarInt.destroy(buff)
        return buff.read(l).decode()

    def __class_getitem__(class_, val):

        obj = class_()

        # Type[int] set max length\max value
        if isinstance(val, int):
            obj.max = val

        # Type[[int]] set excepted length\value
        elif isinstance(val, list) and len(val) == 1:

            obj.min = val[0]
            obj.max = val[0]

        # Type[int, int] set range of excepted values\len
        elif isinstance(val, tuple) and len(val) == 2:

            obj.min = val[0]
            obj.max = val[1]

        else:
            raise Exception('какой далбаеб писал анатацию?!?!')

        return obj

class Long:

    @staticmethod
    def destroy(buff: SafeBuff) -> int:
        return unpack('!q', buff.read(8))[0]

    @staticmethod
    def build(val: int) -> bytes:
        return pack('!q', val)

class NextState(Enum):

    Status = 1
    Login = 2

    @staticmethod
    def destroy(buff: SafeBuff):
        return NextState(int.from_bytes(buff.read(1), 'little'))

    def build(self) -> bytes:
        return bytes([self.value])

class UnsignedByte:

    @staticmethod
    def destroy(buff: SafeBuff) -> int:
        return unpack('!B', buff.read(1))[0]

    @staticmethod
    def build(val: int) -> bytes:
        return pack('!B', val)

class Byte:

    @staticmethod
    def destroy(buff: SafeBuff) -> int:
        return unpack('!b', buff.read(1))[0]

    @staticmethod
    def build(val: int) -> bytes:
        return pack('!b', val)

class Bool:

    @staticmethod
    def destroy(buff: SafeBuff) -> bool:
        return unpack('!?', buff.read(1))[0]

    @staticmethod
    def build(val: bool) -> bytes:
        return pack('!?', val)

class Int:

    @staticmethod
    def destroy(buff: SafeBuff) -> int:
        return unpack('!i', buff.read(4))[0]

    @staticmethod
    def build(val: int) -> bytes:
        return pack('!i', val)

class ByteArray:

    @staticmethod
    def destroy(buff: SafeBuff) -> bytes:
        return buff.read()

    @staticmethod
    def build(val: bytes) -> bytes:
        return val

class Position:

    @staticmethod
    def destroy(buff: SafeBuff) -> Tuple[int, int, int]:
        buff.read(8)
        return (-1, -1, -1)

    @staticmethod
    def build(val: tuple) -> bytes:

        return b"\x41"*8

class Float:

    @staticmethod
    def destroy(buff: SafeBuff) -> int:
        return unpack('!f', buff.read(4))[0]

    @staticmethod
    def build(val: int) -> bytes:
        return pack('!f', val)

class Double:

    @staticmethod
    def destroy(buff: SafeBuff) -> int:
        return unpack('!d', buff.read(8))[0]

    @staticmethod
    def build(val: int) -> bytes:
        return pack('!d', val)

class Short:
    
    @staticmethod
    def destroy(buff: SafeBuff) -> int:
        return unpack('!h', buff.read(2))[0]

    @staticmethod
    def build(val: int) -> bytes:
        return pack('!h', val)

class Angle:

    @staticmethod
    def destroy(buff: SafeBuff) -> int:
        return unpack('!B', buff.read(1))[0]

    @staticmethod
    def build(val: int) -> bytes:
        return pack('!B', val)

class Slot(ByteArray):
    pass

class FiniteLengthByteArray(ByteArray):

    @staticmethod
    def destroy(buff: SafeBuff) -> bytes:        
        return buff.read(VarInt.destroy(buff))
    
    @staticmethod
    def build(val: bytes) -> bytes:
        out = VarInt.build(len(val))
        out += val
        return out

class UUID:

    @staticmethod
    def destroy(buff: SafeBuff) -> bytes:
        return buff.read(16)
    
    @staticmethod
    def build(val: bytes) -> bytes:
        return val

class PlayerDiggingStatusEnum(MCEnum):

    IntegerType:  Byte

    StartedDigging = 0
    CancelledDigging = 1
    FinishedDigging = 2
    DropItemStack = 3
    DropItem = 4
    ShootArrow_FinishEating = 5

class FaceEnum(MCEnum):

    IntegerType: Byte

    YNEG = 0
    YPOS = 1
    ZNEG = 2
    ZPOS = 3
    XNEG = 4
    XPOS = 5

    SPEC = 255

class EntityActionActionIDEnum(MCEnum):

    IntegerType: VarInt

    StartSneaking = 0
    StopSneaking = 1
    LeaveBed = 2
    StartSprinting = 3
    StopSprinting = 4
    JumpWithHorse = 5
    OpenRiddenHorseInventory = 6
