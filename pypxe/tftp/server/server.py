import io
import sys
import socket
import asyncio
import logging
import traceback
from typing import Callable, Tuple, Optional

from .. import tftp
from . import ServerError, BadOpCode
from .handler import Reader, Writer

#** Variables **#

RequestHandler = Callable[[tftp.Request], Optional[io.IOBase]]

#** Functions **#

def _logger(name: str, loglevel: int) -> logging.Logger:
    """
    spawn logging instance w/ the given loglevel

    :param name:     name of the logging instance
    :param loglevel: level of verbosity on logging instance
    """
    log = logging.getLogger(name)
    log.setLevel(loglevel)
    # spawn handler
    fmt     = logging.Formatter(
        '%(asctime)s [%(process)d] [%(levelname)s] %(message)s')
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(loglevel)
    log.handlers.append(handler)
    return log

def _new_handler(
    log:       logging.Logger,
    reader:    RequestHandler,
    writer:    RequestHandler,
    interface: Optional[str] = None,
) -> asyncio.DatagramProtocol:
    """
    spawn new subclass of handler to handle incoming TFTP packets

    :param log:       logging instance used for debugging
    :param reader:    function handler used to handle tftp read requests
    :param writer:    function handler used to handle tftp write requests
    :param interface: network interface to bind socket to
    :return:          new handler to handle tftp packets
    """
    class NewHandler(_Handler):
        _log       = log
        _on_read   = reader
        _on_write  = writer
        _interface = None if interface is None else interface.encode('utf-8')
    return NewHandler

#** Classes **#

class _Handler(asyncio.DatagramProtocol):
    """baseclass packet handler used to handle incoming TFTP packets"""
    _log:       logging.Logger
    _on_read:   RequestHandler
    _on_write:  RequestHandler
    _interface: Optional[bytes] = None

    def connection_made(self, transport: asyncio.DatagramTransport):
        self._transport = transport
        self._connstate = {}
        # bind to given interface if given
        if self._interface is not None:
            sock = self._transport.get_extra_info('socket')
            sock.setsockopt(socket.SOL_SOCKET,
                socket.SO_BINDTODEVICE, self._interface)

    def _kill_transaction(self, addr: str):
        """kill any transactions taking place w/ an existing address"""
        _, handler = self._connstate[addr]
        handler.close()
        del self._connstate[addr]

    def on_packet(self, req: tftp.Packet, addr: str) -> Optional[tftp.Packet]:
        # check if address is newly connected to service
        if addr not in self._connstate:
            if not req.is_request():
                raise BadOpCode(req.op)
            elif req.op == tftp.OpCode.ReadRequest:
                # check if handler wants to handle read
                buffer = self._on_read(req)
                if buffer is None:
                    raise ServerError(
                        tftp.ErrorCode.FileNotFound, 'file not found')
                # spawn reader object
                reader = Reader(buffer, req.options)
                self._connstate[addr] = (tftp.OpCode.ReadRequest, reader)
                return reader.generate()
            elif req.op == tftp.OpCode.WriteRequest:
                # check if handler wants to handle write
                buffer = self._on_write(req)
                if buffer is None:
                    raise ServerError(
                        tftp.ErrorCode.FileAlreadyExists, 'file already exists')
                # spawn writer object
                writer = Writer(buffer, req.options)
                self._connstate[addr] = (tftp.OpCode.WriteRequest, writer)
                return writer.generate()
        # if address was already messaged previously
        else:
            if req.is_request():
                self._kill_transaction(addr)
            # handle active read
            opcode, handler = self._connstate[addr]
            if opcode == tftp.OpCode.ReadRequest:
                next = handler.next(req)
                res  = handler.generate()
                if not next:
                    self._kill_transaction(addr)
                return res
            else:
                raise NotImplementedError('write no supported yet')

    def datagram_received(self, data: bytes, addr: Tuple[str, int]):
        """
        handle incoming dhcp-packet and send appropriate response

        :param data: raw-bytes being collected from client
        :param addr: address request is coming from
        """
        # retrieve request object if possible
        try:
            req = tftp.from_bytes(data)
        except Exception as e:
            self._log.debug('failed to parse TFTP packet: %s' % e)
            return
        # attempt to retrieve response
        try:
            print(req)
            res = self.on_packet(req, '%s:%d' % addr)
        except ServerError as e:
            res = tftp.Error(e.code, e.message.encode('utf-8'))
        except Exception as e:
            self._log.error('failed to handle packet: %s' % e)
            traceback.print_exc()
            return
        # attempt to send response
        try:
            print(res)
            if res is not None:
                self._transport.sendto(res.to_bytes(), addr)
        except Exception as e:
            self._log.error('unable to send response: %s' % e)
            traceback.print_exc()

class TFTPServer:
    """complete TFTP server used to handle and reply to packets"""

    def __init__(self,
        reader:    Optional[RequestHandler] = None,
        writer:    Optional[RequestHandler] = None,
        address:   Tuple[str, int]          = ('0.0.0.0', 69),
        interface: Optional[str]            = None,
        debug:     bool                     = False,
    ):
        """
        :param reader:    read request handler for TFTP requests
        :param writer:    write request handler for TFTP requests
        :param address:   address to bind server to
        :param interface: network interface used to send replies
        :param debug:     enable debugging if true
        """
        loglevel          = logging.DEBUG if debug else logging.INFO
        self.log          = _logger('dhcp.server', loglevel)
        self.address      = address
        self.interface    = interface
        self.reader       = self.reader if reader is None else reader
        self.writer       = self.writer if writer is None else writer

    def reader(self, req: tftp.Request) -> Optional[io.IOBase]:
        pass

    def writer(self, req: tftp.Request) -> Optional[io.IOBase]:
        pass

    def run_forever(self) -> asyncio.Task:
        """
        spawn DHCP server and start handling incoming packets

        :return: asyncio future object in charge of running server
        """
        handle = _new_handler(
            log=self.log,
            reader=self.reader,
            writer=self.writer,
            interface=self.interface
        )
        loop   = asyncio.get_event_loop()
        point  = loop.create_datagram_endpoint(handle, local_addr=self.address)
        return asyncio.Task(point)
