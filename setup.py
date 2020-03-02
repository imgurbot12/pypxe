from setuptools import setup

#** Variables **#

DESCRIPTION = """a complete PXE library written for python3
contains libraries for:
    DHCPv4/DHCPv6
        - packet creation
        - packet parsing
        - basic DHCP server implementation
    TFTP
        - packet creation
        - packet parsing
        - basic TFTP server implementation
    Debugging:
        - form hexdumps of any raw-bytes
""".strip()

#** Start **#

setup(
    name='pypxe',
    version='1.0.0',
    url='https://github.com/imgurbot12/pypxe',
    license=None,
    description=DESCRIPTION.split('\n')[0],
    long_description=DESCRIPTION,
    author='Andrew Scott',
    author_email='imgurbot12@gmail.com',
    packages=[
        'pypxe',
        'pypxe.dhcp',
        'pypxe.dhcp.dhcp4',
        'pypxe.dhcp.dhcp6',

        'pypxe.tftp',
        'pypxe.tftp.server',
    ],
)
