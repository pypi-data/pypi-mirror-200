"""
cubelib.p
===========================================================
Module that contains the abstractions for protocol packets.
"""

from dataclasses import dataclass
from inspect import signature
from types import ModuleType
from typing import Union
import zlib

from cubelib.types import VarInt, SafeBuff, Optional
from cubelib.enums import state, bound
from cubelib.errors import BadPacketException, BufferExhaustedException, DecoderException


@dataclass
class Packet:
    """
    Class that represents protocol packet structure.

    Parameters
    ----------
    id
        Packet ID
    payload
        Packet payload
    bound
        Bound of the packet
    compressed
        Show packet was compressed or not
    """

    id: int
    payload: bytes
    bound: Union[bound, None] = None
    compressed: Union[bool, None] = None

    def _build_plain(self) -> bytes:
        """Build binary plain packet by class fields."""

        r = VarInt.build(self.id)
        r += self.payload
        r = VarInt.build(len(r)) + r
        return r

    def _build_compressed(self, threshold: int) -> bytes:
        """Build binary compressed packet by class fields."""

        if len(self.payload) <= threshold:

            r = VarInt.build(0)  # set data length 0
            r += VarInt.build(self.id)
            r += self.payload

        else:

            c = VarInt.build(self.id) + self.payload
            r = VarInt.build(len(c))  # set data length
            r += zlib.compress(c)

        r = VarInt.build(len(r)) + r
        return r

    def build(self, threshold: int = -1) -> bytes:
        """Build binary packet compressed or not, defined, by threshold."""

        if threshold == -1:
            return self._build_plain()
        return self._build_compressed(threshold)

    @staticmethod
    def _read_plain(buff: bytes, bound: bound):
        """Read binary plain packet into packet class instance."""

        buff = SafeBuff(buff)
        try:
            length = VarInt.destroy(buff)
        except RuntimeError as e:
            raise BadPacketException("Invalid packet length field!") from e

        if not 2097151 >= length > 0:
            raise BadPacketException(f'Packet length field {length} invalid! (2097151 >= length > 0)')

        try:
            id, fl = VarInt.cntd_destroy(buff)
        except RuntimeError as e:
            raise BadPacketException("Invalid packet id field!") from e

        payload = buff.read(length - fl)
        tail = buff.read()
        return (Packet(id, payload, bound, False), tail)

    @staticmethod
    def _read_compressed(buff: bytes, bound: bound, threshold):
        """Read binary compressed packet into packet class instance."""

        buff = SafeBuff(buff)
        try:
            p_length = VarInt.destroy(buff)
        except RuntimeError as e:
            raise BadPacketException("Invalid packet length field!") from e

        if not 2097151 >= p_length > 0:
            raise BadPacketException(f'Packet length field {p_length} invalid! (2097151 >= length > 0)')

        try:
            d_length, fl = VarInt.cntd_destroy(buff)
        except RuntimeError as e:
            raise BadPacketException("Invalid data length field!") from e

        if not 2097151 >= d_length >= 0:
            raise BadPacketException(f'Data length field {d_length} invalid! (2097151 >= length > 0)')

        data = SafeBuff(buff.read(p_length - fl))
        tail = buff.read()

        if d_length == 0:
            pass
        elif d_length > threshold:
            data = SafeBuff(zlib.decompress(data.read()))
        else:
            raise BadPacketException((f'compressed data length ({d_length}) is '
                                      f'less than the threshold ({threshold})'))

        id = VarInt.destroy(data)
        payload = data.read()

        return (Packet(id, payload, bound, True), tail)

    def resolve(self, state: state, protocol: ModuleType):
        """Resolve packet class into packet abstraction class."""

        try:
            pclass = getattr(getattr(protocol, f"{self.bound.name}Bound"), state.name).map[self.id]
        except KeyError:
            raise DecoderException(
                f'Bad packet ID! There is no packet with id #{self.id} in {protocol.__name__}.{self.bound.name}Bound.{state.name}')

        if not pclass:
            return NotImplementedPacket(hex(self.id), self.bound, protocol.name)
        return pclass.destroy(self.payload)

    def __eq__(first, second) -> bool:
        """Checks packets equality."""

        if first.__class__ != second.__class__:
            return False

        if first.id != second.id:
            return False

        if first.payload != second.payload:
            return False

        if first.bound != second.bound:
            return False

        return True

def readPacketsStream(buff: bytes, threshold: int, bound: bound, packets: list) -> bytes:
    """
    Read all completed packets in binary buffer and store it in list.
    """

    while 7:
        if buff:
            try:
                if threshold >= 0:
                    packet, tail = Packet._read_compressed(buff, bound, threshold)
                else:
                    packet, tail = Packet._read_plain(buff, bound)
                packets.append(packet)
                buff = tail
                continue            
            except BufferExhaustedException:                
                return buff
        return buff

def rrPacketsStream(buff: bytes, threshold: int, bound: bound, state: state, protocol: ModuleType, packets: list):
    """
    Read Resolve Packets Stream

    readPacketsStream + Night.resolve()
    Read all completed packets in binary buffer, resolve it into abstract classes and store it in list.
    """

    pcks = []
    buff = readPacketsStream(buff, threshold, bound, pcks)
    [packets.append(p.resolve(state, protocol)) for p in pcks]
    return buff

@dataclass
class NotImplementedPacket:
    """
    Class for not implemented packets that can't be resolved into the abstracted class.

    Parameters
    hex_id
        Hexadecimal id of packet as a string
    bound
        Bound of the packet
    ver_name
        Protocol version name
    """

    hex_id: str
    bound: bound
    ver_name: str


class Night:
    """
    Parent class for all packet abstract clases.
    """

    @classmethod
    def destroy(cls, buff: bytes):
        """
        Read abstract class annotations and decode binary buffer with annotated types.
        Fill fields of abstract class with gotten values.
        """

        self = object.__new__(cls)
        if not hasattr(self, '__annotations__'):
            return self  # zero-body

        buff = SafeBuff(buff)
        an = self.__annotations__

        for name in an:
            TYPE = an[name]

            if isinstance(TYPE, Optional):
                if not TYPE.is_legit(getattr(self, TYPE.field_name)):
                    continue
                TYPE = TYPE.type
            try:
                val = TYPE.destroy(buff)
            except Exception as e:  # NOQA
                raise DecoderException from e

            size = len(val) if isinstance(val, str) else val
            if hasattr(TYPE, 'max'):
                if size > TYPE.max:
                    raise DecoderException(f'Packet field [{name}] larger than maximum! {size} > {TYPE.max}')

            if hasattr(TYPE, 'min'):
                if size < TYPE.min:
                    raise DecoderException(f'Packet field [{name}] thinker than minimum! {size} < {TYPE.max}')

            setattr(self, name, val)

        try:
            unex = buff.read(1) + buff.read()
            raise DecoderException(f"Packet [{cls.__name__}] fields over, but packet's buffer not empty yet! Unexpected data len: {len(unex)} Data: {unex}")
        except BufferExhaustedException:
            pass

        return self

    def _build_into_packet(self) -> Packet:
        """
        Build abstract class into packet class.
        """

        payload = b""
        an = self.__annotations__ if hasattr(self, '__annotations__') else None
        if an:
            for name in an:
                try:
                    if isinstance(an[name], Optional):
                        if not hasattr(self, name):
                            break

                        if getattr(self, an[name].field_name) != an[name].excepted_val:
                            print(("We resolved your optional field and his tweaker is shutted down. "
                                   "I'll hope you know what you're doin'"))

                    payload += an[name].build(getattr(self, name))
                except AttributeError:
                    raise Exception(f'Failed to get {name}. Empty?')

        return Packet(self._id(), payload, self._bound(), False)

    def build(self, cmp_threshold: int = -1) -> bytes:
        """Build abstract class into binary."""

        return self._build_into_packet().build(cmp_threshold)

    def __repr__(self) -> str:
        """Show data in abstract class fields like dataclass."""

        full_name = str(self.__class__).split("'")[1].split(".")

        def typo(x): return f"'{x}'" if type(x) is str else x  # NOQA: E704

        out = f'{full_name[-2]}.{full_name[-1]}('

        try:
            an = self.__annotations__
        except AttributeError:
            return out + ')'

        out += ', '.join([f'{a}={typo(getattr(self, a) if hasattr(self, a) else "UNSET BO" if not an[a].is_legit(getattr(self, an[a].field_name)) else "UNSET!?")}' for a in an])

        return out + ')'

    def __init__(self, *args):
        """Fill abstract class with given in args values."""

        if not hasattr(self, '__annotations__'):
            return

        def has_optional(an: dict):
            for a in an:
                if isinstance(an[a], Optional):
                    return True
            return False

        an = self.__annotations__

        if len(an) != len(args) and not has_optional(an) or len(args) == 0:
            v = f'{self.__class__.__name__}({", ".join([f"{a}: {an[a].__name__ if isinstance(an[a], type) else an[a].__class__.__name__}" for a in an])})'
            raise ValueError(f'{v} requires {len(an)} arguments but you provided only {len(args)}!')

        for i, a in enumerate(an):
            if isinstance(an[a], Optional):
                if not an[a].is_legit(getattr(self, an[a].field_name)):                    
                    print(f"Annotations are over but arguments are not. Optionals mismatch?") if len(args) != i else None
                    return
            setattr(self, a, args[i])

    @classmethod
    def _id(class_) -> int:
        """Find abstract packet's ID in protocol class map."""

        from cubelib import proto
        w = str(class_).split("'")[1].split('.')[:-1][2:]
        map = getattr(getattr(getattr(proto, w[0]), w[1]), w[2]).inv_map
        return map[class_]

    @classmethod
    def _bound(class_) -> int:
        """Find abstract packet's bound in protocol module."""

        w = str(class_).split("'")[1].split('.')[:-1][2:]
        return getattr(bound, w[1][:-5])

    def __eq__(first, second) -> bool:
        """Check abstract classes equality."""

        if first.__class__ != second.__class__:
            return False

        try:
            an = first.__class__.__annotations__
        except AttributeError:
            return True

        for a in an:
            if getattr(first, a) != getattr(second, a):
                return False
        return True
