# __future__.annotations, and typing.TYPE_CHECKING
# enable anything imported for type hinting to disappear at run time
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

# make imports for type-hinting disappear at run-time to avoid
# circular imports.
# this also reduced exercising tested code simply by importing
if TYPE_CHECKING:
    # non-runtime imports here
    from pyonepassword import OP
    from .fixtures.expected_item_list import ExpectedItemListData, ExpectedItemList

from pyonepassword.api.object_types import OPItemList

# ensure HOME env variable is set, and there's a valid op config present
pytestmark = pytest.mark.usefixtures("valid_op_cli_config_homedir")


def _validate_item_list(item_list, expected_item_list):
    assert isinstance(item_list, OPItemList)
    assert len(item_list) == len(expected_item_list)


def test_item_delete_multiple_01(signed_in_op: OP, expected_item_list_data: ExpectedItemListData):
    expected_items: ExpectedItemList = expected_item_list_data.data_for_name(
        "item-list-test-vault-3")
    vault_name = "Test Data 3"
    deleted_items: OPItemList
    deleted_items = signed_in_op.item_delete_multiple(vault_name)

    _validate_item_list(deleted_items, expected_items)

    for expected, actual in zip(expected_items, deleted_items):
        assert expected.unique_id == actual.unique_id
        assert expected.title == actual.title
