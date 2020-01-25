"""
global utilities used in variety of sub-libraries
"""
import enum
from typing import Any

#** Variables **#
__all__ = [
    'hexdump',
    'find_enum',
]

#** Functions **#

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
