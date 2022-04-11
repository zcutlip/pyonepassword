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

from pyonepassword import (  # noqa: E402
    OP,
    OPSigninException,
    OPGetItemException,
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
    except OPGetItemException as opge:
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

    print("Doing signout.")
    try:
        op.signout()
    except OPSignoutException as e:
        print("Signout failed.")
        print(e.err_output)
        exit(e.returncode)

    print("Trying to get item")
    do_lookup()

    print("Trying 'op forget'")
    try:
        op = do_signin()
    except OPSigninException as opse:
        print("1Password sign-in failed.")
        print(opse.err_output)
        exit(opse.returncode)

    print("Doing forget.")
    try:
        op.signout(forget=True)
    except OPSignoutException as e:
        print(e.err_output)
        exit(e.returncode)
    print("Done.")

    print("Trying to get item")
    ret = do_lookup()

    print("Trying to re-signin")
    try:
        do_signin()
    except OPSigninException as opse:
        print("1Password sign-in failed.")
        print(opse.err_output)
