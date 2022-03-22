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
    OPNotFoundException,
    OPNotSignedInException,
    OPConfigNotFoundException
)


def do_signin():
    op_path = "op-binaries/1.12.4/op"
    try:
        op = OP(vault="Test Data", op_path=op_path,
                use_existing_session=True, password_prompt=False)
    except OPNotSignedInException:

        # If you've already signed in at least once, you don't need to provide all
        # account details on future sign-ins. Just master password
        my_password = getpass.getpass(prompt="1Password master password:\n")
        # You may optionally provide an account shorthand if you used a custom one during initial sign-in
        # shorthand = "arbitrary_account_shorthand"
        # return OP(account_shorthand=shorthand, password=my_password)
        # Or we'll try to look up account shorthand from your latest sign-in in op's config file
        op = OP(vault="Test Data", password=my_password, op_path=op_path)
    return op


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
    except OPConfigNotFoundException as ope:
        print("Didn't provide an account shorthand, and we couldn't locate 'op' config to look it up.")
        print(ope)
        exit(1)

    print("Signed in.")
    print("Looking up \"Example Login\"...")
    try:
        item_password = op.get_item_password("Example Login")
        print(item_password)
        print("")
        print("\"Example Login\" can also be looked up by its uuid")
        print("")
        print("Looking up uuid \"ubrjbhaixbexdglqfbe24nf2gu\"...")
        print("Overriding \"Test Data\" vault, and look in \"Test Data 2\" instead")
        item_password = op.get_item_password(
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
