"""
utilities used within tftp library to handle packets
"""
from typing import Tuple

from ..utils import *

#** Variables **#
__all__ = [
    'hexdump',
    'find_enum',
    'read_bytes',
]

#** Functions **#

def read_bytes(raw: bytes) -> Tuple[bytes, bytes]:
    """read bytes until null-byte appears marking end of string"""
    idx = raw.index(b'\x00')
    return raw[:idx], raw[idx+1:]
