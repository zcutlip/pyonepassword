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
    OPConfigNotFoundException,
    OPGetItemException,
    OPNotFoundException,
    OPSigninException
)
from pyonepassword.py_op_exceptions import OPCmdFailedException  # noqa: E402


if __name__ == "__main__":
    try:
        op = do_signin(vault="Test Data")
    except OPSigninException as opse:
        print("1Password sign-in failed.")
        print(opse.err_output)
        exit(opse.returncode)
    except OPNotFoundException as ope:
        print("Uh oh. Couldn't find 'op'")
        print(ope)
        exit(ope.errno)
    except OPConfigNotFoundException as ope:
        print("Didn't provide an account shorthand, and we couldn't locate 'op' config to look it up.")
        print(ope)
        exit(1)
    except OPCmdFailedException as ope:
        print(ope.err_output)
        exit(ope.returncode)

    print("Signed in.")
    print("Looking up \"Example Login\"...")
    try:
        item_password = op.item_get_password("Example Login")
        print(item_password)
        print("")
        print("\"Example Login\" can also be looked up by its uuid")
        print("")
        print("Looking up uuid \"ubrjbhaixbexdglqfbe24nf2gu\"...")
        print("Overriding \"Test Data\" vault, and look in \"Test Data 2\" instead")
        item_password = op.item_get_password(
            "ubrjbhaixbexdglqfbe24nf2gu", vault="Test Data 2")
        print(item_password)
    except OPGetItemException as ope:
        print("1Password lookup failed: {}".format(ope))
        print(ope.err_output)
        exit(ope.returncode)
    except OPNotFoundException as ope:
        print("Uh oh. Couldn't find 'op'")
        print(ope)
        exit(ope.errno)
