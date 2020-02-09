"""
complete TFTP server instance for easy control of reading/writing files
"""
import io
import os
from .. import tftp
from typing import Optional

#** Variables **#
__all__ = [
    'ServerError',
    'BadOpCode',
    'FileFinder',

    'RequestHandler',
    'CallbackHandler',
    'TFTPServer',
]

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
        return f'{self.code.name}: {self.message}'

class BadOpCode(ServerError):
    """error to be reaised on unexpected operation"""

    def __init__(self, op: tftp.OpCode):
        """
        :param op: opcode given that was unexpected
        """
        super().__init__(tftp.ErrorCode.IllegalOperation,
            'unexpected op=%s' % op.name)

class FileFinder:
    """utility to find and return file objects from a given starting filepath"""

    def __init__(self, basedir: str):
        """
        :param basdir: base directory to pull all other files from
        """
        if not os.path.exists(basedir):
            raise Exception('no such path: %s' % basedir)
        self.basedir = os.path.realpath(basedir)

    def find(self, path: str, mode: str = 'rb') -> Optional[io.IOBase]:
        """
        retrieve file object if path exists else return none

        :param path: path requested from directory
        :param mode: mode to open file in if found
        :return:     file object or none if not found
        """
        fp = os.path.join(self.basedir, path)
        if mode.startswith('w') or mode.startswith('a') or os.path.exists(fp):
            return open(fp, mode)

#** Imports **#
from .server import *
