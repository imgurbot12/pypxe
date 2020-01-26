"""
implementation of TFTP Request Options (RFC 2347-2349)
"""
import enum
from typing import List

from . import utils

#** Variables **#
__all__ = [
    'from_bytes',

    'Param',
    'Option'
]

#** Variables **#

class Param(enum.Enum):
    """possible options available"""
    BlockSize = b'blksize'
    Timeout   = b'timeout'
    TotalSize = b'tsize'

#** Functions **#

def from_bytes(raw: bytes) -> List['Option']:
    """
    parse list of options from byte-string

    :param raw: byte-string being parsed
    :return:    list of option objects
    """
    # retrieve options
    (options, n) = ([], 0)
    while n < len(raw):
        # parse option from raw-bytes
        opt = Option.from_bytes(raw[n:])
        options.append(opt)
        # update index based on length of name and value
        n += len(opt.name.value) + len(str(opt.value)) + 2
    return options

#** Classes **#

class Option:
    """baseclass option object which handles serlization/deserialization"""

    def __init__(self, name: Param, value: int):
        """
        :param name:  name of option being passed
        :param value: value of option as an integer
        """
        self.name  = name
        self.value = value

    def to_bytes(self) -> bytes:
        """convert option into byte-string"""
        return self.name.value + b'\x00' + \
            bytes(str(self.value), 'utf-8') + b'\x00'

    @classmethod
    def from_bytes(cls, raw: bytes) -> 'Option':
        """
        convert raw-bytes into option object

        :param raw: byte-string being parsed
        :return:    generated option object
        """
        name,  raw = utils.read_bytes(raw)
        value, raw = utils.read_bytes(raw)
        return cls(
            utils.find_enum(Param, name),
            int(value.decode('utf-8'))
        )
