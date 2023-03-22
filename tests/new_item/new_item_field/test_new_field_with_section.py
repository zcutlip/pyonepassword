from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from pyonepassword.op_items._new_item import OPNewSection
from pyonepassword.op_items.fields_sections._new_fields import OPNewStringField
from pyonepassword.op_items.fields_sections.item_section import (
    OPItemFieldCollisionException
)

if TYPE_CHECKING:
    from ...fixtures.valid_data import ValidData


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
