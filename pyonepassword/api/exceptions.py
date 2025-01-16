# needed so we can pass getattr() logic
# through to module for deprecation warnings
from .. import py_op_exceptions as __py_op_exceptions
from .._op_cli_version import OPCLIVersionSupportException
from .._svc_account import OPSvcAcctCommandNotSupportedException
from ..op_items._item_type_registry import OPUnknownItemTypeException
from ..op_items.fields_sections._new_fields import OPNewTOTPUriException
from ..op_items.fields_sections.item_section import (
    OPItemFieldCollisionException,
    OPSectionCollisionException
)
from ..op_items.item_types._item_base import (
    OPFieldNotFoundException,
    OPSectionNotFoundException
)
from ..op_items.item_types.login import OPNewLoginItemURLException
from ..op_objects import (
    OPInvalidGroupException,
    OPInvalidGroupListException,
    OPInvalidObjectException,
    OPInvalidUserException,
    OPInvalidUserListException,
    OPInvalidVaultException,
    OPInvalidVaultListException
)
from ..py_op_exceptions import (
    OPAuthenticationException,
    OPCLIPanicException,
    OPCmdFailedException,
    OPCmdMalformedSvcAcctTokenException,
    OPConfigNotFoundException,
    OPDesktopAppException,
    OPDocumentDeleteException,
    OPDocumentEditException,
    OPDocumentGetException,
    OPForgetException,
    OPGroupGetException,
    OPGroupListException,
    OPInvalidDocumentException,
    OPInvalidItemException,
    OPItemDeleteException,
    OPItemDeleteMultipleException,
    OPItemEditException,
    OPItemGetException,
    OPItemListException,
    OPItemShareException,
    OPNotFoundException,
    OPRevokedSvcAcctTokenException,
    OPSigninException,
    OPSignoutException,
    OPUnknownAccountException,
    OPUserEditException,
    OPUserGetException,
    OPUserListException,
    OPVaultGetException,
    OPVaultListException
)

# This causes these types to properly re-exported
# https://mypy.readthedocs.io/en/stable/config_file.html?highlight=export#confval-implicit_reexport
# anything that gets imported needs to be added to this list
__all__ = [
    "OPAuthenticationException",
    "OPCLIPanicException",
    "OPCLIVersionSupportException",
    "OPCmdFailedException",
    "OPCmdMalformedSvcAcctTokenException",
    "OPConfigNotFoundException",
    "OPDesktopAppException",
    "OPDocumentDeleteException",
    "OPDocumentEditException",
    "OPDocumentGetException",
    "OPFieldNotFoundException",
    "OPForgetException",
    "OPGroupGetException",
    "OPGroupListException",
    "OPInvalidDocumentException",
    "OPInvalidGroupException",
    "OPInvalidGroupListException",
    "OPInvalidItemException",
    "OPInvalidObjectException",
    "OPInvalidUserException",
    "OPInvalidUserListException",
    "OPInvalidVaultException",
    "OPInvalidVaultListException",
    "OPItemDeleteException",
    "OPItemDeleteMultipleException",
    "OPItemEditException",
    "OPItemFieldCollisionException",
    "OPItemGetException",
    "OPItemListException",
    "OPItemShareException",
    "OPNewLoginItemURLException",
    "OPNewTOTPUriException",
    "OPNotFoundException",
    "OPRevokedSvcAcctTokenException",
    "OPSectionCollisionException",
    "OPSectionNotFoundException",
    "OPSigninException",
    "OPSignoutException",
    "OPSvcAcctCommandNotSupportedException",
    "OPUnknownAccountException",
    "OPUnknownItemTypeException",
    "OPUserEditException",
    "OPUserGetException",
    "OPUserListException",
    "OPVaultGetException",
    "OPVaultListException"
]


def __getattr__(name: str):
    return getattr(__py_op_exceptions, name)

    # if name in _deprecated_exceptions:
    #     _deprecated_name = f"_{name}"
    #     alternate = _deprecated_exceptions[name]
    #     warnings.warn(
    #         f"Exception class {name} is deprecated. Use {alternate}", category=DeprecationWarning)
    #     return globals()[_deprecated_name]

    # raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
