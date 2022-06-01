import os
import sys

from do_signin import do_signin

parent_path = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)
if parent_path not in sys.path:
    sys.path.append(parent_path)

from pyonepassword import (  # noqa: E402
    OPItemGetException,
    OPSigninException,
    OPSignoutException
)


def do_lookup():
    try:
        print(op.item_get_password("Example Login"))
    except OPItemGetException as opge:
        print("Get item failed.")
        print(opge.err_output)
        return opge.returncode


if __name__ == "__main__":
    try:
        op = do_signin(vault="Test Data")
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

    print("Trying to get item. This should fail.")
    do_lookup()

    print("Trying 'op forget'")
    try:
        op = do_signin(vault="Test Data")
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

    print("Trying to get item. This should fail")
    ret = do_lookup()

    print("Trying to re-signin")
    try:
        do_signin(vault="Test Data")
    except OPSigninException as opse:
        print("1Password sign-in failed.")
        print(opse.err_output)
