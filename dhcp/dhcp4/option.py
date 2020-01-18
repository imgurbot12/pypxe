import enum
import struct
from typing import List

from . import const
from .. import abc
from .. import net
from ..net import iana


#** Variables **#

#** Classes **#

class Param:
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

#TODO: implement from-bytes operations for existing options

class Option(abc.ByteOperator):
    """base class for all option objects"""
    opcode = 0

    def __init__(self, value: bytes):
        """
        :param value: raw-bytes value being passed as option
        """
        self.value = value

    def to_bytes(self) -> bytes:
        """convert option to raw byte-string"""
        return bytes((self.opcode, len(self.value))) + self.value


class OptMessageType(Option):
    """adds the DHCPv4 message type to a packet"""
    opcode = 53

    def __init__(self, type: const.MessageType):
        """
        :param type: DHCP message-type for this option
        """
        self.type = type

    def to_bytes(self) -> bytes:
        """convert option to raw byte-string"""
        return bytes((self.opcode, 1, self.type.value))

class OptParameterRequestList(Option):
    """list all paramters requested during discovery packet"""
    opcode = 55

    def __init__(self, params: List[Param]):
        """
        :param params: list of paramters being requested via dhcp discovery
        """
        self.params = params

    def to_bytes(self) -> bytes:
        """convert option to raw byte-string"""
        return bytes((self.opcode, len(self.params))) + \
            bytes(p.value if isinstance(p, Param) else p for p in self.params)

class OptMaxMessageSize(Option):
    """the Maximum DHCP Message Size option is described by RFC 2132"""
    opcode = 57

    def __init__(self, max_length: int):
        """
        :param max_length: max allowed DHCP message length
        """
        self.max_length = max_length

    def to_bytes(self) -> bytes:
        """convert option to raw byte-string"""
        return bytes((self.opcode, 2)) + struct.pack('>H', self.max_length)

class OptVendorClassIdentifier(Option):
    """includes vendor information"""
    opcode = 60

class OptClientIdentifier(Option):
    """extended client identification"""
    opcode = 61

    def __init__(self, hwtype: iana.HWType, mac: net.MacAddress):
        """
        :param hwtype: hardware-type of mac address being given
        :param mac:    mac-address of client
        """
        self.hwtype = hwtype
        self.mac    = mac

    def to_bytes(self) -> bytes:
        """convert option to raw byte-string"""
        raw = self.mac.to_bytes()
        return bytes((self.opcode, len(raw)+1, self.hwtype.value))+raw

class OptUserClassInfo(Option):
    """includes user class information"""
    opcode = 77

class OptClientSystemArchitecture(Option):
    """lists all types of architectures client currently supports"""
    opcode = 93

    def __init__(self, archs: iana.ArchList):
        """
        :param archs: list of supported architectures
        """
        self.archs = iana.ArchList(archs) if isinstance(archs, list) else archs

    def to_bytes(self) -> bytes:
        """convert option to raw byte-string"""
        raw = self.archs.to_bytes()
        return bytes((self.opcode, len(raw))) + raw

class OptClientNetworkDeviceInterface(Option):
    """declares PXE device interface version required for PXE (RFC 4578)"""
    opcode = 94

    def __init__(self, major: int, minor: int):
        """
        :param major: major version of network device interface
        :param minor: minor version of network device interface
        """
        self.major = major
        self.minor = minor

    def to_bytes(self) -> bytes:
        """convert option to raw byte-string"""
        return bytes((self.opcode, 3, 1, self.major, self.minor))

class OptXXIDClientIdentifier(Option):
    """uuid/guid client based identifier"""
    opcode = 97

    def to_bytes(self) -> bytes:
        """convert option to raw byte-string"""
        return bytes((self.opcode, len(self.value)+1, 0)) + self.value

class OptEtherBoot(Option):
    """extended PXE functionality via gPXE"""
    opcode = 175

# TODO: impelement byte-code conversion (and enable methods/vars to function as option)
# TODO: re-order options in order of opcodes if possible
