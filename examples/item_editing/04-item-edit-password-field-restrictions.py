import sys

import dotenv

from pyonepassword import OP
from pyonepassword.api.object_types import OPLoginItem
from pyonepassword.py_op_exceptions import (  # these are intentionally not exported as API
    OPInsecureOperationException,
    OPPasswordFieldDowngradeException
)


def set_password_field(op: OP):
    """
    Demonstrate requirement to pass insecure_operation=True
    when assigning a new value to a password field
    """
    item = "Example Login Item 101"
    field_label = "password"
    field_value = "really great new password"
    vault = "Test Data 2"

    try:
        op.item_edit_set_password(item,
                                  field_value,
                                  field_label=field_label,
                                  vault=vault)
    except OPInsecureOperationException:
        # exception raised because we didn't pass insecure_operation=True
        pass

    # must acknowledge insecurity of passing password text as a CLI argument
    op.item_edit_set_password(item,
                              field_value,
                              field_label=field_label,
                              vault=vault,
                              insecure_operation=True)


def add_password_field(op: OP):
    """
    Demonstrate requirement to pass insecure_operation=True
    when adding a new password field
    """
    item_label = "Example Login Item 102"

    vault = "Test Data 2"
    item: OPLoginItem = op.item_get(item_label, vault=vault)
    orig_password = item.password

    field_label = "archived password 01"
    section_label = "Archived Passwords"

    # just as with setting existing password fields, when adding a password field
    # we must acknowledge insecurity of passing password text as a CLI argument
    op.item_edit_add_password_field(item_label,
                                    orig_password,
                                    field_label,
                                    section_label=section_label,
                                    vault=vault,
                                    insecure_operation=True)


def change_password_field_to_text(op: OP):
    """
    Demonstrate requirement to pass password_downgrade=True
    when converting a password field to another type of field
    """
    item_label = "Example Login Item 30"
    section_label = "Section 01"
    field_label = "Change me to Text"
    new_field_value = "No longer a password"
    vault = "Test Data 2"

    try:
        op.item_edit_set_text_field(item_label,
                                    new_field_value,
                                    field_label,
                                    section_label=section_label,
                                    vault=vault)
    except OPPasswordFieldDowngradeException as e:
        print(e)

    # We have to acknowledge downgrade and that this is not
    # an accidental unmasking of a password
    op.item_edit_set_text_field(item_label,
                                new_field_value,
                                field_label,
                                section_label=section_label,
                                vault=vault,
                                password_downgrade=True)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        dotenv.load_dotenv(sys.argv[1])
    # see README.md for sign-in process
    op: OP = OP()
    # set_password_field(op)
    # add_password_field(op)
    change_password_field_to_text(op)
