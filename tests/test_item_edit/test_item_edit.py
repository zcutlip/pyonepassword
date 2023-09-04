from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from pyonepassword.api.object_types import OPPasswordRecipe

if TYPE_CHECKING:
    from pyonepassword import OP
    from pyonepassword.api.object_types import OPLoginItem

    from ..fixtures.expected_login import ExpectedLogin, ExpectedLoginItemData

# ensure HOME env variable is set, and there's a valid op config present
pytestmark = pytest.mark.usefixtures("valid_op_cli_config_homedir")


def _get_item_password(item: OPLoginItem, field_label: str = "password", section_label: str = None):
    section = None
    if section_label:
        section = item.first_section_by_label(section_label)

    if section:
        field = section.first_field_by_label(field_label)
    else:
        field = item.first_field_by_label(field_label)

    password = field.value
    return password


@pytest.mark.usefixtures("setup_stateful_item_edit")
def test_item_edit_set_password_010(signed_in_op: OP):
    """
    Test: OP.item_edit_set_password()
        - Retrieve an item via OP.item_get()
        - Call item_edit_set_password(), saving returned object
        - Retreive the same item a second time

    Verify:
        - The original item's password is not equal to the desired new password
        - The returned edited item's password is the same as newly retrieved item's password
        - The newly retrieved item's password is the same as the desired new password

    """

    item_name = "Example Login Item 00"
    field_label = "password"
    new_password = "new password"
    vault = "Test Data 2"

    # stateful response directory
    # state 1: responses-item-edit/response-directory-1.json
    item_get_1 = signed_in_op.item_get(item_name, vault=vault)

    assert item_get_1.password != new_password

    edited_item = signed_in_op.item_edit_set_password(item_name,
                                                      new_password,
                                                      field_label=field_label,
                                                      insecure_operation=True,
                                                      vault=vault)

    # state changed with item_edit above
    # state 2: responses-item-edit/response-directory-2.json
    item_get_2 = signed_in_op.item_get(item_name, vault=vault)

    assert edited_item.password == item_get_2.password
    assert item_get_2.password == new_password


@pytest.mark.usefixtures("setup_stateful_item_edit")
def test_item_edit_set_password_015(signed_in_op: OP):
    """
    Test: OP.item_edit_set_password()
        - Retrieve an item via OP.item_get()
        - Call item_edit_set_password(), saving returned object
        - Retreive the same item a second time

    Verify:
        - The original item's password is not equal to the desired new password
        - The returned edited item's password is the same as newly retrieved item's password
        - The newly retrieved item's password is the same as the desired new password

    """

    item_name = "Example Login Item 03"
    section_label = "Example Section"
    field_label = "password in a section"
    new_password = "new password in a section"
    vault = "Test Data 2"

    # stateful response directory
    # state 1: responses-item-edit/response-directory-1.json
    item_get_1 = signed_in_op.item_get(item_name, vault=vault)

    item_get_password_1 = _get_item_password(
        item_get_1, field_label=field_label, section_label=section_label)

    assert item_get_password_1 != new_password

    edited_item = signed_in_op.item_edit_set_password(item_name,
                                                      new_password,
                                                      field_label=field_label,
                                                      section_label=section_label,
                                                      insecure_operation=True,
                                                      vault=vault)

    edited_item_password = _get_item_password(
        edited_item, field_label=field_label, section_label=section_label)

    # state changed with item_edit above
    # state 2: responses-item-edit/response-directory-2.json
    item_get_2 = signed_in_op.item_get(item_name, vault=vault)
    item_get_password_2 = _get_item_password(
        item_get_2, field_label=field_label, section_label=section_label)

    assert edited_item_password == item_get_password_2
    assert item_get_password_2 == new_password


@pytest.mark.usefixtures("setup_stateful_item_edit")
def test_item_edit_gen_password_020(signed_in_op: OP,
                                    expected_login_item_data: ExpectedLoginItemData):
    """
    Test: OP.item_edit_generate_password()
        - Retrieve an item via OP.item_get()
        - Call item_edit_generate_password(), saving returned object
        - Retreive the same item a second time

    Verify:
        - The original item's password matches the expected original password
        - The returned edited item's password is not the same as the original item's password
        - The newly retrieved item's password matches the expected edited item's password
    """
    item_name = "Example Login Item 01"
    vault = "Test Data 2"

    password_recipe = OPPasswordRecipe(20, symbols=False)

    # stateful response directory
    # state 1: responses-item-edit/response-directory-1.json
    expected_item_original: ExpectedLogin = expected_login_item_data.data_for_login(
        item_name)
    expected_item_edited: ExpectedLogin = expected_login_item_data.data_for_login(
        item_name, version=1)
    item_get_1 = signed_in_op.item_get(item_name, vault=vault)

    assert item_get_1.password == expected_item_original.password

    edited_item = signed_in_op.item_edit_generate_password(item_name,
                                                           password_recipe,
                                                           vault=vault)

    # state changed with item_edit above
    # state 2: responses-item-edit/response-directory-2.json
    item_get_2 = signed_in_op.item_get(item_name, vault=vault)

    assert edited_item.password != item_get_1.password
    assert item_get_2.password == expected_item_edited.password


@pytest.mark.usefixtures("setup_stateful_item_edit")
def test_item_edit_set_title_030(signed_in_op: OP):
    """
    Test: OP.item_edit_set_title()
        - Retrieve an item via OP.item_get() using the original title
        - Call item_edit_set_title(), saving returned object
        - Retreive the same item a second time using the new title

    Verify:
        - The original item's password matches the expected original password
        - The returned edited item's password is not the same as the original item's password
        - The newly retrieved item's password matches the expected edited item's password
    """
    item_name = "Example Login Item 02"
    item_name_new = "Example Login Item 02 (New Title)"
    vault = "Test Data 2"

    # stateful response directory
    # state 1: responses-item-edit/response-directory-1.json
    item_get_1 = signed_in_op.item_get(item_name, vault=vault)

    # sort of obvious since we retrieved using the old title, but for the sake of completeness
    assert item_get_1.title != item_name_new
    edited_item = signed_in_op.item_edit_set_title(
        item_name, item_name_new, vault=vault)

    # state changed with item_edit above
    # state 2: responses-item-edit/response-directory-2.json
    item_get_2 = signed_in_op.item_get(item_name_new, vault=vault)

    assert edited_item.title == item_get_2.title
    assert item_get_2.title == item_name_new


@pytest.mark.usefixtures("setup_stateful_item_edit")
def test_item_edit_set_favorite_040(signed_in_op: OP):
    """
    Test: OP.item_edit_set_favorite() setting favorite to True
        - Retrieve an item via OP.item_get()
        - Call item_edit_set_favorite(), saving returned object
        - Retreive the same item a second time

    Verify:
        - The original item's favorite flag is False
        - The returned edited item's favorite flag matches the newly retrieved item's favorite flag
        - The newly retrieved item's favorite flag is True
    """
    item_name = "Example Login Item 04"
    vault = "Test Data 2"

    # stateful response directory
    # state 1: responses-item-edit/response-directory-1.json
    item_get_1 = signed_in_op.item_get(item_name, vault=vault)

    assert item_get_1.favorite is False

    edited_item = signed_in_op.item_edit_set_favorite(
        item_name, True, vault=vault)

    # state changed with item_edit above
    # state 2: responses-item-edit/response-directory-2.json
    item_get_2 = signed_in_op.item_get(item_name, vault=vault)

    assert edited_item.favorite == item_get_2.favorite
    assert item_get_2.favorite is True


@pytest.mark.usefixtures("setup_stateful_item_edit")
def test_item_edit_set_favorite_050(signed_in_op: OP):
    """
    Test: OP.item_edit_set_favorite() setting favorite to False
        - Retrieve an item via OP.item_get()
        - Call item_edit_set_favorite(), saving returned object
        - Retreive the same item a second time

    Verify:
        - The original item's favorite flag is True
        - The returned edited item's favorite flag matches the newly retrieved item's favorite flag
        - The newly retrieved item's favorite flag is False
    """
    item_name = "Example Login Item 05"
    vault = "Test Data 2"

    # stateful response directory
    # state 1: responses-item-edit/response-directory-1.json
    item_get_1 = signed_in_op.item_get(item_name, vault=vault)

    assert item_get_1.favorite is True

    edited_item = signed_in_op.item_edit_set_favorite(
        item_name, False, vault=vault)

    # state changed with item_edit above
    # state 2: responses-item-edit/response-directory-2.json
    item_get_2 = signed_in_op.item_get(item_name, vault=vault)

    assert edited_item.favorite == item_get_2.favorite
    assert item_get_2.favorite is False
