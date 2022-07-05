from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pyonepassword import OP

from pyonepassword.api.descriptor_types import (
    OPIdentityItemDescriptor,
    OPLoginDescriptorItem
)
from pyonepassword.api.object_types import OPItemList

# ensure HOME env variable is set, and there's a valid op config present
pytestmark = pytest.mark.usefixtures("valid_op_cli_config_homedir")


def _item_by_id(item_list: OPItemList, item_id):
    item = None
    for item in item_list:
        if item.unique_id == item_id:
            break
    return item


def _items_by_title(item_list: OPItemList, item_title):
    items = []
    for item in item_list:
        if item.title == item_title:
            items.append(item)
    return items


def test_items_list_multiple_01(signed_in_op: OP, expected_login_item_data):
    login_item_title = "Example Login 1"
    items: OPItemList = signed_in_op.item_list(
        vault="Test Data", categories=["login", "identity"])
    result = _items_by_title(items, login_item_title)
    result: OPLoginDescriptorItem = result[0]
    expected = expected_login_item_data.data_for_login(login_item_title)
    assert isinstance(result, OPLoginDescriptorItem)
    assert result.unique_id == expected.unique_id
    assert result.created_at == expected.created_at


def test_items_list_multiple_02(signed_in_op: OP, expected_identity_data):
    identity_item_title = "Example Identity"
    items: OPItemList = signed_in_op.item_list(
        vault="Test Data", categories=["login", "identity"])
    result = _items_by_title(items, identity_item_title)
    result: OPIdentityItemDescriptor = result[0]
    expected = expected_identity_data.data_for_identity(identity_item_title)
    assert isinstance(result, OPIdentityItemDescriptor)
    assert result.unique_id == expected.unique_id
    assert result.created_at == expected.created_at
