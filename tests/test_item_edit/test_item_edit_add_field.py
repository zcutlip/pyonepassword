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
def test_item_edit_add_text_field_010(signed_in_op: OP):
    """
    Test: OP.item_edit_add_text_field()
        - Retrieve an item via OP.item_get()
        - Look up sections based on requested section label
        - Look up fields based on requested field label
        - Call item_edit_add_text_field(), saving returned object
        - Retreive the same item a second time

    Verify:
        - The original item has no sections matching the requested section label
        - The original item has no fields matching the requested field label
        - The returned edited item field's value is the same as newly retrieved item field's value
        - The newly retrieved item field's value is the same as the desired new value
    """

    item_name = "Example Login Item 17"
    field_label = "Text Field 01"
    section_label = "Section 01"
    new_field_value = "new text field value"
    vault = "Test Data 2"

    # stateful response directory
    # state 1: responses-item-edit/response-directory-1.json
    item_get_1 = signed_in_op.item_get(item_name, vault=vault)

    # item should not have the requested section
    with pytest.raises(OPSectionNotFoundException):
        item_get_1.sections_by_label(section_label)

    # item should not have the requested field
    with pytest.raises(OPFieldNotFoundException):
        item_get_1.fields_by_label(field_label)

    edited_item = signed_in_op.item_edit_add_text_field(item_name,
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
def test_item_edit_add_text_field_020(signed_in_op: OP):
    """
    Scenario:
    - adding a section/text field pairing when:
        - Matching section does not exist
        - Matching text field does exist
        - Existing text field belongs to a non-matching section

    This should succeed because the new (section, field) pairing does not
    match any existing (section, field) pairing

    Test: OP.item_edit_add_text_field(),
        - Retrieve an item via OP.item_get()
        - Look up sections based on requested section label
        - Look up fields based on requested field label
        - Call item_edit_add_text_field(), saving returned object
        - Retreive the same item a second time

    Verify:
        - The original item has no sections matching the requested section label
        - The original item has at least one field matching the requested field label
        - The returned edited item field's value is the same as newly retrieved item field's value
        - The newly retrieved item field's value is the same as the desired new value
    """

    item_name = "Example Login Item 17a"
    field_label = "Text Field 01"
    section_label = "Section 01"
    new_field_value = "new text field value"
    vault = "Test Data 2"

    # stateful response directory
    # state 1: responses-item-edit/response-directory-1.json
    item_get_1 = signed_in_op.item_get(item_name, vault=vault)

    # item should not have the requested section
    with pytest.raises(OPSectionNotFoundException):
        item_get_1.sections_by_label(section_label)

    # item SHOULD have the requested field
    try:
        item_get_1.fields_by_label(field_label)
    except OPFieldNotFoundException:
        assert False, f"Item SHOULD have the field: {field_label}"

    edited_item = signed_in_op.item_edit_add_text_field(item_name,
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
def test_item_edit_add_text_field_030(signed_in_op: OP):
    """
    Scenario:
    - adding a section/text field pairing when:
        - Matching section does exist
        - Matching text field does not exist

    This should succeed because the new (section, field) pairing does not
    match any existing (section, field) pairing

    Test: OP.item_edit_add_text_field(),
        - Retrieve an item via OP.item_get()
        - Look up sections based on requested section label
        - Look up fields based on requested field label
        - Call item_edit_add_text_field(), saving returned object
        - Retreive the same item a second time

    Verify:
        - The original item has at least one section matching the requested section label
        - The original item has no fields matching the requested field label
        - The returned edited item field's value is the same as newly retrieved item field's value
        - The newly retrieved item field's value is the same as the desired new value
    """

    item_name = "Example Login Item 17b"
    field_label = "Text Field 01"
    section_label = "Section 01"
    new_field_value = "new text field value"
    vault = "Test Data 2"

    # stateful response directory
    # state 1: responses-item-edit/response-directory-1.json
    item_get_1 = signed_in_op.item_get(item_name, vault=vault)

    # item should have the requested section

    try:
        item_get_1.sections_by_label(section_label)
    except OPSectionNotFoundException:
        assert False, f"Item SHOULD have the section: {section_label}"

    # item should not have the requested field
    with pytest.raises(OPFieldNotFoundException):
        item_get_1.fields_by_label(field_label)

    edited_item = signed_in_op.item_edit_add_text_field(item_name,
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
def test_item_edit_add_text_field_040(signed_in_op: OP):
    """
    Scenario:
    - adding a section/text field pairing when:
        - Matching section exists
        - Matching text field exists
        - Existing text field belongs to a non-matching section

    This should succeed because the new (section, field) pairing does not
    match any existing (section, field) pairing

    Test: OP.item_edit_add_text_field(),
        - Retrieve an item via OP.item_get()
        - Look up sections based on requested section label
        - Look up fields based on requested field label
        - Call item_edit_add_text_field(), saving returned object
        - Retreive the same item a second time

    Verify:
        - The original item has at least one section matching the requested section label
        - The original item has at least one field matching the requested field label
        - The original item does not have a (section, field) pairing matching what is to be added
        - The returned edited item field's value is the same as newly retrieved item field's value
        - The newly retrieved item field's value is the same as the desired new value
    """

    item_name = "Example Login Item 17c"
    field_label = "Text Field 01"
    section_label = "Section 01"
    new_field_value = "new text field value"
    vault = "Test Data 2"

    # stateful response directory
    # state 1: responses-item-edit/response-directory-1.json
    item_get_1 = signed_in_op.item_get(item_name, vault=vault)

    # item should have the requested section

    try:
        item_get_1.sections_by_label(section_label)
    except OPSectionNotFoundException:
        assert False, f"Item SHOULD have the section: {section_label}"

    # item should have the requested field
    try:
        item_get_1.fields_by_label(field_label)
    except OPFieldNotFoundException:
        assert False, f"Item SHOULD have the field: {field_label}"

    with pytest.raises(OPFieldNotFoundException):
        # even though there is a matching section and a matching field,
        # the two are not paired, so an exception is raised
        _get_field_value(item_get_1, field_label, section_label=section_label)

    edited_item = signed_in_op.item_edit_add_text_field(item_name,
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
def test_item_edit_add_text_field_045(signed_in_op: OP):
    """
    Scenario:
    - adding a text field with no section when:
        - Item has no existing sections
        - No fields other than the default fields
    This should succeed because:
        - the (<no section>, field) pairing does not exist
        - no ambiguosly matching fields exist belonging to a section

    Test: OP.item_edit_add_text_field(),
        - Retrieve an item via OP.item_get()
        - Access original item's sections property
        - Look up fields based on requested field label
        - Call item_edit_add_text_field(), saving returned object
        - Retreive the same item a second time

    Verify:
        - The original item has no sections
        - The original item has no fields matching the requested field label
        - The returned edited item field's value is the same as newly retrieved item field's value
        - The newly retrieved item field's value is the same as the desired new value
    """

    item_name = "Example Login Item 17d"
    field_label = "Text Field With no Section 01"
    new_field_value = "new text field value"
    vault = "Test Data 2"

    # stateful response directory
    # state 1: responses-item-edit/response-directory-1.json
    item_get_1 = signed_in_op.item_get(item_name, vault=vault)

    # item should have the requested section

    assert not item_get_1.sections, "Item should have no sections"

    # item should have no fields other than the default
    # no public access to fields, so we'll have to settle for this
    with pytest.raises(OPFieldNotFoundException):
        item_get_1.first_field_by_label(field_label)

    edited_item = signed_in_op.item_edit_add_text_field(item_name,
                                                        new_field_value,
                                                        field_label,
                                                        vault=vault)

    # state changed with item_edit above
    # state 2: responses-item-edit/response-directory-2.json
    item_get_2 = signed_in_op.item_get(item_name, vault=vault)

    edited_item_field_value = _get_field_value(edited_item, field_label)
    item_2_field_value = _get_field_value(item_get_2, field_label)

    # ensure the field value in the item returned from the edit operation
    # matches the field value for the same item in a subsequent "item_get" operation
    assert edited_item_field_value == item_2_field_value

    # ensure the field value for the newly retrieved item matches the intended new field value
    assert item_2_field_value == new_field_value


@pytest.mark.usefixtures("setup_stateful_item_edit")
def test_item_edit_add_password_field_050(signed_in_op: OP):
    """
    Test: OP.item_edit_add_password_field()
        - Retrieve an item via OP.item_get()
        - Look up sections based on requested section label
        - Look up fields based on requested field label
        - Call item_edit_add_password_field(), saving returned object
        - Retreive the same item a second time

    Verify:
        - The original item has no sections matching the requested section label
        - The original item has no fields matching the requested field label
        - The returned edited item field's value is the same as newly retrieved item field's value
        - The newly retrieved item field's value is the same as the desired new value
    """

    item_name = "Example Login Item 18"
    field_label = "Password Field 01"
    section_label = "Section 01"
    new_field_value = "new password field value"
    vault = "Test Data 2"

    # stateful response directory
    # state 1: responses-item-edit/response-directory-1.json
    item_get_1 = signed_in_op.item_get(item_name, vault=vault)

    # item should not have the requested section
    try:
        item_get_1.sections_by_label(section_label)
        assert False, f"Item should not have the section: {section_label}"
    except OPSectionNotFoundException:
        pass

    # item should not have the requested field
    try:
        item_get_1.fields_by_label(field_label)
        assert False, f"Item should not have the field: {field_label}"
    except OPFieldNotFoundException:
        pass

    edited_item = signed_in_op.item_edit_add_password_field(item_name,
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
def test_item_edit_add_url_field_060(signed_in_op: OP):
    """
    Test: OP.item_edit_add_url_field()
        - Retrieve an item via OP.item_get()
        - Look up sections based on requested section label
        - Look up fields based on requested field label
        - Call item_edit_add_url_field(), saving returned object
        - Retreive the same item a second time

    Verify:
        - The original item has no sections matching the requested section label
        - The original item has no fields matching the requested field label
        - The returned edited item field's value is the same as newly retrieved item field's value
        - The newly retrieved item field's value is the same as the desired new value
    """

    item_name = "Example Login Item 23"
    field_label = "URL Field 01"
    section_label = "Section 01"
    new_field_value = "https://new-url-field.com/"
    vault = "Test Data 2"

    # stateful response directory
    # state 1: responses-item-edit/response-directory-1.json
    item_get_1 = signed_in_op.item_get(item_name, vault=vault)

    # item should not have the requested section
    try:
        item_get_1.sections_by_label(section_label)
        assert False, f"Item should not have the section: {section_label}"
    except OPSectionNotFoundException:
        pass

    # item should not have the requested field
    try:
        item_get_1.fields_by_label(field_label)
        assert False, f"Item should not have the field: {field_label}"
    except OPFieldNotFoundException:
        pass

    edited_item = signed_in_op.item_edit_add_url_field(item_name,
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
