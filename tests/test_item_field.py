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


def test_item_field_02(valid_data: ValidData, expected_item_field_data: ExpectedItemFieldData):
    expected: ExpectedItemField

    expected = expected_item_field_data.data_for_key("example-login-username")
    field_dict = valid_data.data_for_name("login-item-field-username")
    field = OPItemField(field_dict)
    assert field.field_type == expected.type


def test_item_field_03(valid_data: ValidData, expected_item_field_data: ExpectedItemFieldData):
    expected: ExpectedItemField

    expected = expected_item_field_data.data_for_key("example-login-username")
    field_dict = valid_data.data_for_name("login-item-field-username")
    field = OPItemField(field_dict)
    assert field.reference is not None
    assert field.reference == expected.reference


def test_item_field_04(valid_data: ValidData, expected_item_field_data: ExpectedItemFieldData):
    expected: ExpectedItemField

    expected = expected_item_field_data.data_for_key("example-login-username")
    field_dict = valid_data.data_for_name("login-item-field-username")
    field = OPItemField(field_dict)
    assert field.label == expected.label


def test_item_field_05(valid_data: ValidData, expected_item_field_data: ExpectedItemFieldData):
    expected: ExpectedItemField

    expected = expected_item_field_data.data_for_key("example-login-username")
    field_dict = valid_data.data_for_name("login-item-field-username")
    field = OPItemField(field_dict)
    assert field.value == expected.value


def test_item_field_06(valid_data: ValidData, expected_item_field_data: ExpectedItemFieldData):
    expected: ExpectedItemField

    expected = expected_item_field_data.data_for_key("example-login-username")
    field_dict = valid_data.data_for_name("login-item-field-username")
    field = OPItemField(field_dict)
    assert field.purpose == expected.purpose


def test_item_field_11(valid_data: ValidData, expected_item_field_data: ExpectedItemFieldData):
    expected: ExpectedItemField

    expected = expected_item_field_data.data_for_key("example-login-password")
    field_dict = valid_data.data_for_name("login-item-field-password")
    field = OPItemField(field_dict)
    assert field.field_id == expected.field_id


def test_item_field_12(valid_data: ValidData, expected_item_field_data: ExpectedItemFieldData):
    expected: ExpectedItemField

    expected = expected_item_field_data.data_for_key("example-login-password")
    field_dict = valid_data.data_for_name("login-item-field-password")
    field = OPItemField(field_dict)
    assert field.field_type == expected.type


def test_item_field_13(valid_data: ValidData, expected_item_field_data: ExpectedItemFieldData):
    expected: ExpectedItemField

    expected = expected_item_field_data.data_for_key("example-login-password")
    field_dict = valid_data.data_for_name("login-item-field-password")
    field = OPItemField(field_dict)
    assert field.reference is not None
    assert field.reference == expected.reference


def test_item_field_14(valid_data: ValidData, expected_item_field_data: ExpectedItemFieldData):
    expected: ExpectedItemField

    expected = expected_item_field_data.data_for_key("example-login-password")
    field_dict = valid_data.data_for_name("login-item-field-password")
    field = OPItemField(field_dict)
    assert field.label == expected.label


def test_item_field_15(valid_data: ValidData, expected_item_field_data: ExpectedItemFieldData):
    expected: ExpectedItemField

    expected = expected_item_field_data.data_for_key("example-login-password")
    field_dict = valid_data.data_for_name("login-item-field-password")
    field = OPItemField(field_dict)
    assert field.value == expected.value


def test_item_field_16(valid_data: ValidData, expected_item_field_data: ExpectedItemFieldData):
    expected: ExpectedItemField

    expected = expected_item_field_data.data_for_key("example-login-password")
    field_dict = valid_data.data_for_name("login-item-field-password")
    field = OPItemField(field_dict)
    assert field.purpose == expected.purpose


def test_item_field_17(valid_data: ValidData, expected_item_field_data: ExpectedItemFieldData):
    expected: ExpectedItemField
    expected = expected_item_field_data.data_for_key("example-login-password")
    field_dict = valid_data.data_for_name("login-item-field-password")
    field = OPItemField(field_dict)
    assert isinstance(field.entropy, float)
    margin = .000001
    expected_entropy = expected.entropy
    high = expected_entropy * (1 + margin)
    low = expected_entropy * (1 - margin)
    assert field.entropy < high
    assert field.entropy > low
