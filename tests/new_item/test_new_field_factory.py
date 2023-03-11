from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from pyonepassword.op_items._new_field_registry import (
    OPNewItemFieldFactory,
    OPUnknownFieldTypeException
)
from pyonepassword.op_items._new_fields import OPNewStringField
from pyonepassword.op_items.item_field_base import OPItemField
from pyonepassword.py_op_exceptions import OPInvalidFieldException

if TYPE_CHECKING:
    from ..fixtures.expected_item_fields import (
        ExpectedItemField,
        ExpectedItemFieldData
    )
    from ..fixtures.invalid_data import InvalidData
    from ..fixtures.valid_data import ValidData


def test_item_field_factory_01(valid_data: ValidData, expected_item_field_data: ExpectedItemFieldData):
    expected: ExpectedItemField

    expected = expected_item_field_data.data_for_key("example-login-username")
    field_dict = valid_data.data_for_name("login-item-field-username")

    existing_field = OPItemField(field_dict)

    new_field = OPNewItemFieldFactory.item_field(existing_field)

    assert isinstance(new_field, OPNewStringField)
    assert new_field.value == expected.value


def test_item_field_factory_02(valid_data: ValidData, expected_item_field_data: ExpectedItemFieldData):
    expected: ExpectedItemField

    expected = expected_item_field_data.data_for_key("example-login-username")
    field_dict = valid_data.data_for_name("login-item-field-username")

    existing_field = OPItemField(field_dict)

    new_field = OPNewItemFieldFactory.item_field(existing_field)

    assert isinstance(new_field, OPNewStringField)
    assert new_field.field_id == expected.field_id


def test_item_field_factory_unknown_field_type_01(invalid_data: InvalidData):
    unk_field_type_dict = invalid_data.data_for_name("unknown-field-type")
    with pytest.raises(OPUnknownFieldTypeException):
        OPNewItemFieldFactory.item_field(unk_field_type_dict)


def test_item_field_factory_malformed_field_json_01(invalid_data: InvalidData):
    malformed_json = invalid_data.data_for_name("malformed-field-json")
    with pytest.raises(OPInvalidFieldException):
        OPNewItemFieldFactory.item_field(malformed_json)
