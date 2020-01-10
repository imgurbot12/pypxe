from . import abc
from . import option
from typing import List

#** Variables **#
__all__ = [
    'DHCPv4',
]

#** Classes **#

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
