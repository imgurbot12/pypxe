"""
constants used throughout tftp
"""
import enum

#** Variables **#
__all__ = [
    'DefaultServerPort',

    'OpCode',
    'RequestMode',
    'ErrorCode'
]

#** Variables **#
DefaultServerPort = 69

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

class ErrorCode(enum.Enum):
    """possible error codes used in response"""
    NotDefined        = 0
    FileNotFound      = 1
    AccessViolation   = 2
    DiskFull          = 3
    IllegalOperation  = 4
    UnknownTransferID = 5
    FileAlreadyExists = 6
    NoSuchUser        = 7
