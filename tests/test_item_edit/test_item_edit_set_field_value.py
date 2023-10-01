from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pyonepassword import OP
    from pyonepassword.api.object_types import OPAbstractItem

# ensure HOME env variable is set, and there's a valid op config present
pytestmark = pytest.mark.usefixtures("valid_op_cli_config_homedir")


def _get_field_value(item: OPAbstractItem, field_label: str, section_label: str = None):
    section = None
    if section_label:
        section = item.first_section_by_label(section_label)

    if section:
        field = section.first_field_by_label(field_label)
    else:
        field = item.first_field_by_label(field_label)

    field_value = field.value
    return field_value


@pytest.mark.usefixtures("setup_stateful_item_edit")
def test_item_edit_set_text_field_010(signed_in_op: OP):
    """
    Test: OP.item_edit_set_text_field()
        - Retrieve an item via OP.item_get()
        - Call item_edit_set_text_field(), saving returned object
        - Retreive the same item a second time

    Verify:
        - The original item field's value is not equal to the desired new value
        - The returned edited item field's value is the same as newly retrieved item field's value
        - The newly retrieved item field's value is the same as the desired new value
    """

    item_name = "Example Login Item 12"
    field_label = "Text Field 01"
    section_label = "Section 01"
    new_field_value = "new text field value"
    vault = "Test Data 2"

    # stateful response directory
    # state 1: responses-item-edit/response-directory-1.json
    item_get_1 = signed_in_op.item_get(item_name, vault=vault)

    item_1_field_value = _get_field_value(
        item_get_1, field_label, section_label=section_label)

    assert item_1_field_value != new_field_value

    edited_item = signed_in_op.item_edit_set_text_field(item_name,
                                                        new_field_value,
                                                        field_label,
                                                        section_label=section_label,
                                                        vault=vault)

    # state changed with item_edit above
    # state 2: responses-item-edit/response-directory-2.json
    item_get_2 = signed_in_op.item_get(item_name, vault=vault)

    edited_item_field_value = _get_field_value(
        edited_item, field_label, section_label=section_label)
    item_2_field_value = _get_field_value(
        item_get_2, field_label, section_label=section_label)

    # ensure the field value in the item returned from the edit operation
    # matches the field value for the same item in a subsequent "item_get" operation
    assert edited_item_field_value == item_2_field_value

    # ensure the field value for the newly retrieved item matches the intended new field value
    assert item_2_field_value == new_field_value


@pytest.mark.usefixtures("setup_stateful_item_edit")
def test_item_edit_set_url_field_020(signed_in_op: OP):
    """
    Test: OP.item_edit_set_url_field()
        -

    Verify:
        - The original item's...

    """

    item_name = "Example Login Item 13"
    field_label = "URL Field 01"
    section_label = "Section 01"
    new_field_value = "https://new-url.com/login.html"
    vault = "Test Data 2"

    # stateful response directory
    # state 1: responses-item-edit/response-directory-1.json
    item_get_1 = signed_in_op.item_get(item_name, vault=vault)

    item_1_field_value = _get_field_value(
        item_get_1, field_label, section_label=section_label)

    assert item_1_field_value != new_field_value

    edited_item = signed_in_op.item_edit_set_url_field(item_name,
                                                       new_field_value,
                                                       field_label,
                                                       section_label=section_label,
                                                       vault=vault)

    # state changed with item_edit above
    # state 2: responses-item-edit/response-directory-2.json
    item_get_2 = signed_in_op.item_get(item_name, vault=vault)
    edited_item_field_value = _get_field_value(
        edited_item, field_label, section_label=section_label)
    item_2_field_value = _get_field_value(
        item_get_2, field_label, section_label=section_label)

    # ensure the field value in the item returned from the edit operation
    # matches the field value for the same item in a subsequent "item_get" operation
    assert edited_item_field_value == item_2_field_value

    # ensure the field value for the newly retrieved item matches the intended new field value
    assert item_2_field_value == new_field_value
