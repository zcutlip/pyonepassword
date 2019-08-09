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

from pyonepassword import (
    OP,
    OPSigninException
)


def do_signin():
    # If you've already signed in at least once, you don't need to provide all
    # account details on future sign-ins. Just master password
    my_password = getpass.getpass(prompt="1Password master password:\n")
    try:
        op = OP(password=my_password)
    except OPSigninException as ope:
        print("1Password initial signin failed: {}".format(ope))
        print(ope.err_output)
        exit(1)
    return op


if __name__ == "__main__":
    op = do_signin()
    print("Signed in.")
    print("Looking up \"Example Login\"...")
    print(op.lookup("Example Login"))
    print("")
    print("\"Example Login\" can also be looked up by its uuid")
    print("")
    print("Looking up uuid \"ykhsbhhv2vf6hn2u4qwblfrmg4\"...")
    print(op.lookup("ykhsbhhv2vf6hn2u4qwblfrmg4"))
