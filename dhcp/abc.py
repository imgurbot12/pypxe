import enum
from typing import Any, List, Union

#** Variables **#
__all__ = [
    'find_enum',
    'ByteOperator',
    'ByteObject',
]

#** Functions **#

def find_enum(enum: enum.Enum, value: Any, default: Any = None) -> Any:
    """
    find value by value in enum object

    :param enum:    enumeration object being collected from
    :param value:   value being retrieved from enum object
    :param default: default value to return only if default is not none
    """
    if value not in enum._value2member_map_:
        if default is None:
            raise ValueError('no such value: %r in enum: %s' % (value, enum))
        return default
    return enum._value2member_map_[value]

def hexdump(raw: bytes) -> str:
    """
    convert raw-bytes into legible hex dump

    :param raw: raw bytes being parsed
    :return:    hexdump string of bytes
    """
    hex = raw.hex()
    hex = ' '.join(hex[i:i+2] for i in range(0, len(hex), 2))
    hex = '| '.join(hex[i:i+24] for i in range(0, len(hex), 24))
    hex = '\n | '.join(hex[i:i+52] for i in range(0, len(hex), 52))
    return ' | ' + hex + '\n'

#** Classes **#

class ByteOperator:
    """base class used to describe objects moving to/from bytes"""

    @staticmethod
    def from_bytes(raw: bytes) -> 'ByteOperator':
        """base class method declaration"""
        raise NotImplementedError('must be overwritten!')

    def to_bytes(self) -> bytes:
        """base class method declaration"""
        raise NotImplementedError('must be overwritten!')

class ByteObject(ByteOperator):
    """basic storage/management tool for both mac-addresses and ip-addresses"""

    def __init__(self, length: int, raw: List[int]):
        """
        :param length: length the byte-array is allowed to be
        :param raw:    list of bytes to be stored in object
        """
        # ensure values are valid
        if len(raw) != length:
            raise TypeError('invalid byte-count: %d expected: %d' % (
                len(raw), length))
        for n, num in enumerate(raw, 1):
            if num < 0 or num > 255:
                raise TypeError('%s byte: %d, invalid value: %r' % (
                    self.__class__.__name__, n, num))
        # save variables
        self._length = length
        self._addr   = bytes(raw)

    def __str__(self) -> str:
        return '0x' + self._addr.hex()

    def __eq__(self, other: Union['ByteObject', bytes]) -> bool:
        if isinstance(other, ByteObject):
            return self._addr == other._addr
        else:
            return self._addr == other

    @staticmethod
    def from_bytes(raw: bytes) -> 'ByteObject':
        """
        convert raw byte-string into address object

        :param raw: byte-string being turned into ByteObject
        :return:    newly generated address object
        """
        return ByteObject(len(raw), [c for c in raw])

    def to_bytes(self) -> bytes:
        """
        convert byte-object into bytes to pass into buffer

        :return: byte-string
        """
        return self._addr
