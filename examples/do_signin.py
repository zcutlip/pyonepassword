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


from pyonepassword import OP, OPNotSignedInException  # noqa: E402


def do_signin(vault=None, op_path="op"):
    # op_path = "op-binaries/2.0.0/op"
    uses_biometric = OP.uses_biometric(op_path=op_path)
    try:
        op = OP(vault=vault, op_path=op_path,
                use_existing_session=True, password_prompt=False)
    except OPNotSignedInException as e:
        if uses_biometric:
            raise e
        # If you've already signed in at least once, you don't need to provide all
        # account details on future sign-ins. Just master password
        my_password = getpass.getpass(prompt="1Password master password:\n")
        # You may optionally provide an account shorthand if you used a custom one during initial sign-in
        # shorthand = "arbitrary_account_shorthand"
        # return OP(account_shorthand=shorthand, password=my_password)
        # Or we'll try to look up account shorthand from your latest sign-in in op's config file
        op = OP(vault=vault, password=my_password, op_path=op_path)
    return op
