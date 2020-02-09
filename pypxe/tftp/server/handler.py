"""
helper read/write packet handlers for a single TFTP transaction
"""
import io
from typing import Optional

from .. import tftp, option
from . import ServerError, BadOpCode

#** Variables **#
__all__ = [
    'BadBlockError',

    'TFTPHandler',
    'Reader',
    'Writer',
]

#** Classes **#

#TODO: no system to support rebroadcast of the same packet is supported

class BadBlockError(ServerError):
    """server exception caused by unexpected block number"""

    def __init__(self, given: int, expected: int):
        """
        :param given:    block number given by packet
        :param expected: expected block number
        """
        super().__init__(tftp.ErrorCode.IllegalOperation,
            'bad block=%d, expected=%d ' % (given, expected))

class TFTPHandler:
    """baseclass for reader/writer tftp request handlers"""

    def __init__(self, file: io.IOBase, options: option.Options):
        """
        :param file:    file buffer being read/writen to based on handler
        :parma options: options set for read/write request
        """
        self.file    = file
        self.block   = 0
        self.options = options
        self.blksize = options.blocksize()
        self.tsize   = options.totalsize()

    @property
    def is_closed(self) -> bool:
        """return true if handler is closed"""
        return self.block == -1

    def close(self):
        """close handler object"""
        if self.block != -1:
            self.block = -1
            self.file.close()

class Reader(TFTPHandler):
    """handler used to handle read-request from bytes-buffer"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._optack = False
        self._skip   = False

    @property
    def filesize(self) -> int:
        """retrieve filesize from file object"""
        before   = self.file.tell()
        filesize = self.file.seek(0, 2)
        self.file.seek(before, 0)
        return filesize

    def index(self) -> int:
        """get location to read from based on block number"""
        return self.blksize*(self.block)

    def generate(self) -> Optional[tftp.Packet]:
        """
        respond with packet last sent already for re-broadcast

        :return: packet last sent already
        """
        # handle if already closed
        if self.is_closed:
            return None
        # generate option acknowledgement
        elif self.block == 0 and len(self.options) > 0 and not self._optack:
            self._optack = self._skip = True
            # send options acknowledgement
            options = []
            if self.blksize != 512:
                options.append(
                    option.Option(option.Param.BlockSize, self.blksize))
            if self.tsize is not None:
                options.append(
                    option.Option(option.Param.TotalSize, self.filesize))
            return tftp.OptionAcknowledgement(options)
        # handle data transfer
        elif self.index() <= self.file.tell():
            # update index to requested block if required
            index = self.index()
            if index != self.file.tell():
                self.file.seek(index, 0)
            # send data from file object
            return tftp.Data(self.block+1, self.file.read(self.blksize))

    def next(self, pkt: tftp.Packet) -> bool:
        """
        handle next incoming packet in transaction

        :param pkt: packet being recieved
        :return:    false if the transmission is complete else true
        """
        # handle if connection is already closed
        if self.is_closed:
            return False
        # raise exception on error
        elif pkt.op == tftp.OpCode.Error:
            raise Exception(f'client err[{pkt.code.name}]: {pkt.code.message}')
        # handle incoming acknowledgement packet
        elif pkt.op == tftp.OpCode.Ack:
            # handle first ack if options ackowledged packet was sent
            if self._skip:
                if pkt.block != 0:
                    raise BadBlockError(pkt.block, 0)
                self._skip = False
                return True
            # check for unexpected block number
            if pkt.block != self.block+1:
                raise BadBlockError(pkt.block, self.block+1)
            # update block number
            self.block += 1
            # check if last block acknowledged
            if self.filesize < self.index():
                return False
        # handle unexpected packet type
        else:
            raise BadOpCode(pkt.op)
        return True

    @classmethod
    def new(cls, pkt: tftp.Request, buffer: io.IOBase) -> 'Writer':
        """
        spawn a new reader object based on a read-request

        :param pkt:      read-request packet used to form reader object
        :param buffer:   buffer being read from
        :return:         new reader object to handle TFTP transaction
        """
        return cls(file=buffer, options=pkt.options)

class Writer(TFTPHandler):
    """handler used to recieve write-request and write to file"""

    def generate(self) -> Optional[tftp.Packet]:
        """
        respond with packet last sent already for re-broadcast

        :return: packet last sent already
        """
        if self.is_closed:
            return None
        return tftp.Acknowledgement(self.block)

    def next(self, pkt: tftp.Packet) -> bool:
        """
        handle next incoming packet in transaction

        :param pkt: packet being recieved
        :return:    false if the transmission is complete else true
        """
        # check if already terminated
        if self.is_closed:
            return False
        # raise exception on error
        elif pkt.op == tftp.OpCode.Error:
            raise Exception(f'client err[{pkt.code.name}]: {pkt.code.message}')
        # handle incoming block from server
        elif pkt.op == tftp.OpCode.Data:
            # error on unexpected block
            if pkt.block != self.block+1:
                raise BadBlockError(pkt.block, self.block+1)
            # add bytes from data packet to buffer
            self.file.write(pkt.data)
            # check if blocksize is too big
            if len(pkt.data) > self.blksize:
                raise ServerError(tftp.ErrorCode.IllegalOperation,
                    'invalid size=%d, block<=%d'%(len(pkt.data), self.blksize))
            # update block count
            self.block += 1
            # check if last block
            if len(pkt.data) < self.blksize:
                return False
        # handle other unexpected packets
        else:
            raise BadOpCode(pkt.op)
        return True

    @classmethod
    def new(cls, pkt: tftp.Request, buffer: io.IOBase) -> 'Writer':
        """
        spawn a new writer object based on a write-request

        :param pkt:      write-request packet used to form writer object
        :param buffer:   buffer being written to
        :return:         new writer object to handle TFTP transaction
        """
        return cls(file=buffer, options=pkt.options)
