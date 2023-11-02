from pyonepassword import OP


def do_set_text_field(op: OP):
    item = "Example Login Item 103"
    section_label = "Section 01"
    field_label = "New Field 01"
    field_value = "new text for field 01 "
    vault = "Test Data 2"
    # item_edit_add_url_field() and item_edit_add_password_field() are similar
    op.item_edit_add_text_field(item,
                                field_value,
                                field_label,
                                section_label=section_label,
                                vault=vault)


if __name__ == "__main__":
    # see README.md for sign-in process
    op: OP = OP()
    do_set_text_field(op)
