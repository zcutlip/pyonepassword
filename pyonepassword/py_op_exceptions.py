"""
Various exception classes raised by ponepassword API
TODO: Move other exception classes here
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .op_items._item_list import OPItemList


class OPBaseException(Exception):

    def __init__(self, msg):
        super().__init__(msg)


class OPCmdFailedException(OPBaseException):
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
    def from_opexception(cls, ope: OPCmdFailedException):
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


class OPItemDeleteMultipleException(OPItemDeleteException):
    """
    Exception class for OP.item_delete_multiple() failures

    Contains list of deleted items, if any, before the failure occured
    """
    MSG = "1Password 'item delete' for multiple objects failed."

    def __init__(self, deleted_items: OPItemList, stderr_out, returncode):
        """
        Parameters
        ----------
        deleted_items : OPItemList
            List of items that were deleted before the failure occured
        stderr_out : str
            Error output from the 'op' command
        returncode : int
            Exit status of the 'op' op command
        """
        self.deleted_items = deleted_items
        super().__init__(stderr_out, returncode)

    @classmethod
    # type: ignore[override]
    def from_opexception(cls, ope: OPCmdFailedException, deleted_items: OPItemList):
        return cls(deleted_items, ope.err_output, ope.returncode)


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


class OPInvalidItemException(OPBaseException):
    def __init__(self, msg):
        super().__init__(msg)


class OPNotSignedInException(OPBaseException):
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


class OPInvalidFieldException(OPBaseException):
    def __init__(self, msg):
        super().__init__(msg)


class OPUnknownAccountException(OPBaseException):
    def __init__(self, msg):
        super().__init__(msg)
