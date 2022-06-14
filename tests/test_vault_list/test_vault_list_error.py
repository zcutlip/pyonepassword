from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

# make imports for type-hinting disappear at run-time to avoid
# circular imports.
# this also reduced exercising tested code simply by importing
if TYPE_CHECKING:
    from pyonepassword import OP

from pyonepassword.api.descriptor_types import OPVaultDescriptorList
from pyonepassword.api.exceptions import (
    OPInvalidVaultListException,
    OPVaultListException
)

pytestmark = pytest.mark.usefixtures("valid_op_cli_config_homedir")


def test_vault_list_malformed_json_01(invalid_data):
    malformed_json = invalid_data.data_for_name("malformed-vault-list-json")

    with pytest.raises(OPInvalidVaultListException):
        OPVaultDescriptorList(malformed_json)


def test_vault_list_invalid_user_01(signed_in_op: OP):
    user_identifier = "No Such User"
    with pytest.raises(OPVaultListException):
        signed_in_op.vault_list(user_name_or_id=user_identifier)
