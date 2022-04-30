from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pyonepassword import OP

from pyonepassword import OPItemList
from pyonepassword.op_items.password import OPPasswordItemDescriptor


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


def test_item_list_password_01(signed_in_op: OP, expected_item_password_data):
    item_id = "2dvgl7kk5yjrq3gxwqimp5awve"
    items: OPItemList = signed_in_op.item_list(vault="Test Data")
    expected = expected_item_password_data.data_for_password(
        "Example Password")
    result = _item_by_id(items, item_id)

    # weird if this doesn't match, but hey
    assert result.unique_id == expected.unique_id
    assert isinstance(result, OPPasswordItemDescriptor)


def test_item_list_password_02(signed_in_op: OP, expected_item_password_data):
    item_id = "2dvgl7kk5yjrq3gxwqimp5awve"
    items: OPItemList = signed_in_op.item_list(vault="Test Data")
    expected = expected_item_password_data.data_for_password(
        "Example Password")
    result = _item_by_id(items, item_id)

    # weird if this doesn't match, but hey
    assert result.unique_id == expected.unique_id
    assert result.title == expected.title


def test_item_list_password_03(signed_in_op: OP, expected_item_password_data):
    item_id = "2dvgl7kk5yjrq3gxwqimp5awve"
    items: OPItemList = signed_in_op.item_list(vault="Test Data")
    expected = expected_item_password_data.data_for_password(
        "Example Password")
    result = _item_by_id(items, item_id)

    # weird if this doesn't match, but hey
    assert result.unique_id == expected.unique_id
    assert result.created_at == expected.created_at


def test_item_list_password_04(signed_in_op: OP, expected_item_password_data):
    item_id = "2dvgl7kk5yjrq3gxwqimp5awve"
    items: OPItemList = signed_in_op.item_list(vault="Test Data")
    expected = expected_item_password_data.data_for_password(
        "Example Password")
    result = _item_by_id(items, item_id)

    # weird if this doesn't match, but hey
    assert result.unique_id == expected.unique_id
    assert result.updated_at == expected.updated_at


def test_item_list_password_05(signed_in_op: OP, expected_item_password_data):
    item_id = "2dvgl7kk5yjrq3gxwqimp5awve"
    items: OPItemList = signed_in_op.item_list(vault="Test Data")
    expected = expected_item_password_data.data_for_password(
        "Example Password")
    result = _item_by_id(items, item_id)

    # weird if this doesn't match, but hey
    assert result.unique_id == expected.unique_id
    assert result.last_edited_by == expected.last_edited_by


def test_item_list_password_06(signed_in_op: OP, expected_item_password_data):
    item_id = "2dvgl7kk5yjrq3gxwqimp5awve"
    items: OPItemList = signed_in_op.item_list(vault="Test Data")
    expected = expected_item_password_data.data_for_password(
        "Example Password")
    result = _item_by_id(items, item_id)

    # weird if this doesn't match, but hey
    assert result.unique_id == expected.unique_id
    assert result.vault_id == expected.vault_id
