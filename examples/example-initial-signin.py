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


def do_initial_signin():
    my_signin_address = input("1Password sign-in address:\n")
    my_email_address = input("1Password email address:\n")
    my_secret_key = getpass.getpass(prompt="1Password secret key:\n")
    my_password = getpass.getpass(prompt="1Password master password:\n")
    try:
        op = OP(signin_address=my_signin_address,
                email_address=my_email_address,
                secret_key=my_secret_key,
                password=my_password)
    except OPSigninException as ope:
        print("1Password initial signin failed: {}".format(ope))
        print(ope.err_output)
        exit(1)

    return op


if __name__ == "__main__":
    op = do_initial_signin()
    print("Signed in.")
