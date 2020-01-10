from . import abc

#** Classes **#

class Option(abc.ByteOperator):
    """base class for all option objects"""

    def __init__(self, opcode: int, raw: bytes):
        """
        :param opcode: single byte code to designate option type
        :param raw:    raw bytes containing data stored for option
        """
        if opcode < 0 or opcode > 255:
            raise TypeError('opcode must be a single byte')
        self.opcode = opcode
        self.raw = raw

# TODO: impelement byte-code conversion (and enable methods/vars to function as option)
