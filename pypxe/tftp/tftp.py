"""
packet crafting for TFTP protocl
"""
import struct
from typing import Tuple, List

from . import option, utils
from .const import OpCode, RequestMode

#** Variables **#
__all__ = [
    'from_bytes',

    'Packet',
    'Request',
    'OptionAcknowledgement',
    'Acknowledgement',
    'Data'
]

#** Functions **#

def from_bytes(raw: bytes) -> 'Packet':
    """
    convert raw-bytestring into TFTP packet object

    :param raw: bytestring being parsed
    :return:    TFTP packet object
    """
    op = struct.unpack('>H', raw[:2])[0]
    if op == OpCode.ReadRequest or op == OpCode.WriteRequest:
        return Request.from_bytes(raw)
    elif op == OpCode.OptionAck:
        return OptionAcknowledgement.from_bytes(raw)
    elif op == OpCode.Ack:
        return Acknowledgement.from_bytes(raw)
    elif op == OpCode.Data:
        return Data.from_bytes(raw)
    else:
        raise NotImplementedError('error type not supported yet!')
        #TODO: have not written handler for error packet

#** Classes **#

class Packet:
    op: OpCode = None

    def __str__(self) -> str:
        return '<TFTP.Packet: %s>' % self.op.name

    def to_bytes(self) -> bytes:
        raise NotImplementedError('baseclass must be overwritten!')

    def from_bytes(cls, raw: bytes) -> 'Packet':
        raise NotImplementedError('baseclass must be overwritten!')

class Request(Packet):
    """complete TFTP Request packet to start sending/recieving files"""

    def __init__(self,
        op:       OpCode,
        filename: bytes,
        mode:     RequestMode,
        options:  List[option.Option],
    ):
        """
        :param op:       request opcode (READ/WRITE)
        :param filename: filename being read/written
        :param mode:     method used to transfer file
        :param options:  extra options used to declare behavior
        """
        self.op       = op
        self.filename = filename
        self.mode     = mode
        self.options  = options

    def to_bytes(self) -> bytes:
        """
        convert request into byte-format for sending across the wire

        :return: raw bytestring generated from request
        """
        return struct.pack('>H', self.op.value)                + \
            self.filename                           + b'\x00'  + \
            bytes(self.mode.value.lower(), 'utf-8') + b'\x00'  + \
            b''.join(opt.to_bytes() for opt in self.options)

    @classmethod
    def from_bytes(cls, raw: bytes) -> 'Request':
        """
        convert raw-bytes into request object

        :param raw: byte-string being parsed
        :return:    generated request object
        """
        op            = raw[:2]
        filename, raw = utils.read_bytes(raw[2:])
        mode,     raw = utils.read_bytes(raw)
        return Request(
            op=utils.find_enum(OpCode, struct.unpack('>H', op)[0]),
            filename=filename,
            mode=utils.find_enum(RequestMode, mode.decode('utf-8').lower()),
            options=option.from_bytes(raw),
        )

class OptionAcknowledgement(Packet):
    """complete TFTP option ack to let server know opts are accepted"""
    op = OpCode.OptionAck

    def __init__(self, options: List['Option']):
        """
        :param options: list of options that have been accepted
        """
        self.options = options

    def to_bytes(self) -> bytes:
        """
        convert request into byte-format for sending across the wire

        :return: raw bytestring generated from request
        """
        return struct.pack('>H', self.op.value) + \
            b''.join(opt.to_bytes() for opt in self.options)

    @classmethod
    def from_bytes(cls, raw: bytes) -> 'OptionAcknowledgement':
        """
        convert raw-bytes into request object

        :param raw: byte-string being parsed
        :return:    generated request object
        """
        return cls(options=option.from_bytes(raw[2:]))

class Acknowledgement(Packet):
    """complete TFTP ack packet to let server know block was recieved"""
    op = OpCode.Ack

    def __init__(self, block: int):
        """
        :param block: block number being acknowledged
        """
        self.block = block

    def to_bytes(self) -> bytes:
        """
        convert request into byte-format for sending across the wire

        :return: raw bytestring generated from request
        """
        return struct.pack('>H', self.op.value) + struct.pack('>H', self.block)

    @classmethod
    def from_bytes(cls, raw: bytes) -> 'Acknowledgement':
        """
        convert raw-bytes into request object

        :param raw: byte-string being parsed
        :return:    generated request object
        """
        return cls(block=struct.unpack('>H', raw[2:])[0])

class Data(Packet):
    """complete TFTP data packet used to transfer data"""
    op = OpCode.Data

    def __init__(self, block: int, data: bytes):
        """
        :param data: raw-bytes being sent in packet
        """
        self.block = block
        self.data  = data

    def to_bytes(self) -> bytes:
        """
        convert request into byte-format for sending across the wire

        :return: raw bytestring generated from request
        """
        return struct.pack('>H', self.op.value) + \
            struct.pack('>H', self.block) + self.data

    @classmethod
    def from_bytes(cls, raw: bytes) -> 'Data':
        """
        convert raw-bytes into request object

        :param raw: byte-string being parsed
        :return:    generated request object
        """
        return cls(
            block=struct.unpack('>H', raw[2:4])[0],
            data=raw[4:],
        )
