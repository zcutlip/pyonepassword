import getpass
import os
import sys
parent_path = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)
if parent_path not in sys.path:
    sys.path.append(parent_path)

from pyonepassword import (  # noqa: E401
    OP,
    OPSigninException,
    OPGetItemException,
    OPNotFoundException
)


def do_signin():
    account_shorthand = "arbitrary_account_shorthand"
    # If you've already signed in at least once, you don't need to provide all
    # account details on future sign-ins. Just master password
    my_password = getpass.getpass(prompt="1Password master password:\n")
    return OP(account_shorthand, password=my_password)


if __name__ == "__main__":
    try:
        op = do_signin()
    except OPSigninException as opse:
        print("1Password sign-in failed.")
        print(opse.err_output)
        exit(opse.returncode)
    except OPNotFoundException as ope:
        print("Uh oh. Couldn't find 'op'")
        print(ope)
        exit(ope.errno)

    print("Signed in.")
    print("Looking up \"Example Login\"...")
    try:
        item_password = op.get_item_password("Example Login")
        print(item_password)
        print("")
        print("\"Example Login\" can also be looked up by its uuid")
        print("")
        print("Looking up uuid \"ykhsbhhv2vf6hn2u4qwblfrmg4\"...")
        item_password = op.get_item_password("ykhsbhhv2vf6hn2u4qwblfrmg4")
        print(item_password)
    except OPGetItemException as ope:
        print("1Password lookup failed: {}".format(ope))
        print(ope.err_output)
        exit(ope.returncode)
    except OPNotFoundException as ope:
        print("Uh oh. Couldn't find 'op'")
        print(ope)
        exit(ope.errno)
