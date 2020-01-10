from typing import Union

#** Variables **#
__all__ = [
    'ByteOperator',
    'FourByteObject'
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

class FourByteObject(ByteOperator):
    """basic storage/management tool for both mac-addresses and ip-addresses"""

    def __init__(self, a: int, b: int, c: int, d: int):
        """
        :param a: first octet of address
        :param b: second octet of address
        :param c: third octet of address
        :param d: fourth octet of address
        """
        for n, num in enumerate([a, b, c, d], 1):
            if num < 0 or num > 255:
                raise TypeError(
                    'ipv4 octet: %d, invalid value: %r' % (n, num))
        self._addr = bytes([a, b, c, d])

    def __eq__(self, other: Union['FourByteObject', bytes]) -> bool:
        if isinstance(other, FourByteObject):
            return self._addr == other._addr
        else:
            return self._addr == other

    @staticmethod
    def from_bytes(raw: bytes) -> 'FourByteObject':
        """
        convert raw 4byte byte-string into address object

        :param raw: 4byte byte-string being turned into ipv4
        :return:    newly generated address object
        """
        if len(raw) != 4:
            raise ValueError('ipv4.len != 4bytes')
        return _4ByteObject(*[c for c in raw])

    def to_bytes(self) -> bytes:
        """
        convert ipv4 address into bytes to pass into buffer

        :return: ipv4 address as 4byte byte-string
        """
        return self._addr
