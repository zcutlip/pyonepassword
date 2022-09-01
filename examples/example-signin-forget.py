import getpass
import os
import sys

parent_path = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)
# isort: split
if parent_path not in sys.path:
    sys.path.append(parent_path)

from pyonepassword import OP  # noqa: E402
from pyonepassword.api.exceptions import (  # noqa: E402
    OPForgetException,
    OPItemGetException,
    OPSigninException,
    OPSignoutException
)


def do_signin():
    # If you've already signed in at least once, you don't need to provide all
    # account details on future sign-ins. Just master password
    my_password = getpass.getpass(prompt="1Password master password:\n")
    # You may optionally provide an account shorthand if you used a custom one during initial sign-in
    # shorthand = "arbitrary_account_shorthand"
    # return OP(account_shorthand=shorthand, password=my_password)
    # Or we'll try to look up account shorthand from your latest sign-in in op's config file
    return OP(vault="Test Data", password=my_password)


def do_lookup():
    try:
        print(op.item_get_password("Example Login"))
    except OPItemGetException as opge:
        print("Get item failed.")
        print(opge.err_output)
        return opge.returncode


if __name__ == "__main__":
    try:
        op = do_signin()
    except OPSigninException as opse:
        print("1Password sign-in failed.")
        print(opse.err_output)
        exit(opse.returncode)
    account_shorthand = op._account_shorthand
    print("Doing signout.")
    try:
        op.signout()
    except OPSignoutException as e:
        print("Signout failed.")
        print(e.err_output)
        exit(e.returncode)

    print("Forgetting account: {}.".format(account_shorthand))
    try:
        OP.forget(account_shorthand)
    except OPForgetException as e:
        print(e.err_output)
        exit(e.returncode)
    print("Done.")

    print("Trying to re-sign-in")
    try:
        do_signin()
    except OPSigninException as opse:
        print("1Password sign-in failed.")
        print(opse.err_output)
