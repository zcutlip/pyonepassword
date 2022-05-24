from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from pyonepassword.op_items import (
    OPFieldNotFoundException,
    OPItemFactory,
    OPUnknownItemType
)
from pyonepassword.op_items.item_section import OPItemFieldCollisionException
from pyonepassword.py_op_exceptions import OPInvalidItemException

if TYPE_CHECKING:
    from pyonepassword import OP, OPLoginItem


# ensure HOME env variable is set, and there's a valid op config present
pytestmark = pytest.mark.usefixtures("valid_op_cli_config_homedir")


def test_unknown_item_type_01(invalid_data):
    invalid_item_json = invalid_data.data_for_name("invalid-item")
    with pytest.raises(OPUnknownItemType):
        _ = OPItemFactory.op_item(invalid_item_json)


def test_malformed_item_json_01(invalid_data):
    malformed_json = invalid_data.data_for_name("malformed-item-json")
    with pytest.raises(OPInvalidItemException):
        _ = OPItemFactory.op_item(malformed_json)


def test_item_field_not_found_01(signed_in_op: OP):
    item_name = "Example Login 1"
    vault = "Test Data"
    result: OPLoginItem
    result = signed_in_op.item_get(item_name, vault=vault)
    with pytest.raises(OPFieldNotFoundException):
        result.field_by_id("Non-existent-field")


def test_item_field_collision_01(invalid_data):
    field_collision_json = invalid_data.data_for_name("field-collision")
    with pytest.raises(OPItemFieldCollisionException):
        OPItemFactory.op_item(field_collision_json)
