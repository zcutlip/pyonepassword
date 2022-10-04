from __future__ import annotations

from typing import TYPE_CHECKING

from pyonepassword.op_items._new_field_registry import OPItemFieldFactory
from pyonepassword.op_items._new_fields import OPNewStringField
from pyonepassword.op_items.item_section import OPItemField

if TYPE_CHECKING:
    from ..fixtures.expected_item_fields import (
        ExpectedItemField,
        ExpectedItemFieldData
    )
    from ..fixtures.valid_data import ValidData


def test_item_field_factory_01(valid_data: ValidData, expected_item_field_data: ExpectedItemFieldData):
    expected: ExpectedItemField

    expected = expected_item_field_data.data_for_key("example-login-username")
    field_dict = valid_data.data_for_name("login-item-field-username")

    existing_field = OPItemField(field_dict)

    new_field = OPItemFieldFactory.item_field(existing_field)

    assert isinstance(new_field, OPNewStringField)
    assert new_field.value == expected.value


def test_item_field_factory_02(valid_data: ValidData, expected_item_field_data: ExpectedItemFieldData):
    expected: ExpectedItemField

    expected = expected_item_field_data.data_for_key("example-login-username")
    field_dict = valid_data.data_for_name("login-item-field-username")

    existing_field = OPItemField(field_dict)

    new_field = OPItemFieldFactory.item_field(existing_field)

    assert isinstance(new_field, OPNewStringField)
    assert new_field.field_id == expected.field_id
