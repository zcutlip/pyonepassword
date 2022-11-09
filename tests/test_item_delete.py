# __future__.annotations, and typing.TYPE_CHECKING
# enable anything imported for type hinting to disappear at run time
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from pyonepassword.api.exceptions import OPItemDeleteException

# make imports for type-hinting disappear at run-time to avoid
# circular imports.
# this also reduced exercising tested code simply by importing
if TYPE_CHECKING:
    from pyonepassword import OP

    from .fixtures.expected_login import ExpectedLoginItemData


# ensure HOME env variable is set, and there's a valid op config present
pytestmark = pytest.mark.usefixtures("valid_op_cli_config_homedir")


def test_item_delete_01(signed_in_op: OP, expected_login_item_data: ExpectedLoginItemData):
    """
    Test deleting an item based on its non-unique title
    """
    login_name = "Delete Me Unique"
    vault = "Test Data"
    expected = expected_login_item_data.data_for_login(login_name)
    expected_item_id = expected.unique_id
    result = signed_in_op.item_delete(login_name, vault=vault)
    assert result == expected_item_id


def test_item_delete_non_existent_01(signed_in_op: OP):
    """
    Test deleting a non-existent item
    """
    login_name = "non-existent-item"
    vault = "Test Data"

    with pytest.raises(OPItemDeleteException):
        signed_in_op.item_delete(login_name, vault=vault)


def test_item_delete_non_existent_02(signed_in_op: OP):
    """
    Test deleting a non-existent item, bypassing item_get()
    """
    login_name = "non-existent-item"
    vault = "Test Data"

    with pytest.raises(OPItemDeleteException):
        # OP.item_delete() calls item_get() first
        # which will fail on non-existent items
        # so in order to test delete operatation failing, we
        # need to call private ._item_delete() interface
        signed_in_op._item_delete(login_name, vault=vault)
