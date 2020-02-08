from .. import tftp

#** Classes **#

class ServerError(Exception):
    """custom exception used for tftp errors"""

    def __init__(self, code: tftp.ErrorCode, message: str):
        """
        :param code:    error code passed in exception
        :param message: message included in exception
        """
        self.code    = code
        self.message = message

    def __str__(self) -> str:
        return f'tftp-error[{self.code.name}]: {self.message}'

class BadOpCode(Exception):
    """error to be reaised on unexpected operation"""

    def __init__(self, op: tftp.OpCode):
        """
        :param op: opcode given that was unexpected
        """
        super().__init__(tftp.ErrorCode.IllegalOperation,
            'unexpected op=%s' % op.name)
