from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from pyonepassword.api.exceptions import (
    OPFieldNotFoundException,
    OPSectionNotFoundException
)
from pyonepassword.py_op_exceptions import OPInsecureOperationException

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
