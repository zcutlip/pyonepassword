from __future__ import annotations

from typing import TYPE_CHECKING

from pyonepassword.op_items.item_section import OPItemField

if TYPE_CHECKING:
    from .fixtures.expected_item_fields import (
        ExpectedItemField,
        ExpectedItemFieldData
    )
    from .fixtures.valid_data import ValidData


def test_item_field_01(valid_data: ValidData, expected_item_field_data: ExpectedItemFieldData):
    expected: ExpectedItemField

    expected = expected_item_field_data.data_for_key("example-login-username")
    field_dict = valid_data.data_for_name("login-item-field-username")
    field = OPItemField(field_dict)
    assert field.field_id == expected.field_id
