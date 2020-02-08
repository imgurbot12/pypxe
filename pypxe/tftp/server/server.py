"""
server definition and handler design used to send/recieve incoming TFTP packets
"""
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
__all__ = [
    'RequestHandler',
    'CallbackHandler',

    'TFTPServer',
]

#: function definition used to give file-object for reading/writing
RequestHandler  = Callable[[tftp.Request], Optional[io.IOBase]]

#: function definition for retrieving file-object after read/write request
CallbackHandler = Callable[[tftp.OpCode, io.IOBase], None]

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
        '[%(process)d] [%(levelname)s] %(message)s')
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(fmt)
    handler.setLevel(loglevel)
    log.handlers.append(handler)
    return log

def _new_handler(
    log:       logging.Logger,
    reader:    RequestHandler,
    writer:    RequestHandler,
    callback:  CallbackHandler,
    interface: Optional[str] = None,
) -> asyncio.DatagramProtocol:
    """
    spawn new subclass of handler to handle incoming TFTP packets

    :param log:       logging instance used for debugging
    :param reader:    function handler used to handle tftp read requests
    :param writer:    function handler used to handle tftp write requests
    :param callback:  function called on completion of read/write request
    :param interface: network interface to bind socket to
    :return:          new handler to handle tftp packets
    """
    class NewHandler(_Handler):
        _log       = log
        _on_read   = reader
        _on_write  = writer
        _callback  = callback
        _interface = None if interface is None else interface.encode('utf-8')
    return NewHandler

#** Classes **#

class _Handler(asyncio.DatagramProtocol):
    """baseclass packet handler used to handle incoming TFTP packets"""
    _log:       logging.Logger
    _on_read:   RequestHandler
    _on_write:  RequestHandler
    _callback:  CallbackHandler
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
        if addr in self._connstate:
            _, handler = self._connstate[addr]
            handler.close()
            del self._connstate[addr]

    def on_packet(self, pkt: tftp.Packet, addr: str) -> Optional[tftp.Packet]:
        # check if address is newly connected to service
        if addr not in self._connstate:
            if not pkt.is_request():
                raise BadOpCode(pkt.op)
            # log request
            self._log.info('(%s) req=%-12s file=%s block=%d' % (
                addr.split(':')[0],
                pkt.op.name,
                pkt.filename.decode(),
                pkt.options.blocksize()
            ))
            # handle read/write request
            if pkt.op == tftp.OpCode.ReadRequest:
                # check if handler wants to handle read
                buffer = self._on_read(pkt)
                if buffer is None:
                    raise ServerError(
                        tftp.ErrorCode.FileNotFound, 'file not found')
                # spawn reader object
                reader = Reader(buffer, pkt.options)
                self._connstate[addr] = (pkt, reader)
                return reader.generate()
            elif pkt.op == tftp.OpCode.WriteRequest:
                # check if handler wants to handle write
                buffer = self._on_write(pkt)
                if buffer is None:
                    raise ServerError(
                        tftp.ErrorCode.FileAlreadyExists, 'file already exists')
                # spawn writer object
                writer = Writer(buffer, pkt.options)
                self._connstate[addr] = (pkt, writer)
                return writer.generate()
        # if address was already messaged previously
        else:
            if pkt.is_request():
                raise BadOpCode(pkt.op)
            # handle active read
            request, handler = self._connstate[addr]
            next = handler.next(pkt)
            res  = handler.generate()
            if not next:
                handler.file.seek(0, 0)
                self._callback(request, handler.file)
                self._kill_transaction(addr)
            return res

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
        addrstr = '%s:%d' % addr
        try:
            res = self.on_packet(req, addrstr)
        except ServerError as e:
            self._log.error('(%s) %s' % (addr[0], e))
            self._kill_transaction(addrstr)
            res = tftp.Error(e.code, e.message.encode('utf-8'))
        except Exception as e:
            # print error
            self._log.error('(%s) failed to handle packet: %s' % (addr[0], e))
            print('\n%s' % traceback.format_exc(), file=sys.stderr)
            # format response
            self._kill_transaction(addrstr)
            res = tftp.Error(tftp.ErrorCode.NotDefined,
                b'internal server error occured')
        # attempt to send response
        try:
            if res is not None:
                self._transport.sendto(res.to_bytes(), addr)
        except Exception as e:
            self._log.error('unable to send response: %s' % e)
            traceback.print_exc()

class TFTPServer:
    """complete TFTP server used to handle and reply to packets"""

    def __init__(self,
        reader:    Optional[RequestHandler]  = None,
        writer:    Optional[RequestHandler]  = None,
        callback:  Optional[CallbackHandler] = None,
        address:   Tuple[str, int]           = ('0.0.0.0', 69),
        interface: Optional[str]             = None,
        debug:     bool                      = False,
    ):
        """
        :param reader:    read request handler for TFTP requests
        :param writer:    write request handler for TFTP requests
        :param callback:  callback called after completion of read/write op
        :param address:   address to bind server to
        :param interface: network interface used to send replies
        :param debug:     enable debugging if true
        """
        loglevel          = logging.DEBUG if debug else logging.INFO
        self.log          = _logger('tftp.server', loglevel)
        self.address      = address
        self.interface    = interface
        self.reader       = self.reader if reader is None else reader
        self.writer       = self.writer if writer is None else writer
        self.callback     = self.callback if callback is None else callback

    def reader(self, req: tftp.Request) -> Optional[io.IOBase]:
        pass

    def writer(self, req: tftp.Request) -> Optional[io.IOBase]:
        pass

    def callback(self, req: tftp.Request, file: io.IOBase):
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
            callback=self.callback,
            interface=self.interface
        )
        loop   = asyncio.get_event_loop()
        point  = loop.create_datagram_endpoint(handle, local_addr=self.address)
        self.log.info('Serving TFTP on %s port %d' % self.address)
        return asyncio.Task(point)
