from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pyonepassword import OP

from pyonepassword.api.descriptor_types import OPLoginDescriptorItem
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


def test_items_list_tags_01(signed_in_op: OP):

    # tags are ORed, so there should be more than one result
    result: OPItemList = signed_in_op.item_list(
        vault="Test Data", tags=["example-tag-1", "example-tag-2"])

    assert len(result) == 2


def test_items_list_tags_02(signed_in_op: OP):
    result: OPItemList = signed_in_op.item_list(
        vault="Test Data", tags=["example-tag-2"])

    assert len(result) == 1


def test_items_list_tags_03(signed_in_op: OP, expected_login_item_data):
    login_item_title = "Login Item with 2 Tags"

    items: OPItemList = signed_in_op.item_list(
        vault="Test Data", tags=["example-tag-2"])
    result = _items_by_title(items, login_item_title)
    result: OPLoginDescriptorItem = result[0]

    expected = expected_login_item_data.data_for_login(login_item_title)
    assert isinstance(result, OPLoginDescriptorItem)
    assert result.unique_id == expected.unique_id
    assert result.created_at == expected.created_at


def test_items_list_tags_04(signed_in_op: OP, expected_login_item_data):
    login_item_title = "Login Item with 1 Tag"

    # tags are ORed, so there should be more than one result
    items: OPItemList = signed_in_op.item_list(
        vault="Test Data", tags=["example-tag-1", "example-tag-2"])
    result = _items_by_title(items, login_item_title)
    result: OPLoginDescriptorItem = result[0]

    expected = expected_login_item_data.data_for_login(login_item_title)
    assert isinstance(result, OPLoginDescriptorItem)
    assert result.unique_id == expected.unique_id
    assert result.created_at == expected.created_at
