from __future__ import annotations

from typing import TYPE_CHECKING

from pyonepassword.op_items._new_item import OPNewSection

from ..test_support.util import is_uuid

if TYPE_CHECKING:
    from ..fixtures.expected_item_sections import (
        ExpectedItemSection,
        ExpectedItemSectionData
    )


def test_new_item_section_01(expected_item_section_data: ExpectedItemSectionData):
    """
    Create a new section providing only a lable
    Verify the label is set as expected
    """
    expected: ExpectedItemSection = expected_item_section_data.data_for_key(
        "example-section-1")
    label = expected.label
    new_section = OPNewSection(label)

    assert new_section.label == expected.label


def test_new_item_section_02(expected_item_section_data: ExpectedItemSectionData):
    """
    Create a new section, providing only a label
    Verify the generated section ID is a UUID
    """
    expected = expected_item_section_data.data_for_key("example-section-1")
    label = expected.label
    new_section = OPNewSection(label)

    assert is_uuid(new_section.section_id)


def test_new_item_section_03(expected_item_section_data: ExpectedItemSectionData):
    """
    Create two new sections providing the same lable
    Verify the sections' IDs are UUIDs and are not the same as each other
    """
    expected = expected_item_section_data.data_for_key("example-section-1")
    label = expected.label

    new_section_1 = OPNewSection(label)
    new_section_2 = OPNewSection(label)

    assert is_uuid(new_section_1.section_id)
    assert is_uuid(new_section_2.section_id)

    assert new_section_1.section_id != new_section_2.section_id
