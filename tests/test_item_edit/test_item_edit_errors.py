from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from pyonepassword.py_op_exceptions import OPInsecureOperationException

if TYPE_CHECKING:
    from pyonepassword import OP

# ensure HOME env variable is set, and there's a valid op config present
pytestmark = pytest.mark.usefixtures("valid_op_cli_config_homedir")


@pytest.mark.usefixtures("setup_stateful_item_edit")
def test_item_edit_set_password_no_insecure_acknowledge_010(signed_in_op: OP):
    """
    Test: OP.item_edit_set_password() raises OPInsecureOperationException appropriately
        - Attempt to call item_edit_set_password() without passing insecure_operation = True
    Verify:
        - OPInsecureOperationException is raised
    """

    item_name = "Example Login Item 00"
    new_password = "new password"
    vault = "Test Data 2"

    # item_edit_set_password() is inherently insecure, so
    # requires insecure_operation=True
    # This is expected to fail
    with pytest.raises(OPInsecureOperationException):
        signed_in_op.item_edit_set_password(item_name,
                                            new_password,
                                            vault=vault)
