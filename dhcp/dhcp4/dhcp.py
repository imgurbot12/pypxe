import enum
import struct
from typing import List

from .. import abc
from .. import net
from . import const
from . import option
from ..net import iana

#** Variables **#
__all__ = [
    'IpZero'
    'magic_cookie',

    'DHCPv4',
]

IpZero       = net.Ipv4(0, 0, 0, 0)
magic_cookie = bytes([0x63, 0x82, 0x53, 0x63])

#** Classes **#

class TransactionID(abc.ByteObject):
    """used to match DHCP replies to their original request as in RFC 951"""

    @staticmethod
    def new() -> 'TransactionID':
        return TransactionID(4, [random.getrandbits(8) for _ in range(4)])

class DHCPv4(abc.ByteOperator):
    """
    DHCP over Ipv4 as defined in RFC 1541.
    this object handles serlization & deserlization
    """

    def __init__(self,
        op:            const.OpCode,
        trans_id:      TransactionID,
        client_hwaddr: net.MacAddress,
        options:       List[option.Option],
        htype:         iana.HWType         = iana.HWType.Ethernet,
        hops:          int                 = 0,
        secs:          int                 = 0,
        flags:         int                 = 0,
        client_addr:   net.Ipv4            = IpZero,
        your_addr:     net.Ipv4            = IpZero,
        server_addr:   net.Ipv4            = IpZero,
        gateway_addr:  net.Ipv4            = IpZero,
        server_name:   bytes               = b'',
        boot_file:     bytes               = b'',
    ):
        """
        :param op:            DHCP operation code (request/reply)
        :param trans_id:      transaction-id used to track communication trail
        :param client_hwaddr: client's' hardware address used in assignment
        :param options:       dhcp options used for attaching addional info
        :param htype:         hardware type (method of transmission)
        :param hops:          number of completed hops on relay (default = 0)
        :param secs:          secs since client started trying to boot
        :param flags:         unused extra flags for dhcp definition (always 0)
        :param client_addr:   client's existing ip-addres (default=0.0.0.0)
        :param your_addr:     newly assigned client ip-address in offer
        :param server_addr:   ip of next server to use in bootstrap
        :param gateway_addr:  relay agent ip-address
        :param server_name:   optional server host-name
        :param boot_file:     boot-file name used in PXE to declare image file
        """
        self.op            = op
        self.xid           = trans_id
        self.client_hwaddr = client_hwaddr
        self.options       = options
        self.htype         = htype
        self.hlen          = client_hwaddr._length
        self.hops          = hops
        self.secs          = secs
        self.flags         = flags
        self.client_addr   = client_addr
        self.your_addr     = your_addr
        self.server_addr   = server_addr
        self.gateway_addr  = gateway_addr
        self.server_name   = server_name
        self.boot_file     = boot_file

    def to_bytes(self) -> bytes:
        """
        convert DHCPv4 object into bytes

        :return: byte-string representing serialized DHCPv4 object
        """
        hwaddr = self.client_hwaddr.to_bytes()
        return bytes([self.op.value,self.htype.value,self.hlen,self.hops]) + \
                self.xid.to_bytes()                                        + \
                struct.pack('>H', self.secs)                               + \
                struct.pack('>H', self.flags)                              + \
                self.client_addr.to_bytes()                                + \
                self.your_addr.to_bytes()                                  + \
                self.server_addr.to_bytes()                                + \
                self.gateway_addr.to_bytes()                               + \
                hwaddr + bytes(16)[len(hwaddr):]                           + \
                self.server_name + bytes(64-len(self.server_name))         + \
                self.boot_file + bytes(128-len(self.boot_file))            + \
                magic_cookie                                               + \
                b''.join(opt.to_bytes() for opt in self.options)           + \
                bytes((255, ))

    @staticmethod
    def from_bytes(raw: bytes) -> 'DHCPv4':
        """
        convert raw byte-string into DHCPv4 object

        :param raw: raw byte-string to be parsed and converted
        :return:    generated DHCPv4 packet object
        """
        hlen       = int(raw[2])
        end_hwaddr = 28+hlen
        return DHCPv4(
            op=raw[0],
            htype=raw[1],
            hlen=hlen,
            hops=raw[4],
            trans_id=TransactionID.from_bytes(raw[4:8]),
            secs=struct.unpack('>H', raw[8:10])[0],
            flags=struct.unpack('>H', raw[10:12])[0],
            client_addr=net.Ipv4.from_bytes(raw[12:16]),
            your_addr=net.Ipv4.from_bytes(raw[16:20]),
            server_addr=net.Ipv4.from_bytes(raw[20:24]),
            gateway_addr=net.Ipv4.from_bytes(raw[24:28]),
            client_hwaddr=net.MacAddress.from_bytes(raw[28:end_hwaddr]),
            server_name=raw[end_hwaddr:end_hwaddr+64].rstrip('\x00'),
            boot_file=raw[end_hwaddr+64:end_hwaddr+192].rstrip('\x00'),
            options=[],
        )
        #TODO: opcode is not translated to enum on deserialization
        #TODO: options are not parsed
        #TODO: to/from bytes has not yet been checked
