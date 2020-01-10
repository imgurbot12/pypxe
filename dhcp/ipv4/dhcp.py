from . import abc
from . import option
from typing import List

#** Variables **#
__all__ = [
    'Ipv4',
    'MacAddress',
    'DHCPv4',
]

#** Classes **#

class Ipv4(abc.FourByteObject):
    """basic ipv4 type used to compare/store ip addresses"""

    def __str__(self) -> str:
        return '<ipv4: %s>' % self.to_string()

    @staticmethod
    def from_string(ip: str) -> 'Ipv4':
        """
        convert ipv4 string into ipv4 object

        :param ip: ipv4 string
        :return:   newly generated ipv4 object
        """
        octets = ip.split('.')
        if len(octets) != 4 or not all(grp.isdigit() for grp in octets):
            raise TypeError('invalid ipv4: %s' % ip)
        return Ipv4(*[int(grp) for grp in octets])

    def to_string(self) -> str:
        """
        convert ipv4 object into string format

        :return: string formatted ipv4-address
        """
        return '%d.%d.%d.%d' % tuple(self._addr)

class MacAddress(abc.FourByteObject):
    """basic mac-address type used to compare/store mac addresses"""

    def __str__(self) -> str:
        return '<mac: %s>' % self.to_string()

    @staticmethod
    def from_string(mac: str) -> 'MacAddress':
        """
        convert mac-address string into mac-address object

        :param mac: raw mac-address to be formated
        :return:    newly generated mac-address object
        """
        mac = mac.replace(':', '')
        if len(mac) != 12:
            raise TypeError('invalid mac-address: %r' % mac)
        return MacAddress.from_bytes(bytes.tohex(mac))

    def to_string(self) -> str:
        """
        convert mac-address byte-string into hex-string

        :return: hex-string formatted from saved byte-string
        """
        mac = self._addr.tohex()
        return ':'.join([mac[i:i+2] for i in range(0, len(mac), 2)])

class DHCPv4:

    def __init__(self,
        op:            int,
        htype:         int,
        hlen:          int,
        hops:          int,
        trans_id:      int,
        secs:          int,
        flags:         int,
        client_addr:   Ipv4,
        your_addr:     Ipv4,
        server_addr:   Ipv4,
        gateway_addr:  Ipv4,
        client_hwaddr: MacAddress,
        options:       List[option.Option],
    ):
        pass
