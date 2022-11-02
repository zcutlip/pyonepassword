from pyonepassword import OP
from pyonepassword.api.constants import LETTERS_DIGITS_SYMBOLS_20
from pyonepassword.api.object_types import (
    OPLoginItem,
    OPNewLoginItem,
    OPNewSection,
    OPNewStringField
)

from ..do_signin import do_signin


def main():
    # see README.md for sign-in process

    username = "test_username"
    title = "Test Login Item"
    login_url = "https://website.example"

    section_label = "Example Section"
    field_label = "Example Field"
    field_value = "Exampe field text."
    # Section ID will be randomly generated if not provided
    new_section = OPNewSection(section_label)

    # Field ID will be randomly generated if not provided
    # If section is provided, this field will be part of that section
    new_field = OPNewStringField(field_label, field_value, section=new_section)

    # add custom field and section to the new login item template
    item_template = OPNewLoginItem(title, username, url=login_url,
                                   sections=[new_section], fields=[new_field])

    op: OP = do_signin()
    recipe = LETTERS_DIGITS_SYMBOLS_20

    # Use generic 'item_create()' API to pass in an item template object
    new_item: OPLoginItem = op.item_create(
        item_template, password_recipe=recipe)
    return new_item


if __name__ == "__main__":
    main()
