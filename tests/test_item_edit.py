import pytest

from pyonepassword import OP

# ensure HOME env variable is set, and there's a valid op config present
pytestmark = pytest.mark.usefixtures("valid_op_cli_config_homedir")


@pytest.mark.usefixtures("setup_stateful_item_edit")
def test_item_edit_01(signed_in_op: OP):

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
