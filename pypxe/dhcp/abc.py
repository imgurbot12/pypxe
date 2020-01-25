"""
base objects and useful functions used as base of other classes
"""
import enum
from typing import Any, List, Union

from ..utils import *

#** Variables **#
__all__ = [
    'hexdump',
    'find_enum',

    'ByteOperator',
    'ByteObject',
]

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
