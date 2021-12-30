import getpass

from pyonepassword import (
    OP,
    OPCreateItemException,
    OPLoginItem
)
from pyonepassword.py_op_exceptions import OPNotSignedInException


def do_signin():
    try:
        op = OP(vault="Test Data", use_existing_session=True,
                password_prompt=False)
    except OPNotSignedInException:
        my_password = getpass.getpass(prompt="1Password master password:\n")
        op = OP(vault="Test Data", password=my_password)
    return op


def main():
    username = "testuser"
    password = "testpass"
    url = "https://example.website"
    item_name = "login 3"
    # newlogin = OPLoginItemTemplate(username, password, )

    # user-visible section title is required
    # section name (not user visible) is optional and will be randomly generated if not provided
    # section = newlogin.add_section("New Section")

    # field name is not user visible
    # field label is user visible
    # section.add_field("example field name", "example value", "string", "example field label")

    op = do_signin()

    try:
        result: OPLoginItem = op.create_login_item(
            item_name, username, password, url=url)
    except OPCreateItemException as e:
        print("create_item() failed")
        print(e.err_output)
        return e.returncode
    print("Created item:")
    print(f"Username: {result.username}")
    print(f"Password: {result.password}")
    print(f"Item UUID: {result.uuid}")


if __name__ == "__main__":
    exit(main())
