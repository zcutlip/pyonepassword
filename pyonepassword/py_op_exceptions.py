"""
Various exception classes raised by ponepassword API
TODO: Move other exception classes here
"""
from abc import ABCMeta, abstractmethod


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

    def __init__(self, stderr_out, returncode):
        super().__init__(stderr_out, returncode)


class OPSignoutException(OPCmdFailedException):  # pragma: no coverage
    MSG = "1Password signout failed."

    def __init__(self, stderr_out, returncode):
        super().__init__(stderr_out, returncode)


class OPForgetException(OPCmdFailedException):  # pragma: no coverage
    MSG = "1Password forget failed."

    def __init__(self, stderr_out, returncode):
        super().__init__(stderr_out, returncode)


class OPItemGetException(OPCmdFailedException):
    MSG = "1Password 'get item' failed."

    def __init__(self, stderr_out, returncode):
        super().__init__(stderr_out, returncode)


class OPItemListException(OPCmdFailedException):
    MSG = "1Password 'item list' failed."

    def __init__(self, stderr_out, returncode):
        super().__init__(stderr_out, returncode)


class OPItemDeleteException(OPCmdFailedException):
    MSG = "1Password 'item delete' failed."

    def __init__(self, stderr_out, returncode):
        super().__init__(stderr_out, returncode)


class OPDocumentGetException(OPCmdFailedException):
    MSG = "1Password 'document get' failed."

    def __init__(self, stderr_out, returncode):
        super().__init__(stderr_out, returncode)


class OPDocumentDeleteException(OPCmdFailedException):
    MSG = "1Password 'document delete' failed."

    def __init__(self, stderr_out, returncode):
        super().__init__(stderr_out, returncode)


class OPUserGetException(OPCmdFailedException):
    MSG = "1Password 'get user' failed."

    def __init__(self, stderr_out, returncode):
        super().__init__(stderr_out, returncode)


class OPUserListException(OPCmdFailedException):
    MSG = "1Password 'user list' failed."

    def __init__(self, stderr_out, returncode):
        super().__init__(stderr_out, returncode)


class OPVaultGetException(OPCmdFailedException):
    MSG = "1Password 'get vault' failed."

    def __init__(self, stderr_out, returncode):
        super().__init__(stderr_out, returncode)


class OPVaultListException(OPCmdFailedException):
    MSG = "1Password 'vault list' failed."

    def __init__(self, stderr_out, returncode):
        super().__init__(stderr_out, returncode)


class OPGroupGetException(OPCmdFailedException):
    MSG = "1Password 'get group' failed."

    def __init__(self, stderr_out, returncode):
        super().__init__(stderr_out, returncode)


class OPGroupListException(OPCmdFailedException):
    MSG = "1Password 'group list' failed."

    def __init__(self, stderr_out, returncode):
        super().__init__(stderr_out, returncode)


class OPItemCreateException(OPCmdFailedException):  # pragma: no coverage
    MSG = "1Password 'item create' failed."

    def __init__(self, stderr_out, returncode):
        super().__init__(stderr_out, returncode)


class OPInvalidItemException(_OPAbstractException):
    def __init__(self, msg):
        super().__init__(msg)


class OPNotSignedInException(_OPAbstractException):
    def __init__(self, msg):
        super().__init__(msg)


class OPInvalidDocumentException(OPInvalidItemException):
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


class OPInvalidFieldException(_OPAbstractException):
    def __init__(self, msg):
        super().__init__(msg)


class OPUnknownAccountException(_OPAbstractException):
    def __init__(self, msg):
        super().__init__(msg)
