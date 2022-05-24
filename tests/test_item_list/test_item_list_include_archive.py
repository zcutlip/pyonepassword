from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pyonepassword import OP
    from ..fixtures.expected_server import ExpectedServer

from pyonepassword import OPItemList
from pyonepassword.op_items.server import OPServerItemDescriptor

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


def test_items_list_archived_server_01(signed_in_op: OP, expected_server_data):
    server_title = "Archived Machine with SSH Keys"
    items: OPItemList = signed_in_op.item_list(
        include_archive=True, vault="Test Data")
    result = _items_by_title(items, server_title)
    result: OPServerItemDescriptor = result[0]
    expected: ExpectedServer = expected_server_data.data_for_server(
        server_title)

    assert isinstance(result, OPServerItemDescriptor)
    assert result.unique_id == expected.unique_id
    assert result.archived == expected.archived
