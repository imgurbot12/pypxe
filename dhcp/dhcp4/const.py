import enum

#** Variables **#
__all__ = [
    'OpCode',
    'MessageType'
]

#** Classes **#

class OpCode(enum.Enum):
    """constants that represent valid values for OpcodeType"""
    BootRequest = 1
    BootReply   = 2

class MessageType(enum.Enum):
    """represents the possible DHCP message types - DISCOVER, OFFER, etc"""
    Discover  = 1
    Offer     = 2
    Request   = 3
    Decline   = 4
    Ack       = 5
    Nak       = 6
    Release   = 7
    Inform    = 8
