from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from pyonepassword.api.object_types import (
    OPConcealedField,
    OPStringField,
    OPURLField
)
from pyonepassword.py_op_exceptions import OPPasswordFieldDowngradeException

if TYPE_CHECKING:
    from pyonepassword import OP
    from pyonepassword.api.object_types import OPAbstractItem

# ensure HOME env variable is set, and there's a valid op config present
pytestmark = pytest.mark.usefixtures("valid_op_cli_config_homedir")


def _get_field_value(item: OPAbstractItem, field_label: str, section_label: str = None):
    """
    Given a field label and optionally a section label, return the field's value
    """
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
def test_item_edit_set_text_field_012(signed_in_op: OP):
    """
    Test: password downgrade prevention
        - Call item_edit_set_text_field() on a field that is a concealed/password field
   Verify:
        - Field on unedited item is an instance of OPConcealedField
        - OPPasswordFieldDowngradeException is raised
    """

    item_name = "Example Login Item 14"
    field_label = "Password to Text 01"
    section_label = "Section 01"
    new_field_value = "new text field value"
    vault = "Test Data 2"

    # stateful response directory
    # state 1: responses-item-edit/response-directory-1.json
    item = signed_in_op.item_get(item_name, vault=vault)

    field = item.first_field_by_label(field_label)
    assert isinstance(field, OPConcealedField)

    with pytest.raises(OPPasswordFieldDowngradeException):
        signed_in_op.item_edit_set_text_field(item_name,
                                              new_field_value,
                                              field_label,
                                              section_label=section_label,
                                              vault=vault)


@pytest.mark.usefixtures("setup_stateful_item_edit")
def test_item_edit_set_text_field_015(signed_in_op: OP):
    """
    Test: OP.item_edit_set_url_field()
        - Retrieve an item via OP.item_get()
        - Call item_edit_set_text_field(), saving returned object
            - Set a field that is a concealed/password field
            - pass password_downgrade=True
            - save returned object
        - Retreive the same item a second time
    Verify:
        - OPPasswordFieldDowngradeException is NOT raised when item is edited
        - Field on unedited item is an instance of OPConcealedField
        - The original item field's value is not equal to the desired new value
        - The returned edited item field's value is the same as newly retrieved item field's value
        - The newly retrieved item's field is an instance of OPStringField
        - The edited item field's value is the same as newly retrieved item field's value
        - The newly retrieved item field's value is the same as the desired new value
    """

    item_name = "Example Login Item 14"
    field_label = "Password to Text 01"
    section_label = "Section 01"
    new_field_value = "new text field value"
    vault = "Test Data 2"

    # stateful response directory
    # state 1: responses-item-edit/response-directory-1.json
    item_get_1 = signed_in_op.item_get(item_name, vault=vault)

    section = item_get_1.first_section_by_label(section_label)
    field = section.first_field_by_label(field_label)
    # it's important that we're starting with a concealed field
    # because that's what triggers a downgrade exception
    assert isinstance(field, OPConcealedField)

    field_value = field.value
    assert field_value != new_field_value

    # OPPasswordFieldDowngradeException is NOT raised
    # because password_downgrade=True
    edited_item = signed_in_op.item_edit_set_text_field(item_name,
                                                        new_field_value,
                                                        field_label,
                                                        section_label=section_label,
                                                        vault=vault,
                                                        password_downgrade=True)

    # state changed with item_edit above
    # state 2: responses-item-edit/response-directory-2.json
    item_get_2 = signed_in_op.item_get(item_name, vault=vault)

    section = item_get_2.first_section_by_label(section_label)
    field = section.first_field_by_label(field_label)
    # verify
    assert isinstance(field, OPStringField)

    item_2_field_value = field.value

    edited_item_field_value = _get_field_value(
        edited_item, field_label, section_label=section_label)

    # ensure the field value in the item returned from the edit operation
    # matches the field value for the same item in a subsequent "item_get" operation
    assert edited_item_field_value == item_2_field_value

    # ensure the field value for the newly retrieved item matches the intended new field value
    assert item_2_field_value == new_field_value


@pytest.mark.usefixtures("setup_stateful_item_edit")
def test_item_edit_set_url_field_020(signed_in_op: OP):
    """
    Test: OP.item_edit_set_url_field()
        - Retrieve an item via OP.item_get()
        - Call item_edit_set_url_field(), saving returned object
        - Retreive the same item a second time

    Verify:
        - The original item field's value is not equal to the desired new value
        - The returned edited item field's value is the same as newly retrieved item field's value
        - The newly retrieved item field's value is the same as the desired new value

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


@pytest.mark.usefixtures("setup_stateful_item_edit")
def test_item_edit_set_url_field_030(signed_in_op: OP):
    """
    Test: OP.item_edit_set_url_field()
        - Retrieve an item via OP.item_get()
        - Look up the field to be changed based on section and field name
        - Call item_edit_set_url_field(), saving returned object
        - Retreive the same item a second time
    Verify:
        - The original item field is an instance of OPURLField
        - The original item field's value is not equal to the desired new value
        - The newly retrieved item field is an instance of OPURLField
        - The newly retrieved item field's value is the same as the desired new value
    """

    item_name = "Example Login Item 13"
    field_label = "URL Field 01"
    section_label = "Section 01"
    new_field_value = "https://new-url.com/login.html"
    vault = "Test Data 2"

    # stateful response directory
    # state 1: responses-item-edit/response-directory-1.json
    item = signed_in_op.item_get(item_name, vault=vault)
    section = item.first_section_by_label(section_label)
    field = section.first_field_by_label(field_label)

    # ensure the field is a URL field
    assert isinstance(field, OPURLField)

    # ensure the original field value is not the value we're trying to set
    assert field.value != new_field_value

    signed_in_op.item_edit_set_url_field(item_name,
                                         new_field_value,
                                         field_label,
                                         section_label=section_label,
                                         vault=vault)

    # state changed with item_edit above
    # state 2: responses-item-edit/response-directory-2.json
    item = signed_in_op.item_get(item_name, vault=vault)
    section = item.first_section_by_label(section_label)
    field = section.first_field_by_label(field_label)

    # ensure the field is still a URL field
    assert isinstance(field, OPURLField)

    # ensure the field value for the newly retrieved item matches the intended new field value
    assert field.value == new_field_value


@pytest.mark.usefixtures("setup_stateful_item_edit")
def test_item_edit_set_url_field_040(signed_in_op: OP):
    """
    Test: OP.item_edit_set_url_field()
        - Retrieve an item via OP.item_get()
        - Look up the field to be changed based on section and field name
        - Call item_edit_set_url_field(), saving returned object
        - Retreive the same item a second time
    Verify:
        - The original item field is an instance of OPStringField
        - The original item field's value is not equal to the desired new value
        - The newly retrieved item field has been chaned to an instance of OPURLField
        - The newly retrieved item field's value is the same as the desired new value
    """

    item_name = "Example Login Item 15"
    field_label = "Text field to be updated to URL 01"
    section_label = "Section 01"
    new_field_value = "https://new-url.com/login.html"
    vault = "Test Data 2"

    # stateful response directory
    # state 1: responses-item-edit/response-directory-1.json
    item = signed_in_op.item_get(item_name, vault=vault)
    section = item.first_section_by_label(section_label)
    field = section.first_field_by_label(field_label)

    # ensure the field is a string field, and more importantly NOT
    # a URL field
    assert isinstance(field, OPStringField)

    # ensure the original field value is not the value we're trying to set
    assert field.value != new_field_value

    signed_in_op.item_edit_set_url_field(item_name,
                                         new_field_value,
                                         field_label,
                                         section_label=section_label,
                                         vault=vault)

    # state changed with item_edit above
    # state 2: responses-item-edit/response-directory-2.json
    item = signed_in_op.item_get(item_name, vault=vault)
    section = item.first_section_by_label(section_label)
    field = section.first_field_by_label(field_label)

    # ensure the field has been changed to a URL field
    assert isinstance(field, OPURLField)

    # ensure the field value for the newly retrieved item matches the intended new field value
    assert field.value == new_field_value
