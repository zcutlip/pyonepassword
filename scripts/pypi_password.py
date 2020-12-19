#!/usr/bin/env python3

import getpass
import sys
import os
from argparse import ArgumentParser
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
    OPGetItemException
)


def do_signin():
    # If you've already signed in at least once, you don't need to provide all
    # account details on future sign-ins. Just master password
    my_password = getpass.getpass(
        prompt="1Password master password:\n", stream=sys.stderr)
    # You may optionally provide an account shorthand if you used a custom one during initial sign-in
    # shorthand = "arbitrary_account_shorthand"
    # return OP(account_shorthand=shorthand, password=my_password)
    # Or we'll try to look up account shorthand from your latest sign-in in op's config file
    return OP(password=my_password)


def pypi_parse_args(args):
    parser = ArgumentParser()
    parser.add_argument(
        "--pypi-item-name", help="Optional item name for PyPI login", default="PyPI")

    parsed = parser.parse_args(args)
    return parsed


def main():
    parsed = pypi_parse_args(sys.argv[1:])
    pypi_item_name = parsed.pypi_item_name
    try:
        op = do_signin()
    except OPSigninException as e:
        print("sign-in failed", file=sys.stderr)
        print(e.err_output, file=sys.stderr)
        exit(e.returncode)

    try:
        password = op.get_item_password(pypi_item_name)
        sys.stdout.write(password)
        sys.stdout.flush()
    except OPGetItemException as e:
        print("Failed to look up password", file=sys.stderr)
        print(e.err_output, file=sys.stderr)
        exit(e.returncode)


if __name__ == "__main__":
    exit(main())
