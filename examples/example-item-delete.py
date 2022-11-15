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
from pyonepassword.api.exceptions import OPItemDeleteException  # noqa: E402


def main():
    op: OP = do_signin()
    try:
        # op.item_delete() can take any identifier accepted by the 'op' command:
        # Usage:  op item delete [{ <itemName> | <itemID> | <shareLink> | - }] [flags]
        deleted_uuid = op.item_delete("Example Login")  # noqa: F841
        # if desired inspect resulting UUID to ensure it's what was
        # Expected
    except OPItemDeleteException as ope:
        # 'op' command can fail for a few reaons, including
        # - item not found
        # - duplicate item names
        # Inspect the error message from the command
        print(ope.err_output)
