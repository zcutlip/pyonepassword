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


def totp_secret():
    # Normally the website/service provides this, but
    # we generate one for our example
    secret = secrets.token_bytes(10)
    secret = base64.b32encode(secret).decode()
    secret = secret.rstrip("=")
    return secret


def build_totp_uri():
    issuer = "Example Website"
    account_name = "newuser@website"
    secret = totp_secret()

    # If website/service provides fully-formed URI string
    new_totp_uri = "otpauth://totp/Example%20Website:newuser%40website?secret=EPW4UE4E7IKC2QMB&issuer=Example%20Website"

    # or for more sanity checking & proper encoding, create a OPNewTOTPUri object
    new_totp_uri = OPNewTOTPUri(
        secret, account_name=account_name, issuer=issuer)

    return new_totp_uri


def main():
    username = "test_username"
    title = "New Login with TOT"

    op = OP()
    recipe = OPPasswordRecipe(length=40, digits=False, symbols=False)
    # or...
    recipe = LETTERS_DIGITS_SYMBOLS_20

    new_totp_uri = build_totp_uri()
    totp_field_label = "One-time Password"
    totp_field = OPNewTOTPField(totp_field_label, new_totp_uri)

    new_item_template = OPNewLoginItem(title, username, fields=[totp_field])

    new_item: OPLoginItem = op.item_create(
        new_item_template, password_recipe=recipe, vault="Test Data")

    totp_field: OPTOTPField = new_item.first_field_by_label(totp_field_label)
    totp_code = totp_field.totp
    print(f"{totp_code}")


if __name__ == "__main__":
    main()
