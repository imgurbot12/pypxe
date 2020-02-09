"""
generic DHCP server implementation useful for both DHCPv4 and DHCPv6
"""
import sys
import socket
import asyncio
import logging
import traceback
from . import dhcp4, dhcp6
from typing import Union, Callable, Optional, Tuple

#** Variables **#
__all__ = [
    'DHCPPacket',
    'PacketHandler',

    'DHCPServer',
]

DHCPPacket    = Union[dhcp4.DHCPv4, dhcp6.DHCPv6]
PacketHandler = Callable[[DHCPPacket], Optional[DHCPPacket]]

#** Function **#

def _logger(name: str, loglevel: int) -> logging.Logger:
    """
    spawn logging instance w/ the given loglevel

    :param name:     name of the logging instance
    :param loglevel: level of verbosity on logging instance
    """
    log = logging.getLogger(name)
    log.setLevel(loglevel)
    # spawn handler
    fmt     = logging.Formatter('[%(process)d] [%(levelname)s] %(message)s')
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(fmt)
    handler.setLevel(loglevel)
    log.handlers.append(handler)
    return log

def _new_handler(
    log:       logging.Logger,
    factory:   DHCPPacket,
    handler:   PacketHandler,
    interface: Optional[str] = None,
) -> asyncio.DatagramProtocol:
    """
    spawn new subclass of handler to handle incoming DHCP packets

    :param log:       logging instance used for debugging
    :param factory:   dhcp-class used to deserialize raw bytes
    :param handler:   function used to handle packets formed with factory
    :param interface: network interface to bind socket to
    :return:          new handler to handle dhcp packets
    """
    class NewHandler(_Handler):
        _log       = log
        _factory   = factory
        _interface = None if interface is None else interface.encode('utf-8')

        def on_packet(self, pkt: DHCPPacket) -> Optional[DHCPPacket]:
            return handler(pkt)
    return NewHandler

#** Classes **#

class _Handler(asyncio.DatagramProtocol):
    """metaclass handler for incoming udp packets built for DHCPv4"""
    _log:       logging.Logger
    _factory:   DHCPPacket
    _interface: Optional[bytes] = None

    def connection_made(self, transport: asyncio.DatagramTransport):
        self._transport = transport
        # bind to given interface if given
        if self._interface is not None:
            sock = self._transport.get_extra_info('socket')
            sock.setsockopt(socket.SOL_SOCKET,
                socket.SO_BINDTODEVICE, self._interface)

    def on_packet(self, req: DHCPPacket) -> Optional[DHCPPacket]:
        raise NotImplementedError('on-packet handler not declared')

    def datagram_received(self, data: bytes, addr: Tuple[str, int]):
        """
        handle incoming dhcp-packet and send appropriate response

        :param data: raw-bytes being collected from client
        :parma addr: address request is coming from
        """
        # retrieve request object if possible
        try:
            req = self._factory.from_bytes(data)
        except Exception as e:
            self._log.debug('(%s) failed to parse DHCP: %s' % (addr[0], e))
            return
        # attempt to retrieve response
        try:
            res = self.on_packet(req)
        except Exception as e:
            self._log.error('(%s) failed to handle packet: %s' % (addr[0], e))
            print('\n%s' % traceback.format_exc(), file=sys.stderr)
            return
        # attempt to send response
        try:
            if res is not None:
                self._transport.sendto(res.to_bytes(), ('255.255.255.255', 68))
        except Exception as e:
            self._log.error('(%s) unable to send response: %s' % (addr[0], e))
            print('\n%s' % traceback.format_exc(), file=sys.stderr)

class DHCPServer:
    """complete DHCP server used to handle and reply to packets"""

    def __init__(self,
        factory:   DHCPPacket,
        handler:   Optional[PacketHandler] = None,
        address:   Tuple[str, int]         = ('0.0.0.0', 67),
        interface: Optional[str]           = None,
        debug:     bool                    = False,
    ):
        """
        :param factory:   dhcp packet factory (ipv4/ipv6)
        :param handler:   optional override on class packet handler
        :param address:   address to bind server to
        :param interface: network interface used to send replies
        :param debug:     enable debugging if true
        """
        loglevel       = logging.DEBUG if debug else logging.INFO
        self.log       = _logger('dhcp.server', loglevel)
        self.factory   = factory
        self.address   = address
        self.interface = interface
        self.handler   = self.handler if handler is None else handler

    def handler(self, pkt: DHCPPacket) -> Optional[DHCPPacket]:
        pass

    def run_forever(self) -> asyncio.Task:
        """
        spawn DHCP server and start handling incoming packets

        :return: asyncio future object in charge of running server
        """
        handle = _new_handler(
            log=self.log,
            factory=self.factory,
            handler=self.handler,
            interface=self.interface
        )
        loop   = asyncio.get_event_loop()
        point  = loop.create_datagram_endpoint(handle,
            local_addr=self.address, allow_broadcast=True)
        self.log.info('Serving DHCP on %s port %d' % self.address)
        return asyncio.Task(point)
