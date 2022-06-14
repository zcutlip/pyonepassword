from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pyonepassword import OP

from pyonepassword.api.exceptions import OPItemListException

# ensure HOME env variable is set, and there's a valid op config present
pytestmark = pytest.mark.usefixtures("valid_op_cli_config_homedir")


def test_item_list_invalid_vault_01(signed_in_op: OP):
    vault = "Invalid Vault"
    with pytest.raises(OPItemListException):
        signed_in_op.item_list(include_archive=True, vault=vault)
