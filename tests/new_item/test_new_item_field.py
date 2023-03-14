from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from pyonepassword.op_items._new_fields import (
    OPNewStringField,
    OPNewUsernameField
)
from pyonepassword.op_items._new_item import OPNewSection
from pyonepassword.op_items.item_field_base import OPItemField
from pyonepassword.op_items.item_section import OPItemFieldCollisionException

if TYPE_CHECKING:
    from ..fixtures.expected_item_fields import (
        ExpectedItemField,
        ExpectedItemFieldData
    )
    from ..fixtures.valid_data import ValidData


def test_new_username_field_01(valid_data: ValidData, expected_item_field_data: ExpectedItemFieldData):
    """
    Create a new OPUsernameField
    Verify the 'value' property
    """
    expected: ExpectedItemField

    expected = expected_item_field_data.data_for_key("example-login-username")
    field_dict = valid_data.data_for_name("login-item-field-username")

    username = field_dict["value"]
    field_id = field_dict["id"]
    new_field = OPNewUsernameField(field_id, username, field_id=field_id)

    assert new_field.value == expected.value


def test_new_username_field_02(valid_data: ValidData, expected_item_field_data: ExpectedItemFieldData):
    """
    Create a new OPUsernameField
    Verify the 'field_id' property
    """
    expected: ExpectedItemField

    expected = expected_item_field_data.data_for_key("example-login-username")
    field_dict = valid_data.data_for_name("login-item-field-username")

    username = field_dict["value"]
    field_id = field_dict["id"]
    new_field = OPNewUsernameField(field_id, username, field_id=field_id)

    assert new_field.field_id == expected.field_id


def test_new_username_field_03(valid_data: ValidData, expected_item_field_data: ExpectedItemFieldData):
    """
    Create a new OPUsernameField
    Verify the 'label' property
    """
    expected: ExpectedItemField

    expected = expected_item_field_data.data_for_key("example-login-username")
    field_dict = valid_data.data_for_name("login-item-field-username")

    username = field_dict["value"]
    field_id = field_dict["id"]
    new_field = OPNewUsernameField(field_id, username, field_id=field_id)

    assert new_field.label == expected.label


def test_new_username_field_04(valid_data: ValidData, expected_item_field_data: ExpectedItemFieldData):
    """
    Create a new OPUsernameField
    Verify the 'purpose' property
    """
    expected: ExpectedItemField

    expected = expected_item_field_data.data_for_key("example-login-username")
    field_dict = valid_data.data_for_name("login-item-field-username")

    username = field_dict["value"]
    field_id = field_dict["id"]
    new_field = OPNewUsernameField(field_id, username, field_id=field_id)

    assert new_field.purpose == expected.purpose


def test_new_username_field_05(valid_data: ValidData, expected_item_field_data: ExpectedItemFieldData):
    """
    Create a new field from an existing field
    Verify the 'value' property
    """
    expected: ExpectedItemField

    expected = expected_item_field_data.data_for_key("example-login-username")
    field_dict = valid_data.data_for_name("login-item-field-username")

    existing_field = OPItemField(field_dict)

    new_field = OPNewUsernameField.from_field(existing_field)

    assert new_field.value == expected.value


def test_new_username_field_06(valid_data: ValidData, expected_item_field_data: ExpectedItemFieldData):
    """
    Create a new field from an existing field
    Verify the 'field_id' property
    """
    expected: ExpectedItemField

    expected = expected_item_field_data.data_for_key("example-login-username")
    field_dict = valid_data.data_for_name("login-item-field-username")

    existing_field = OPItemField(field_dict)

    new_field = OPNewUsernameField.from_field(existing_field)

    assert new_field.field_id == expected.field_id


def test_new_username_field_07(valid_data: ValidData, expected_item_field_data: ExpectedItemFieldData):
    """
    Create a new field from an existing field
    Verify the 'label' property
    """
    expected: ExpectedItemField

    expected = expected_item_field_data.data_for_key("example-login-username")
    field_dict = valid_data.data_for_name("login-item-field-username")

    existing_field = OPItemField(field_dict)

    new_field = OPNewUsernameField.from_field(existing_field)

    assert new_field.label == expected.label


def test_new_username_field_08(valid_data: ValidData, expected_item_field_data: ExpectedItemFieldData):
    """
    Create a new field from an existing field
    Verify the 'purpose' property
    """
    expected: ExpectedItemField

    expected = expected_item_field_data.data_for_key("example-login-username")
    field_dict = valid_data.data_for_name("login-item-field-username")

    existing_field = OPItemField(field_dict)

    new_field = OPNewUsernameField.from_field(existing_field)

    assert new_field.purpose == expected.purpose


def test_new_field_generate_uuid_01(valid_data: ValidData):
    """
    Create a new field from an existing field that has a hex UUID for field ID
    Verify the new field has a newly generated ID that is not the same as the original
    """
    field_dict = valid_data.data_for_name("example-field-with-uuid-1")
    existing_field = OPItemField(field_dict)

    new_field = OPNewStringField.from_field(existing_field)
    print(existing_field.field_id)
    print(new_field.field_id)
    assert new_field.field_id != existing_field.field_id


def test_new_field_generate_uuid_02(valid_data: ValidData):
    """
    Generate two identical fields without specificying field ID
    Verify field ID gets generated and is random for both
    """
    field_dict = valid_data.data_for_name("example-field-with-uuid-1")
    existing_field = OPItemField(field_dict)

    field_label = existing_field.label
    field_value = existing_field.value

    new_field_1 = OPNewStringField(field_label, field_value)
    new_field_2 = OPNewStringField(field_label, field_value)

    assert new_field_1.field_id is not None
    assert new_field_2.field_id is not None
    assert new_field_1.field_id != new_field_2.field_id


def test_new_field_with_section_01(valid_data: ValidData):
    """
    Create:
      - a new section
      - new field, registering with the new section

    Verify new_field.section_id matches new_section.section_id
    """
    section_dict = valid_data.data_for_name("example-item-section-1")
    field_dict = valid_data.data_for_name("example-field-no-uuid-1")
    f_label = field_dict["label"]
    f_value = field_dict["value"]
    f_id = field_dict["id"]

    s_label = section_dict["label"]
    new_section = OPNewSection(s_label)

    new_field = OPNewStringField(
        f_label, f_value, field_id=f_id, section=new_section)

    assert new_field.section_id == new_section.section_id


def test_new_field_with_section_02(valid_data: ValidData):
    """
    create a new section and a new field registered to the section. Then create a second, identical
    field registered to the same section

    Verify OPItemFieldCollisionException is raised
    """
    section_dict = valid_data.data_for_name("example-item-section-1")
    field_dict = valid_data.data_for_name("example-field-no-uuid-1")
    f_label = field_dict["label"]
    f_value = field_dict["value"]
    f_id = field_dict["id"]

    s_label = section_dict["label"]
    new_section = OPNewSection(s_label)

    _ = OPNewStringField(f_label, f_value, field_id=f_id, section=new_section)

    with pytest.raises(OPItemFieldCollisionException):
        OPNewStringField(f_label, f_value, field_id=f_id, section=new_section)
