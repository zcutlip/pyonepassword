import getpass
import os
import sys

parent_path = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)
if parent_path not in sys.path:
    sys.path.insert(0, parent_path)

# isort: split
from pyonepassword import OP  # noqa: E402
from pyonepassword.api.authentication import (  # noqa: E402
    EXISTING_AUTH_AVAIL,
    EXISTING_AUTH_REQD
)
from pyonepassword.api.exceptions import \
    OPAuthenticationException  # noqa: E402


def do_signin(vault=None, op_path="op", existing_auth=EXISTING_AUTH_AVAIL, account=None, logger=None):
    # Let's check If biometric is enabled
    # If so, no need to provide a password
    uses_biometric = OP.uses_biometric(op_path=op_path)
    try:
        op = OP(vault=vault, op_path=op_path,
                existing_auth=existing_auth, password_prompt=False, account=account, logger=logger)
    except OPAuthenticationException as e:
        if uses_biometric or existing_auth == EXISTING_AUTH_REQD:
            raise e
        # If you've already signed in at least once, you don't need to provide all
        # account details on future sign-ins. Just master password
        my_password = getpass.getpass(prompt="1Password master password:\n")
        # You may optionally provide an account shorthand if you used a custom one during initial sign-in
        # shorthand = "arbitrary_account_shorthand"
        # return OP(account_shorthand=shorthand, password=my_password)
        # Or we'll try to look up account shorthand from your latest sign-in in op's config file
        op = OP(vault=vault, password=my_password, op_path=op_path,
                existing_auth=existing_auth, account=account)
    return op
