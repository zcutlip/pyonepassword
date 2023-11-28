from __future__ import annotations

import json
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pyonepassword import OP

from pyonepassword.api.object_types import OPItemList

# ensure HOME env variable is set, and there's a valid op config present
pytestmark = pytest.mark.usefixtures("valid_op_cli_config_homedir")


def test_item_list_serialize_01(signed_in_op: OP):
    items: OPItemList = signed_in_op.item_list(vault="Test Data")
    items_json = items.serialize()

    items_copy = OPItemList(json.loads(items_json))
    assert len(items_copy) == len(items)


def test_item_list_serialize_02(signed_in_op: OP):
    items: OPItemList = signed_in_op.item_list(vault="Test Data")
    items_json = items.serialize()
    item_ids = set([item.unique_id for item in items])
    items_copy = OPItemList(json.loads(items_json))
    for item in items_copy:
        assert item.unique_id in item_ids
