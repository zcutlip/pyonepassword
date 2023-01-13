#!/usr/bin/env python3

import getpass
import os
import sys
from argparse import ArgumentParser

# isort: split
parent_path = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if parent_path not in sys.path:
    sys.path.append(parent_path)

from pyonepassword import OP  # noqa: E402
from pyonepassword.api.authentication import (  # noqa: E402
    EXISTING_AUTH_AVAIL,
    EXISTING_AUTH_IGNORE
)
from pyonepassword.api.exceptions import (  # noqa: E402
    OPItemGetException,
    OPNotSignedInException,
    OPSigninException
)


def do_signin(vault=None, op_path="op", use_existing_session=False, account=None):
    auth = EXISTING_AUTH_IGNORE
    if use_existing_session:
        auth = EXISTING_AUTH_AVAIL
    # Let's check If biometric is enabled
    # If so, no need to provide a password
    uses_biometric = OP.uses_biometric(op_path=op_path)
    try:
        op = OP(vault=vault, op_path=op_path,
                existing_auth=auth, password_prompt=False, account=account)
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
        op = OP(vault=vault, password=my_password, op_path=op_path,
                use_existing_session=use_existing_session, account_shorthand=account)
    return op


def pypi_parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        "--pypi-item-name", help="Optional item name for PyPI login", default="PyPI API")
    parser.add_argument("--use-session", "-S",
                        help="Attempt to use an existing 'op' session. If unsuccessful master password will be requested.", action='store_true')
    parser.add_argument("--account", "-A",
                        help="1Password account to use. (See op signin --help, for valid identifiers")
    parsed = parser.parse_args()
    return parsed


def main():
    op: OP
    print(f"pyonepassword version {OP.version()}", file=sys.stderr)
    parsed = pypi_parse_args()
    pypi_item_name = parsed.pypi_item_name
    try:
        op = do_signin(use_existing_session=parsed.use_session,
                       account=parsed.account)
    except OPSigninException as e:
        print("sign-in failed", file=sys.stderr)
        print(e.err_output, file=sys.stderr)
        exit(e.returncode)

    try:
        op_item = op.item_get(pypi_item_name)
        if hasattr(op_item, "password"):
            password = op_item.password
        else:
            password = op_item.credential
        if os.isatty(sys.stdout.fileno()):
            end = None
        else:
            end = ''
        print(password, end=end)

    except OPItemGetException as e:
        print("Failed to look up password", file=sys.stderr)
        print(e.err_output, file=sys.stderr)
        exit(e.returncode)


if __name__ == "__main__":
    try:
        exit(main())
    except KeyboardInterrupt:
        exit(1)
