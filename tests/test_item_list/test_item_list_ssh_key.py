from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from ..fixtures.expected_ssh_key_data import ExpectedSSHKey, ExpectedSSHKeyData
    from pyonepassword import OP

from pyonepassword.api.descriptor_types import OPSSHKeyItemDescriptor
from pyonepassword.api.object_types import OPItemList

# ensure HOME env variable is set, and there's a valid op config present
pytestmark = pytest.mark.usefixtures("valid_op_cli_config_homedir")


def _item_by_id(item_list: OPItemList, item_id):
    item = None
    for _item in item_list:
        if _item.unique_id == item_id:
            item = _item
            break
    return item


def _items_by_title(item_list: OPItemList, item_title):
    items = []
    for item in item_list:
        if item.title == item_title:
            items.append(item)
    return items


def test_item_list_ssh_key_01(signed_in_op: OP, expected_ssh_key_data: ExpectedSSHKeyData):
    item_id = "k7t4uzbuf3fn7d7wrajh5xb3gi"
    items: OPItemList = signed_in_op.item_list(vault="Test Data")
    expected: ExpectedSSHKey = expected_ssh_key_data.data_for_ssh_key(
        "Example SSH Key")
    result = _item_by_id(items, item_id)

    # weird if this doesn't match, but hey
    print(type(result))
    assert isinstance(result, OPSSHKeyItemDescriptor)
    assert result.unique_id == expected.unique_id


def test_item_list_ssh_key_02(signed_in_op: OP, expected_ssh_key_data: ExpectedSSHKeyData):
    item_id = "k7t4uzbuf3fn7d7wrajh5xb3gi"
    items: OPItemList = signed_in_op.item_list(vault="Test Data")
    expected: ExpectedSSHKey = expected_ssh_key_data.data_for_ssh_key(
        "Example SSH Key")
    result = _item_by_id(items, item_id)

    # weird if this doesn't match, but hey
    assert result.unique_id == expected.unique_id
    assert result.title == expected.title


def test_item_list_ssh_key_03(signed_in_op: OP, expected_ssh_key_data: ExpectedSSHKeyData):
    item_id = "k7t4uzbuf3fn7d7wrajh5xb3gi"
    items: OPItemList = signed_in_op.item_list(vault="Test Data")
    expected: ExpectedSSHKey = expected_ssh_key_data.data_for_ssh_key(
        "Example SSH Key")
    result = _item_by_id(items, item_id)

    # weird if this doesn't match, but hey
    assert result.unique_id == expected.unique_id
    assert result.created_at == expected.created_at


def test_item_list_ssh_key_04(signed_in_op: OP, expected_ssh_key_data: ExpectedSSHKeyData):
    item_id = "k7t4uzbuf3fn7d7wrajh5xb3gi"
    items: OPItemList = signed_in_op.item_list(vault="Test Data")
    expected: ExpectedSSHKey = expected_ssh_key_data.data_for_ssh_key(
        "Example SSH Key")
    result = _item_by_id(items, item_id)

    # weird if this doesn't match, but hey
    assert result.unique_id == expected.unique_id
    assert result.updated_at == expected.updated_at


def test_item_list_ssh_key_05(signed_in_op: OP, expected_ssh_key_data: ExpectedSSHKeyData):
    item_id = "k7t4uzbuf3fn7d7wrajh5xb3gi"
    items: OPItemList = signed_in_op.item_list(vault="Test Data")
    expected: ExpectedSSHKey = expected_ssh_key_data.data_for_ssh_key(
        "Example SSH Key")
    result = _item_by_id(items, item_id)

    # weird if this doesn't match, but hey
    assert result.unique_id == expected.unique_id
    assert result.last_edited_by == expected.last_edited_by


def test_item_list_ssh_key_06(signed_in_op: OP, expected_ssh_key_data: ExpectedSSHKeyData):
    item_id = "k7t4uzbuf3fn7d7wrajh5xb3gi"
    items: OPItemList = signed_in_op.item_list(vault="Test Data")
    expected: ExpectedSSHKey = expected_ssh_key_data.data_for_ssh_key(
        "Example SSH Key")
    result = _item_by_id(items, item_id)

    from pprint import pprint
    pprint(result, sort_dicts=False, indent=2)
    # weird if this doesn't match, but hey
    assert result.unique_id == expected.unique_id
    assert result.vault_id == expected.vault_id


def test_item_list_ssh_key_07(signed_in_op: OP, expected_ssh_key_data: ExpectedSSHKeyData):
    item_id = "k7t4uzbuf3fn7d7wrajh5xb3gi"
    items: OPItemList = signed_in_op.item_list(vault="Test Data")
    expected: ExpectedSSHKey = expected_ssh_key_data.data_for_ssh_key(
        "Example SSH Key")
    result: OPSSHKeyItemDescriptor = _item_by_id(items, item_id)

    from pprint import pprint
    pprint(result, sort_dicts=False, indent=2)
    # weird if this doesn't match, but hey
    assert result.unique_id == expected.unique_id
    assert result.fingerprint == expected.fingerprint
