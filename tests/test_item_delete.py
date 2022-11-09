# __future__.annotations, and typing.TYPE_CHECKING
# enable anything imported for type hinting to disappear at run time
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

# make imports for type-hinting disappear at run-time to avoid
# circular imports.
# this also reduced exercising tested code simply by importing
if TYPE_CHECKING:
    from pyonepassword import OP

    from .fixtures.expected_login import ExpectedLoginItemData


# ensure HOME env variable is set, and there's a valid op config present
pytestmark = pytest.mark.usefixtures("valid_op_cli_config_homedir")


def test_item_delete_01(signed_in_op: OP, expected_login_item_data: ExpectedLoginItemData):
    login_name = "Delete Me Unique"
    vault = "Test Data"
    expected = expected_login_item_data.data_for_login(login_name)
    expected_item_id = expected.unique_id
    result = signed_in_op.item_delete(login_name, vault=vault)
    assert result == expected_item_id
