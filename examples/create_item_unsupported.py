import getpass

from pyonepassword import OP
from pyonepassword.py_op_exceptions import (
    OPCreateItemNotSupportedException,
    OPNotSignedInException
)


def do_signin():
    # item creation unsupported on op version < 1.12.1
    op_path = "./op-binaries/op-1.11.4"
    try:
        op = OP(vault="Test Data", use_existing_session=True,
                password_prompt=False, op_path=op_path)
    except OPNotSignedInException:
        my_password = getpass.getpass(prompt="1Password master password:\n")
        op = OP(vault="Test Data", password=my_password, op_path=op_path)
    return op


def main():
    username = "testuser"
    password = "testpass"
    url = "https://example.website"
    item_name = "login 3"

    op = do_signin()
    if not op.supports_item_creation():
        print(
            f"pyonepassword does not support item creation with op version {op._cli_version}")

    try:
        op.create_login_item(item_name, username, password, url=url)
    except OPCreateItemNotSupportedException as e:
        print("Item creation failed")
        print(e)
        return -1

    print("Should not have reached here.")
    exit(1)


if __name__ == "__main__":
    exit(main())
