import socket
import asyncio
from dhcp import dhcp4, dhcp6
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

def _new_handler(
    factory:   DHCPPacket,
    handler:   PacketHandler,
    interface: Optional[str] = None,
) -> asyncio.DatagramProtocol:
    """
    spawn new subclass of handler to handle incoming DHCP packets

    :param factory:   dhcp-class used to deserialize raw bytes
    :param handler:   function used to handle packets formed with factory
    :param interface: network interface to bind socket to
    :return:          new handler to handle dhcp packets
    """
    class NewHandler(_Handler):
        _factory   = factory
        _interface = None if interface is None else interface.encode('utf-8')

        def on_packet(self, pkt: DHCPPacket) -> Optional[DHCPPacket]:
            return handler(pkt)
    return NewHandler

#** Classes **#

#TODO: maybe find a way to send errors back to dhcp-server instance for logging

class _Handler(asyncio.DatagramProtocol):
    """metaclass handler for incoming udp packets built for DHCPv4"""
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
        try:
            req = self._factory.from_bytes(data)
        except:
            pass
        else:
            res = self.on_packet(req)
            if res is not None:
                self._transport.sendto(res.to_bytes(), ('255.255.255.255', 68))

#TODO: add proper logging for DHCP packets coming in / going out

class DHCPServer:
    """complete DHCP server used to handle and reply to packets"""

    def __init__(self,
        factory:   DHCPPacket,
        handler:   Optional[PacketHandler] = None,
        address:   Tuple[str, int]         = ('0.0.0.0', 67),
        interface: Optional[str]           = None,
    ):
        """
        :param factory:   dhcp packet factory (ipv4/ipv6)
        :param handler:   optional override on class packet handler
        :param address:   address to bind server to
        :param interface: network interface used to send replies
        """
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
        handle = _new_handler(self.factory, self.handler, self.interface)
        loop   = asyncio.get_event_loop()
        point  = loop.create_datagram_endpoint(handle,
            local_addr=self.address, allow_broadcast=True)
        return asyncio.Task(point)
