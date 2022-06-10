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
    OPNotSignedInException,
    OPSigninException
)


def do_signin():
    # Let's check If biometric is enabled
    # If so, no need to provide a password
    if OP.uses_biometric():
        try:
            # no need to provide any authentication parameters if biometric is enabled
            op = OP()
        except OPNotSignedInException:
            print("Uh oh! Sign-in failed")
            exit(-1)
    else:
        # prompt user for a password (or get it some other way)
        my_password = getpass.getpass(prompt="1Password master password:\n")
        # You may optionally provide an account shorthand if you used a custom one during initial sign-in
        # shorthand = "arbitrary_account_shorthand"
        # return OP(account_shorthand=shorthand, password=my_password)
        # Or we'll try to look up account shorthand from your latest sign-in in op's config file
        op = OP(password=my_password)
    return op


def signin_existing_session():
    # if you already have an existing session set, such as: eval $(op signin) in the terminal,
    #  you may use it here.
    #
    # password_prompt=False means to not let 'op' prompt interactively on the console for a password
    # if no session is found
    try:
        op = OP(use_existing_session=True, password_prompt=False)
    except OPNotSignedInException:
        print("Uh oh! Sign-in failed")
        exit(-1)
    return op


def signin_allow_op_prompt():
    # You can allow 'op' decide how to authenticate
    # if biometric is not available, it will prompt you interactively on the console

    # password_prompt defaults to True
    try:
        op = OP()
    except OPSigninException:
        print("Uh oh! Sign-in failed")
        exit(-1)

    return op


if __name__ == "__main__":
    do_signin()
    signin_existing_session()
    signin_allow_op_prompt()
