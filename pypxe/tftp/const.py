"""
constants used throughout tftp
"""
import enum

#** Variables **#
__all__ = [
    'OpCode',
    'RequestMode'
]

#** Classes **#

class OpCode(enum.Enum):
    """operation codes for TFTP packets (RFC 1350)"""
    ReadRequest  = 1
    WriteRequest = 2
    Data         = 3
    Ack          = 4
    Error        = 5
    OptionAck    = 6

class RequestMode(enum.Enum):
    """possible request modes available for TFTP (RFC 1350)"""
    NetAscii = "netascii"
    Octet    = "octet"
    Mail     = "mail"
