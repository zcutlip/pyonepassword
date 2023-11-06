from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from pyonepassword.api.exceptions import (
    OPFieldNotFoundException,
    OPSectionNotFoundException
)
from pyonepassword.py_op_exceptions import (
    OPFieldExistsException,
    OPInsecureOperationException
)

if TYPE_CHECKING:
    from pyonepassword import OP

# ensure HOME env variable is set, and there's a valid op config present
pytestmark = pytest.mark.usefixtures("valid_op_cli_config_homedir")


@pytest.mark.usefixtures("setup_stateful_item_edit")
def test_item_edit_set_password_no_insecure_acknowledge_010(signed_in_op: OP):
    """
    Test: OP.item_edit_set_password() raises OPInsecureOperationException appropriately
        - Attempt to call item_edit_set_password() without passing insecure_operation = True
    Verify:
        - OPInsecureOperationException is raised
    """

    item_name = "Example Login Item 00"
    new_password = "new password"
    vault = "Test Data 2"

    # item_edit_set_password() is inherently insecure, so
    # requires insecure_operation=True
    # This is expected to fail
    with pytest.raises(OPInsecureOperationException):
        signed_in_op.item_edit_set_password(item_name,
                                            new_password,
                                            vault=vault)


@pytest.mark.usefixtures("setup_stateful_item_edit")
def test_item_edit_set_password_invalid_section_020(signed_in_op: OP):
    """
    Test: OPSectionNotFoundException is raised appropriately
        - Attempt to call item_edit_set_password() passing a non-existent section name
    Verify:
        - OPSectionNotFoundException is raised
    """

    item_name = "Example Login Item 03"
    new_password = "new password"
    field_label = "password"
    section_label = "no-such-section"
    vault = "Test Data 2"
    with pytest.raises(OPSectionNotFoundException):
        signed_in_op.item_edit_set_password(item_name,
                                            new_password,
                                            field_label=field_label,
                                            section_label=section_label,
                                            insecure_operation=True,
                                            vault=vault)


@pytest.mark.usefixtures("setup_stateful_item_edit")
def test_item_edit_set_password_invalid_field_030(signed_in_op: OP):
    """
    Test: looking up an invalid field on a valid section
        - Attempt to call item_edit_set_password()
        - Pass a valid section name
        - Pass an invalid field name
    Verify:
        - OPFieldNotFoundException is raised
    """

    item_name = "Example Login Item 03"
    new_password = "new password"
    field_label = "no-such-password-field"
    section_label = "Example Section"
    vault = "Test Data 2"

    with pytest.raises(OPFieldNotFoundException):
        # This excercises a different code path from looking up a field
        # with no section specified
        signed_in_op.item_edit_set_password(item_name,
                                            new_password,
                                            field_label=field_label,
                                            section_label=section_label,
                                            insecure_operation=True,
                                            vault=vault)


@pytest.mark.usefixtures("setup_stateful_item_edit")
def test_item_edit_set_password_invalid_field_040(signed_in_op: OP):
    """
    Test: looking up an invalid field with no section
        - Attempt to call item_edit_set_password()
        - Don't pass a section name
        - Pass an invalid field name
    Verify:
        - OPFieldNotFoundException is raised
    """

    item_name = "Example Login Item 03"
    new_password = "new password"
    field_label = "no-such-password-field"
    vault = "Test Data 2"

    with pytest.raises(OPFieldNotFoundException):
        # This specifies a different code path from looking up a field
        # associated with a specific section
        signed_in_op.item_edit_set_password(item_name,
                                            new_password,
                                            field_label=field_label,
                                            insecure_operation=True,
                                            vault=vault)


@pytest.mark.usefixtures("setup_stateful_item_edit")
def test_item_edit_set_text_field_omit_section_050(signed_in_op: OP):
    """
    Test: Exiting an item where the field exists and is assigned to a section,
          but omitting the section label
        - Attempt to call item_edit_set_text_field()
        - Pass a valid section label
        - Pass None for the section label

    Verify:
        - OPFieldNotFoundException is raised
    """

    item_name = "Example Login Item 12"
    field_label = "Text Field 01"
    new_field_value = "new text field value"
    vault = "Test Data 2"

    with pytest.raises(OPFieldNotFoundException):
        signed_in_op.item_edit_set_text_field(item_name,
                                              new_field_value,
                                              field_label,
                                              section_label=None,
                                              vault=vault)


@pytest.mark.usefixtures("setup_stateful_item_edit")
def test_item_edit_set_mismatched_section_text_field_060(signed_in_op: OP):
    """
    Test: Exiting an item where the field exists and is assigned to a section,
          but omitting the section label
        - Attempt to call item_edit_set_text_field()
        - Pass a valid section label
        - Pass None for the section label
    Verify:
        - OPFieldNotFoundException is raised
    """

    item_name = "Example Login Item 16"
    field_label = "Text Field 01"
    section_label = "Section 02"
    new_field_value = "new text field value"
    vault = "Test Data 2"

    with pytest.raises(OPFieldNotFoundException):
        signed_in_op.item_edit_set_text_field(item_name,
                                              new_field_value,
                                              field_label,
                                              section_label=section_label,
                                              vault=vault)


@pytest.mark.usefixtures("setup_stateful_item_edit")
def test_item_edit_add_text_field_ambiguous_match_070(signed_in_op: OP):
    """
    Scenario:
    - adding a text field pairing when:
        - No section label is specified
        - Two matching text fields exist
        - Each text field belongs to a different section

    This should fail since ambiguous field match is an error when adding a field

    Test: OP.item_edit_add_text_field(),
        - Retrieve an item via OP.item_get()
        - Look up fields based on requested field label
        - Call item_edit_add_text_field(), saving returned object

    Verify:
        - The original item has at least one field matching the requested field label
        - Each matching field belongs to a section
        - OPFieldExistsException is raised during the item edit operation
    """
    item_name = "Example Login Item 19"
    field_label = "Ambiguous Field Match"
    new_field_value = "new text field value"
    vault = "Test Data 2"

    # stateful response directory
    # state 1: responses-item-edit/response-directory-1.json
    item_get_1 = signed_in_op.item_get(item_name, vault=vault)

    # item should have one or more matching fields
    try:
        fields = item_get_1.fields_by_label(field_label)
        for field in fields:
            # all fields should belong to a section
            assert field.section_id is not None
    except OPFieldNotFoundException:
        assert False, f"Item SHOULD have the field: {field_label}"

    with pytest.raises(OPFieldExistsException):
        signed_in_op.item_edit_add_text_field(item_name,
                                              new_field_value,
                                              field_label,
                                              vault=vault)


@pytest.mark.usefixtures("setup_stateful_item_edit")
def test_item_edit_add_text_field_exact_match_080(signed_in_op: OP):
    """
    Scenario:
    - adding a section/text field pairing when:
        - A matching section exists
        - A matching field exists
        - The text field belongs to the section

    This should fail since ambiguous field match is an error when adding a field

    Test: OP.item_edit_add_text_field(),
        - Retrieve an item via OP.item_get()
        - Look up fields based on requested field & section label
        - Call item_edit_add_text_field(), saving returned object

    Verify:
        - The original item has at least matching section
        - The section ias associated with one matching field
        - OPFieldExistsException is raised during the item edit operation
    """
    item_name = "Example Login Item 20"
    field_label = "Field 01"
    section_label = "Section 01"
    new_field_value = "new text field value"
    vault = "Test Data 2"

    # stateful response directory
    # state 1: responses-item-edit/response-directory-1.json
    item_get_1 = signed_in_op.item_get(item_name, vault=vault)

    # item should have a matching section and a matching field
    section = item_get_1.first_section_by_label(section_label)
    assert len(section.fields_by_label(field_label)) == 1

    with pytest.raises(OPFieldExistsException):
        signed_in_op.item_edit_add_text_field(item_name,
                                              new_field_value,
                                              field_label,
                                              section_label=section_label,
                                              vault=vault)


@pytest.mark.usefixtures("setup_stateful_item_edit")
def test_item_edit_add_password_no_insecure_acknowledge_090(signed_in_op: OP):
    """
    Test: OP.item_edit_set_password() raises OPInsecureOperationException appropriately
        - Attempt to call item_edit_set_password() without passing insecure_operation = True
    Verify:
        - OPInsecureOperationException is raised
    """

    item_name = "Example Login Item 18"
    field_label = "Password Field 01"
    section_label = "Section 01"
    new_field_value = "new password field value"
    vault = "Test Data 2"

    # item_edit_set_password() is inherently insecure, so
    # requires insecure_operation=True
    # This is expected to fail
    with pytest.raises(OPInsecureOperationException):
        signed_in_op.item_edit_set_password(item_name,
                                            new_field_value,
                                            field_label=field_label,
                                            section_label=section_label,
                                            vault=vault)
