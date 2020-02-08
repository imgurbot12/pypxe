"""
implementation of TFTP Request Options (RFC 2347-2349)
"""
import enum
from typing import List, Any, Optional

from . import utils

#** Variables **#
__all__ = [
    'from_bytes',

    'Param',
    'Option',
    'Options',
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

class Options:
    """dict/list hybrid allowing for quick-lookups of options"""

    def __init__(self, options: List[Option]):
        """
        :param options: list of already collection options
        """
        self._dict = {opt.name.value:n for n, opt in enumerate(options, 0)}
        self._list = options

    def __len__(self) -> int:
        return len(self._list)

    def __iter__(self) -> List['Option']:
        return iter(self._list)

    def __contains__(self, k: Param) -> bool:
        return k.value in self._dict

    def __getitem__(self, k: Any) -> 'Option':
        idx = self._dict[k.value] if isinstance(k, Param) else k
        return self._list[idx]

    def get(self, k: Param, d: Any = None) -> Optional[int]:
        """
        retrieve an item from the list if the paramter exists

        :param k: key being used to retrieve value
        :param d: default to return if none
        :return:  option object or default value if not found
        """
        return self[k].value if k in self else d

    def blocksize(self) -> int:
        """
        retrive block-size option if given in list or default

        :return: requested block-size for transfer
        """
        return self.get(Param.BlockSize, 512)

    def timeout(self) -> Optional[int]:
        """
        retrieve timeout in seconds if given in list or default

        :return: requested/accepeted timeout value if given or none
        """
        return self.get(Param.Timeout, None)

    def totalsize(self) -> Optional[int]:
        """
        retrieve total-size option if given in list or default

        :return: requested/accepted total-size value if given or none
        """
        return self.get(Param.TotalSize, None)
