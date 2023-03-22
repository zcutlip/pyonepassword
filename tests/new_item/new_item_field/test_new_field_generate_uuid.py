from __future__ import annotations

from typing import TYPE_CHECKING

from pyonepassword.op_items.fields_sections._new_fields import OPNewStringField
from pyonepassword.op_items.fields_sections.item_field_base import OPItemField

if TYPE_CHECKING:
    from ...fixtures.valid_data import ValidData


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
