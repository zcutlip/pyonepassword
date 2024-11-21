import os
import sys

from do_signin import do_signin

parent_path = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)
# isort: split
if parent_path not in sys.path:
    sys.path.append(parent_path)

from pyonepassword import OP  # noqa: E402
from pyonepassword.api.exceptions import OPItemShareException  # noqa: E402


def main():
    op: OP = do_signin()
    try:
        # op.item_share() can take any identifier accepted by the 'op' command:
        # Usage:  op item share { <itemName> | <itemID> }
        share_url = op.item_share("Example Login Item 22", [], expires_in="2d")
        print(share_url)
    except OPItemShareException as ope:
        # 'op' command can fail for a few reaons, including
        # - item not found
        # - duplicate item names
        # - malformed emails or expiration duration
        # Inspect the error message from the command
        print(ope.err_output)


if __name__ == "__main__":
    main()
