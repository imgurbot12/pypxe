
#** Variables **#
__all__ = ['ByteOperator']

#** Classes **#

class ByteOperator:
    """base class used to describe objects moving to/from bytes"""

    @staticmethod
    def from_bytes(raw: bytes) -> 'ByteOperator':
        """base class method declaration"""
        raise NotImplementedError('must be overwritten!')

    def to_bytes(self) -> bytes:
        """base class method declaration"""
        raise NotImplementedError('must be overwritten!')
