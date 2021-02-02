"""
Various exception classes raised by ponepassword API
TODO: Move other exception classes here
"""
from abc import ABCMeta, abstractmethod

from ._py_op_deprecation import deprecated


class _OPAbstractException(Exception, metaclass=ABCMeta):

    @abstractmethod
    def __init__(self, msg):
        super().__init__(msg)


class OPCmdFailedException(_OPAbstractException):
    """
    Generic Exception class for when an `op` command fails.

    Description:
    Raised from subprocess call-site when `op` executable returns non-zero

    Caller should handle this exception and raise a more descriptive exception reflecting
    the action that failed:

    Example:
    try:
        self._run(argv, capture_stdout=True, input_string=password)
    except OPCmdFailedException as ocfe:
        raise OPSigninException.from_opexception(ocfe) from ocfe
    """
    MSG = "'op' command failed"

    def __init__(self, stderr_out, returncode):
        super().__init__(self.MSG)
        self.err_output = stderr_out
        self.returncode = returncode

    @classmethod
    def from_opexception(cls, ope):
        return cls(ope.err_output, ope.returncode)


class OPSigninException(OPCmdFailedException):
    MSG = "1Password sign-in failed."


class OPSignoutException(OPCmdFailedException):
    MSG = "1Password signout failed."


class OPForgetException(OPCmdFailedException):
    MSG = "1Password forget failed."

# Keep this exception class around for a bit
# so any code handling this exception instead of OPGetItemException
# can still work


@deprecated("handle OPGetItemException instead")
class OPLookupException(OPCmdFailedException):
    MSG = "1Password lookup failed."


# For now have this class extend OPLookupException
# so code can handle that exception or this one
# TODO: remove OPLookupException, have this class extend
# _OPAbstractException
class OPGetItemException(OPCmdFailedException):
    MSG = "1Password 'get item' failed."


class OPGetDocumentException(OPCmdFailedException):
    MSG = "1Password 'get document' failed."


class OPGetUserException(OPCmdFailedException):
    MSG = "1Password 'get user' failed."


class OPGetVaultException(OPCmdFailedException):
    MSG = "1Password 'get vault' failed."


class OPGetGroupException(OPCmdFailedException):
    MSG = "1Password 'get group' failed."


class OPListEventsException(OPCmdFailedException):
    MSG = "1Passworm 'list events' failed."


class OPInvalidDocumentException(_OPAbstractException):

    def __init__(self, msg):
        super().__init__(msg)


class OPNotFoundException(Exception):
    MSG = "1Password cli command not found at path: %s"

    def __init__(self, op_path, errno):
        msg = self.MSG % op_path
        self.errno = errno
        super().__init__(msg)


class OPConfigNotFoundException(Exception):
    pass
