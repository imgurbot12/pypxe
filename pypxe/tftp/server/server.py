"""
"""
import asyncio
from typing import Tuple

from .. import tftp

#** Variables **#

#** Classes **#

class _Handler(asyncio.DatagramProtocol):

    def connection_made(self, transport: asyncio.DatagramTransport):
        print('connection made')
        self._transport = transport

    def datagram_received(self, data: bytes, addr: Tuple[str, int]):
        """
        handle incoming dhcp-packet and send appropriate response

        :param data: raw-bytes being collected from client
        :parma addr: address request is coming from
        """
        pass

loop = asyncio.get_event_loop()
t    = loop.create_datagram_endpoint(handle, local_addr=('0.0.0.0', 8080))
loop.run_until_complete(t)
loop.run_forever()
