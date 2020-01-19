from . import abc
from typing import List

#** Variables **#
__all__ = [
    'Ipv4',
    'MacAddress'
]

#** Classes **#

class Ipv4(abc.ByteObject):
    """basic ipv4 type used to compare/store ip addresses"""

    def __init__(self, a: int, b: int, c: int, d: int):
        """
        :param a: first octet of Ipv4
        :param b: second octet of Ipv4
        :param c: third octect of Ipv4
        :param d: fourth octet of Ipv4
        """
        super(Ipv4, self).__init__(4, [a, b, c, d])

    def __str__(self) -> str:
        return '<ipv4: %s>' % self.to_string()

    @staticmethod
    def from_bytes(raw: bytes) -> 'Ipv4':
        """
        convert raw byte-string into address object

        :param raw: byte-string being turned into Ipv4
        :return:    newly generated address object
        """
        return Ipv4(*[b for b in raw])

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

class MacAddress(abc.ByteObject):
    """basic mac-address type used to compare/store mac addresses"""

    def __init__(self, bytes: bytes):
        """
        :param bytes: list of bytes used to generate mac-address
        """
        super(MacAddress, self).__init__(len(bytes), bytes)

    def __str__(self) -> str:
        return '<mac: %s>' % self.to_string()

    @staticmethod
    def from_bytes(raw: bytes) -> 'MacAddress':
        """
        convert raw byte-string into address object

        :param raw: byte-string being turned into MacAddress
        :return:    newly generated address object
        """
        return MacAddress(raw)

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
        return MacAddress.from_bytes(bytes.fromhex(mac))

    def to_string(self) -> str:
        """
        convert mac-address byte-string into hex-string

        :return: hex-string formatted from saved byte-string
        """
        mac = self._addr.hex()
        return ':'.join([mac[i:i+2] for i in range(0, len(mac), 2)])
