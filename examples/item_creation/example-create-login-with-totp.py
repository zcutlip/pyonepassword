import base64
import secrets
from pprint import pprint  # noqa: F401

from pyonepassword import OP
from pyonepassword.api.object_types import (
    OPLoginItem,
    OPNewLoginItem,
    OPTOTPField
)
from pyonepassword.op_items._new_fields import OPNewTOTPField, OPNewTOTPUri
from pyonepassword.op_items.password_recipe import (
    LETTERS_DIGITS_SYMBOLS_20,
    OPPasswordRecipe
)

if __name__ == "__main__":

    username = "test_username"
    title = "Test Login Item"

    op = OP()
    recipe = OPPasswordRecipe(length=40, digits=False, symbols=False)
    # or...
    recipe = LETTERS_DIGITS_SYMBOLS_20
    secret = secrets.token_bytes(10)
    secret = base64.b32encode(secret).decode()
    secret = secret.rstrip("=")

    issuer = "Example Website"
    account_name = "newuser@website"
    new_totp = "otpauth://totp/Example%20Website:newuser%40website?secret=EPW4UE4E7IKC2QMB&issuer=Example%20Website"
    # or...
    new_totp = OPNewTOTPUri(secret, account_name=account_name, issuer=issuer)
    print(str(new_totp))

    totp_field_label = "One-time Password"
    totp_field = OPNewTOTPField(totp_field_label, new_totp)

    new_item_template = OPNewLoginItem(
        "New Login with TOTP", account_name, fields=[totp_field])

    new_item: OPLoginItem = op.item_create(
        new_item_template, password_recipe=recipe, vault="Test Data")

    # pprint(new_item, indent=2)
    totp_field: OPTOTPField = new_item.first_field_by_label(totp_field_label)
    print(totp_field.totp_secret)
    print(totp_field.totp)
    # new_item_2 = op.login_item_create("New Login 2",
    #                                   "new_user_2",
    #                                   url="https://website.example",
    #                                   password="correct-horse-battery-staple",
    #                                   vault="Test Data")
    # pprint(new_item_2, indent=2)
