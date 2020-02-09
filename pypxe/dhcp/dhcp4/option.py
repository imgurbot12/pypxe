"""
implementation of many of the primary DHCP options included in DHCPv4 packets
"""
import enum
import struct
from typing import Tuple, List, Any, Optional

from . import const
from .. import abc, iana, net

#** Variables **#
__all__ = [
    'Param',

    'from_bytes',

    'Options',
    'Option',
    'OptSubnetMask',
    'OptRouter',
    'OptDomainNameServer',
    'OptRequestedAddress',
    'OptIPLeaseTime',
    'OptMessageType',
    'OptServerIdentifier',
    'OptParameterRequestList',
    'OptMaxMessageSize',
    'OptClassIdentifier',
    'OptTFTPServerName',
    'OptTFTPServerIP',
    'OptBootFileName',
    'OptUserClassInfo',
    'OptClientSystemArchitecture',
    'OptClientNetworkInterface',
    'OptXXIDClientIdentifier',
    'OptEtherBoot',
]

class Param(enum.Enum):
    """DHCP Request Paramter List Paramters"""
    OptionPad                                  = 0
    SubnetMask                                 = 1
    TimeOffset                                 = 2
    Router                                     = 3
    TimeServer                                 = 4
    NameServer                                 = 5
    DomainNameServer                           = 6
    LogServer                                  = 7
    QuoteServer                                = 8
    LPRServer                                  = 9
    ImpressServer                              = 10
    ResourceLocationServer                     = 11
    HostName                                   = 12
    BootFileSize                               = 13
    MeritDumpFile                              = 14
    DomainName                                 = 15
    SwapServer                                 = 16
    RootPath                                   = 17
    ExtensionsPath                             = 18
    IPForwarding                               = 19
    NonLocalSourceRouting                      = 20
    PolicyFilter                               = 21
    MaximumDatagramAssemblySize                = 22
    DefaultIPTTL                               = 23
    PathMTUAgingTimeout                        = 24
    PathMTUPlateauTable                        = 25
    InterfaceMTU                               = 26
    AllSubnetsAreLocal                         = 27
    BroadcastAddress                           = 28
    PerformMaskDiscovery                       = 29
    MaskSupplier                               = 30
    PerformRouterDiscovery                     = 31
    RouterSolicitationAddress                  = 32
    StaticRoutingTable                         = 33
    TrailerEncapsulation                       = 34
    ArpCacheTimeout                            = 35
    EthernetEncapsulation                      = 36
    DefaulTCPTTL                               = 37
    TCPKeepaliveInterval                       = 38
    TCPKeepaliveGarbage                        = 39
    NetworkInformationServiceDomain            = 40
    NetworkInformationServers                  = 41
    NTPServers                                 = 42
    VendorSpecificInformation                  = 43
    NetBIOSOverTCPIPNameServer                 = 44
    NetBIOSOverTCPIPDatagramDistributionServer = 45
    NetBIOSOverTCPIPNodeType                   = 46
    NetBIOSOverTCPIPScope                      = 47
    XWindowSystemFontServer                    = 48
    XWindowSystemDisplayManger                 = 49
    RequestedIPAddress                         = 50
    IPAddressLeaseTime                         = 51
    OptionOverload                             = 52
    DHCPMessageType                            = 53
    ServerIdentifier                           = 54
    ParameterRequestList                       = 55
    Message                                    = 56
    MaximumDHCPMessageSize                     = 57
    RenewTimeValue                             = 58
    RebindingTimeValue                         = 59
    ClassIdentifier                            = 60
    ClientIdentifier                           = 61
    NetWareIPDomainName                        = 62
    NetWareIPInformation                       = 63
    NetworkInformationServicePlusDomain        = 64
    NetworkInformationServicePlusServers       = 65
    TFTPServerName                             = 66
    BootfileName                               = 67
    MobileIPHomeAgent                          = 68
    SimpleMailTransportProtocolServer          = 69
    PostOfficeProtocolServer                   = 70
    NetworkNewsTransportProtocolServer         = 71
    DefaultWorldWideWebServer                  = 72
    DefaultFingerServer                        = 73
    DefaultInternetRelayChatServer             = 74
    StreetTalkServer                           = 75
    StreetTalkDirectoryAssistanceServer        = 76
    UserClassInformation                       = 77
    SLPDirectoryAgent                          = 78
    SLPServiceScope                            = 79
    RapidCommit                                = 80
    FQDN                                       = 81
    RelayAgentInformation                      = 82
    InternetStorageNameService                 = 83
    # Option 84 returned in RFC 3679
    NDSServers                       = 85
    NDSTreeName                      = 86
    NDSContext                       = 87
    BCMCSControllerDomainNameList    = 88
    BCMCSControllerIPv4AddressList   = 89
    Authentication                   = 90
    ClientLastTransactionTime        = 91
    AssociatedIP                     = 92
    ClientSystemArchitectureType     = 93
    ClientNetworkInterfaceIdentifier = 94
    LDAP                             = 95
    # Option 96 returned in RFC 3679
    ClientMachineIdentifier     = 97
    OpenGroupUserAuthentication = 98
    GeoConfCivic                = 99
    IEEE10031TZString           = 100
    ReferenceToTZDatabase       = 101
    # Options 102-111 returned in RFC 3679
    NetInfoParentServerAddress = 112
    NetInfoParentServerTag     = 113
    URL                        = 114
    # Option 115 returned in RFC 3679
    AutoConfigure                   = 116
    NameServiceSearch               = 117
    SubnetSelection                 = 118
    DNSDomainSearchList             = 119
    SIPServers                      = 120
    ClasslessStaticRoute            = 121
    CCC                             = 122
    GeoConf                         = 123
    VendorIdentifyingVendorClass    = 124
    VendorIdentifyingVendorSpecific = 125
    # Options 126-127 returned in RFC 3679
    TFTPServerIPAddress                   = 128
    CallServerIPAddress                   = 129
    DiscriminationString                  = 130
    RemoteStatisticsServerIPAddress       = 131
    O_8021PVLANID                         = 132
    O_8021QL2Priority                     = 133
    DiffservCodePoint                     = 134
    HTTPProxyForPhoneSpecificApplications = 135
    PANAAuthenticationAgent               = 136
    LoSTServer                            = 137
    CAPWAPAccessControllerAddresses       = 138
    OPTIONIPv4AddressMoS                  = 139
    OPTIONIPv4FQDNMoS                     = 140
    SIPUAConfigurationServiceDomains      = 141
    OPTIONIPv4AddressANDSF                = 142
    OPTIONIPv6AddressANDSF                = 143
    # Options 144-149 returned in RFC 3679
    TFTPServerAddress = 150
    StatusCode        = 151
    BaseTime          = 152
    StartTimeOfState  = 153
    QueryStartTime    = 154
    QueryEndTime      = 155
    DHCPState         = 156
    DataSource        = 157
    # Options 158-174 returned in RFC 3679
    Etherboot                        = 175
    IPTelephone                      = 176
    EtherbootPacketCableAndCableHome = 177
    # Options 178-207 returned in RFC 3679
    PXELinuxMagicString  = 208
    PXELinuxConfigFile   = 209
    PXELinuxPathPrefix   = 210
    PXELinuxRebootTime   = 211
    OPTION6RD            = 212
    OPTIONv4AccessDomain = 213
    # Options 214-219 returned in RFC 3679
    SubnetAllocation        = 220
    VirtualSubnetAllocation = 221
    # Options 222-223 returned in RFC 3679
    # Options 224-254 are reserved for private use
    End = 255

# hidden cache for all found option objects
_options: List['Option'] = []

#** Functions **#

def _stringify(item: Any, prefix: str = '') -> str:
    """
    stringify value to print reguardless of inbound type

    :param item:   item being converted into string value
    :param prefix: append prefix to certain string formations
    :return:       strinified variable retrieved from option
    """
    if hasattr(item, 'to_string'):
        return item.to_string()
    elif isinstance(item, bytes):
        try:
            return item.decode()
        except UnicodeDecodeError:
            return item.hex()
    elif isinstance(item, (list, Options)):
        return prefix+'\n'+'\n'.join(prefix+' - %s'%_stringify(i) for i in item)
    elif isinstance(item, enum.Flag):
        return item.name
    else:
        return str(item)

def _from_bytes(raw: bytes) -> Tuple['Option', int]:
    """
    convert raw bytes into appropriate option object

    :param raw: raw-bytes being converted into option object
    :return:    generated option object w/ loaded values and num of bytes read
    """
    # retrieve list of options from globals
    global _options
    if not _options:
        classes  = (i for n,i in globals().items()
            if n.startswith('Opt') and n not in ('Optional', 'Options'))
        _options = {
            item.opcode.value:item
            for item in classes if issubclass(item, Option)
        }
    # iterate options until opcode matches
    optlen = int(raw[1]) + 2
    if raw[0] in _options:
        opt = _options[raw[0]]
        return opt.from_bytes(raw[2:optlen]), optlen
    # else if no option was found
    return Option.from_bytes(raw[:optlen]), optlen

def from_bytes(raw: bytes) -> List['Option']:
    """
    convert raw bytes into list of option objects

    :param raw: raw-bytes being converted into option object
    :return:    list of options parsed from bytes
    """
    options = []
    while True:
        opt, mod = _from_bytes(raw)
        raw      = raw[mod:]
        options.append(opt)
        if raw[0] == 255:
            break
    return options

#** Classes **#

class Options:
    """dict/list hybrid allowing for quick-lookups of options"""

    def __init__(self, options: List['Option']):
        """
        :param options: list of options to add to self
        """
        self._dict   = {opt.opcode.value:n for n, opt in enumerate(options, 0)}
        self._list   = options

    def __iter__(self) -> List['Option']:
        return iter(self._list)

    def __contains__(self, k: Param) -> bool:
        return k.value in self._dict

    def __getitem__(self, k: Any) -> 'Option':
        idx = self._dict[k.value] if isinstance(k, Param) else k
        return self._list[idx]

    def get(self, k: Param, d: Any = None) -> Optional['Option']:
        """
        retrieve an item from the list if the paramter exists

        :param k: key being used to retrieve value
        :param d: default to return if none
        :return:  option object or default value if not found
        """
        return self[k] if k in self else d

    def get_ip(self, k: Param) -> Optional[net.Ipv4]:
        """
        retrieve the ip-address from the specified option-type if exists

        :param k: key being used to retrieve value
        :return:  ipv4 or none if not found
        """
        return self[k].ip if k in self else None

    def append(self, option: 'Option'):
        """
        append an item to the options list

        :param option: option to add to array
        """
        self._dict[option.opcode.value] = len(self._list)
        self._list.append(option)

    def extend(self, options: List['Option']):
        """
        append multiple items to the options list

        :param options: list of options to append to list
        """
        idx = len(self._list)
        self._dict.update({
            opt.opcode.value:idx+n
            for n, opt in enumerate(options, 0)
        })
        self._list.extend(options)

class Option(abc.ByteOperator):
    """base class for all option objects, allows conversion to/from bytes"""
    opcode = Param.OptionPad

    def __init__(self, value: bytes, opcode: Param = Param.OptionPad):
        """
        :param value:  raw-bytes value being passed as option
        :param opcode: opcode for option object
        """
        self.value  = value
        self.opcode = opcode

    def __str__(self) -> str:
        return '<Option: %s>' % (self.opcode.name)

    def summary(self, prefix: str = '') -> str:
        """
        retrieve complete summary of option object

        :param prefix: append prefix to start of every line
        :return:       multi-line summary of option object and all vars
        """
        return '%sOption: %s<%s>\n%s' % (
            prefix,
            self.opcode.name,
            self.opcode.value,
            '\n'.join(prefix+' - %s: %s' % (
                k,_stringify(v, prefix))
                for k,v in vars(self).items()
                if k != 'opcode'
            )
        )

    def to_bytes(self) -> bytes:
        """convert option to raw byte-string"""
        return bytes((self.opcode.value, len(self.value))) + self.value

    @classmethod
    def from_bytes(cls, raw: bytes) -> 'Option':
        """convert raw-bytes into option object"""
        return cls(
            value=raw[2:],
            opcode=abc.find_enum(Param, raw[0])
        )

class _IPv4Option(Option):
    """base-class implementation for single ip-paramter option classes"""

    def __init__(self, ip: net.Ipv4):
        """
        :param ip: designated ip-address
        """
        self.ip = ip

    def to_bytes(self) -> bytes:
        """convert option to raw byte-string"""
        return bytes((self.opcode.value, 4)) + self.ip.to_bytes()

    @classmethod
    def from_bytes(cls, raw: bytes) -> '_IPv4Option':
        """convert raw-bytes into option object"""
        return cls(net.Ipv4.from_bytes(raw))

class OptSubnetMask(_IPv4Option):
    """sets subnet mask to be used when on network"""
    opcode = Param.SubnetMask

class OptRouter(_IPv4Option):
    """sets router ip-address to allow internet connectivity"""
    opcode = Param.Router

class OptDomainNameServer(_IPv4Option):
    """sets domain-name server used to make DNS requests"""
    opcode = Param.DomainNameServer

class OptRequestedAddress(_IPv4Option):
    """tells dhcp server what client wants their ip-address to be"""
    opcode = Param.RequestedIPAddress

class OptIPLeaseTime(Option):
    """sets maxiumum lease-time for given settings from dhcp-server"""
    opcode = Param.IPAddressLeaseTime

    def __init__(self,
        secs: int = 0, mins: int = 0, hours: int = 0, days: int = 0):
        """
        :param secs:  number of seconds in lease
        :param mins:  number of minutes in lease
        :param hours: number of hours in lease
        :param days:  number of days in lease
        """
        self.lease = secs + (mins * 60) + (hours * 3600) + (days * 86400)

    def to_bytes(self) -> bytes:
        """convert option to raw byte-string"""
        return bytes((self.opcode.value, 4)) + struct.pack('>I', self.lease)

    @staticmethod
    def from_bytes(raw: bytes) -> 'OptIPLeaseTime':
        """convert raw-bytes into option object"""
        return OptIPLeaseTime(secs=struct.unpack('>I', raw)[0])

class OptMessageType(Option):
    """adds the DHCPv4 message type to a packet"""
    opcode = Param.DHCPMessageType

    def __init__(self, type: const.MessageType):
        """
        :param type: DHCP message-type for this option
        """
        self.type = type

    def __eq__(self, other: const.MessageType) -> bool:
        return self.type == other

    def to_bytes(self) -> bytes:
        """convert option to raw byte-string"""
        return bytes((self.opcode.value, 1, self.type.value))

    @staticmethod
    def from_bytes(raw: bytes) -> 'OptMessageType':
        """convert raw-bytes into option object"""
        return OptMessageType(abc.find_enum(const.MessageType, raw[0]))

class OptServerIdentifier(_IPv4Option):
    """declares which server is sending this response packet"""
    opcode = Param.ServerIdentifier

class OptParameterRequestList(Option):
    """list all paramters requested during discovery packet"""
    opcode = Param.ParameterRequestList

    def __init__(self, params: List[Param]):
        """
        :param params: list of paramters being requested via dhcp discovery
        """
        self.params = params

    def to_bytes(self) -> bytes:
        """convert option to raw byte-string"""
        return bytes((self.opcode.value, len(self.params))) + \
            bytes(p.value if isinstance(p, Param) else p for p in self.params)

    @staticmethod
    def from_bytes(raw: bytes) -> 'OptParameterRequestList':
        """convert raw-bytes into option object"""
        return OptParameterRequestList([
            abc.find_enum(Param, byte, byte)
            for byte in raw
        ])

class OptMaxMessageSize(Option):
    """the Maximum DHCP Message Size option is described by RFC 2132"""
    opcode = Param.MaximumDHCPMessageSize

    def __init__(self, max_length: int):
        """
        :param max_length: max allowed DHCP message length
        """
        self.max_length = max_length

    def to_bytes(self) -> bytes:
        """convert option to raw byte-string"""
        return bytes((self.opcode.value, 2)) + struct.pack('>H',self.max_length)

    @staticmethod
    def from_bytes(raw: bytes) -> 'OptMessageType':
        """convert raw-bytes into option object"""
        return OptMaxMessageSize(struct.unpack('>H', raw)[0])

class OptClassIdentifier(Option):
    """includes vendor information"""
    opcode = Param.ClassIdentifier

class OptTFTPServerName(Option):
    """set TFTP server-name for PXE boot"""
    opcode = Param.TFTPServerName

class OptTFTPServerIP(_IPv4Option):
    """sets TFTP server ip-address for PXE boot"""
    opcode = Param.TFTPServerIPAddress

class OptBootFileName(Option):
    """set boot-file for PXE boot"""
    opcode = Param.BootfileName

class OptUserClassInfo(Option):
    """includes user class information"""
    opcode = Param.UserClassInformation

class OptClientSystemArchitecture(Option):
    """lists all types of architectures client currently supports"""
    opcode = Param.ClientSystemArchitectureType

    def __init__(self, archs: iana.ArchList):
        """
        :param archs: list of supported architectures
        """
        self.archs = iana.ArchList(archs) if isinstance(archs, list) else archs

    def to_bytes(self) -> bytes:
        """convert option to raw byte-string"""
        raw = self.archs.to_bytes()
        return bytes((self.opcode.value, len(raw))) + raw

    @staticmethod
    def from_bytes(raw: bytes) -> 'OptClientSystemArchitecture':
        """convert raw-bytes into option object"""
        return OptClientSystemArchitecture(iana.ArchList.from_bytes(raw))

class OptClientNetworkInterface(Option):
    """declares PXE device interface version required for PXE (RFC 4578)"""
    opcode = Param.ClientNetworkInterfaceIdentifier

    def __init__(self, major: int, minor: int):
        """
        :param major: major version of network device interface
        :param minor: minor version of network device interface
        """
        self.major = major
        self.minor = minor

    def to_bytes(self) -> bytes:
        """convert option to raw byte-string"""
        return bytes((self.opcode.value, 3, 1, self.major, self.minor))

    @staticmethod
    def from_bytes(raw: bytes) -> 'OptClientNetworkInterface':
        """convert raw-bytes into option object"""
        return OptClientNetworkInterface(raw[1], raw[2])

class OptXXIDClientIdentifier(Option):
    """uuid/guid client based identifier"""
    opcode = Param.ClientMachineIdentifier

    def to_bytes(self) -> bytes:
        """convert option to raw byte-string"""
        return bytes((self.opcode.value, len(self.value)+1, 0)) + self.value

    @staticmethod
    def from_bytes(raw: bytes) -> 'OptXXIDClientIdentifier':
        """convert raw-bytes into option object"""
        return OptXXIDClientIdentifier(raw[1:])

class OptEtherBoot(Option):
    """extended PXE functionality via gPXE"""
    opcode = Param.Etherboot

# TODO: impelement byte-code conversion (and enable methods/vars to function as option)
# TODO: re-order options in order of opcodes if possible
