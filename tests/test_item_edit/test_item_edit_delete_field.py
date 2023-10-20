from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from pyonepassword.api.exceptions import (
    OPFieldNotFoundException,
    OPSectionNotFoundException
)

if TYPE_CHECKING:
    from pyonepassword import OP
    from pyonepassword.api.object_types import OPAbstractItem

# ensure HOME env variable is set, and there's a valid op config present
pytestmark = pytest.mark.usefixtures("valid_op_cli_config_homedir")


def _get_field_value(item: OPAbstractItem, field_label: str, section_label: str = None):
    """
    Given a field label and optionally a section label, return the field's value
    """

    if section_label:
        section = item.first_section_by_label(section_label)
        field = section.first_field_by_label(field_label)
    else:
        field = item.first_field_by_label(field_label)

    field_value = field.value
    return field_value


@pytest.mark.usefixtures("setup_stateful_item_edit")
def test_item_edit_delete_field_010(signed_in_op: OP):
    """
    Scenario:
    - deleting a section/text field pairing when:
        - Exactly one matching section exists
        - Exactly one matching field exists
        - Matching field belongs to matching section

    Test: OP.item_edit_delete_field()
        - Retrieve an item via OP.item_get()
        - Look up sections based on requested section label
        - Look up fields based on requested field label
        - Call item_edit_delete_field(), saving returned object
        - Retreive the same item a second time
    Verify:
        - The original item has a section matching the requested section label
        - The original item has a field matching the requested field label
        - The returned edited item has no matching section
        - The returned edited item has no matching field
        - The newly retrieved item has no matching section
        - The newly retrieved item has no matching field
    """

    item_name = "Example Login Item 21a"
    field_label = "Text Field 01"
    section_label = "Section 01"
    vault = "Test Data 2"

    # stateful response directory
    # state 1: responses-item-edit/response-directory-1.json
    item_get_1 = signed_in_op.item_get(item_name, vault=vault)

    # item should have the requested section
    section = item_get_1.first_section_by_label(section_label)

    # item should have the requested field
    section.first_field_by_label(field_label)

    edited_item = signed_in_op.item_edit_delete_field(item_name,
                                                      field_label,
                                                      section_label=section_label,
                                                      vault=vault)

    # state changed with item_edit above
    # state 2: responses-item-edit/response-directory-2.json
    item_get_2 = signed_in_op.item_get(item_name, vault=vault)

    with pytest.raises(OPSectionNotFoundException):
        edited_item.first_section_by_label(section_label)
    with pytest.raises(OPFieldNotFoundException):
        edited_item.first_field_by_label(field_label)

    with pytest.raises(OPSectionNotFoundException):
        item_get_2.first_section_by_label(section_label)
    with pytest.raises(OPFieldNotFoundException):
        item_get_2.first_field_by_label(field_label)


@pytest.mark.usefixtures("setup_stateful_item_edit")
def test_item_edit_delete_field_020(signed_in_op: OP):
    """
    Scenario:
    - deleting a text field when:
        - No matching sections exist
        - Exactly one matching field exists
        - Matching field belongs to no section

    Test: OP.item_edit_delete_field()
        - Retrieve an item via OP.item_get()
        - Look up sections based on requested section label
        - Look up fields based on requested field label
        - Call item_edit_delete_field(), saving returned object
        - Retreive the same item a second time
    Verify:
        - The original item has exactly one field matching the requested field label
        - The original item's matching field has no section
        - The returned edited item has no matching field
        - The newly retrieved item has no matching field
    """

    item_name = "Example Login Item 21b"
    field_label = "Text Field 01"
    vault = "Test Data 2"

    # stateful response directory
    # state 1: responses-item-edit/response-directory-1.json
    item_get_1 = signed_in_op.item_get(item_name, vault=vault)

    # item should have the requested field
    fields = item_get_1.fields_by_label(field_label)
    assert len(fields) == 1
    assert fields[0].section_id is None

    edited_item = signed_in_op.item_edit_delete_field(item_name,
                                                      field_label,
                                                      vault=vault)

    # state changed with item_edit above
    # state 2: responses-item-edit/response-directory-2.json
    item_get_2 = signed_in_op.item_get(item_name, vault=vault)

    with pytest.raises(OPFieldNotFoundException):
        edited_item.first_field_by_label(field_label)

    with pytest.raises(OPFieldNotFoundException):
        item_get_2.first_field_by_label(field_label)
