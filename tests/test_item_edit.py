from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from pyonepassword.api.object_types import OPPasswordRecipe

if TYPE_CHECKING:
    from pyonepassword import OP

    from .fixtures.expected_login import ExpectedLogin, ExpectedLoginItemData

# ensure HOME env variable is set, and there's a valid op config present
pytestmark = pytest.mark.usefixtures("valid_op_cli_config_homedir")


@pytest.mark.usefixtures("setup_stateful_item_edit")
def test_item_edit_010(signed_in_op: OP):

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
def test_item_edit_020(signed_in_op: OP, expected_login_item_data: ExpectedLoginItemData):

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
