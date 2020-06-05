import getpass
import os
import sys
import errno

parent_path = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)
if parent_path not in sys.path:
    sys.path.append(parent_path)

from pyonepassword import (  # noqa: E401
    OP,
    OPSigninException,
    OPNotFoundException
)


def do_initial_signin():
    my_signin_address = input("1Password sign-in address:\n")
    my_email_address = input("1Password email address:\n")
    my_account_shorthand = input("Chosen shorthand for this account:\n")
    my_secret_key = getpass.getpass(prompt="1Password secret key:\n")
    my_password = getpass.getpass(prompt="1Password master password:\n")

    return OP(my_account_shorthand, signin_address=my_signin_address,
              email_address=my_email_address,
              secret_key=my_secret_key,
              password=my_password)


if __name__ == "__main__":
    try:
        op = do_initial_signin()
        print("Signed in.")
    except OPSigninException as ope:
        print("1Password initial signin failed: {}".format(ope))
        print(ope.err_output)
        exit(ope.returncode)
    except OPNotFoundException as opnf:
        print("Uh oh. Couldn't find 'op'")
        print(opnf)
        exit(errno.ENOENT)
