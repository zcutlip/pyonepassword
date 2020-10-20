"""
Various exception classes raised by ponepassword API
TODO: Move other exception classes here
"""
from abc import ABCMeta, abstractmethod

from ._py_op_deprecation import deprecated


class _OPAbstractException(Exception, metaclass=ABCMeta):

    @abstractmethod
    def __init__(self, stderr_out, returncode, msg):
        super().__init__(msg)
        self.err_output = stderr_out
        self.returncode = returncode


class OPSigninException(_OPAbstractException):
    MSG = "1Password sign-in failed."

    def __init__(self, stderr_out, returncode):
        super().__init__(stderr_out, returncode, self.MSG)


# Keep this exception class around for a bit
# so any code handling this exception instead of OPGetItemException
# can still work
@deprecated("handle OPGetItemException instead")
class OPLookupException(_OPAbstractException):
    MSG = "1Password lookup failed."

    def __init__(self, stderr_out, returncode, msg=None):
        if msg is None:
            msg = self.MSG
        super().__init__(stderr_out, returncode, msg)


# For now have this class extend OPLookupException
# so code can handle that exception or this one
# TODO: remove OPLookupException, have this class extend
# _OPAbstractException
class OPGetItemException(OPLookupException):
    MSG = "1Password 'get item' failed."

    def __init__(self, stderr_out, returncode):
        super().__init__(stderr_out, returncode, self.MSG)


class OPGetDocumentException(_OPAbstractException):
    MSG = "1Password 'get document' failed."

    def __init__(self, stderr_out, returncode):
        super().__init__(stderr_out, returncode, self.MSG)


class OPInvalidDocumentException(OPGetDocumentException):

    def __init__(self, msg):
        msg = "{}: {}".format(self.MSG, msg)
        super().__init__("", 0, msg)


class OPNotFoundException(Exception):
    MSG = "1Password cli command not found at path: %s"

    def __init__(self, op_path, errno):
        msg = self.MSG % op_path
        self.errno = errno
        super().__init__(msg)


class OPConfigNotFoundException(Exception):
    pass
