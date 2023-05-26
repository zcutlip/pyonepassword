import os
import sys

import dotenv

# hack to add pyonepassword project directory to search path
parent_path = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

if parent_path not in sys.path:
    # insert at front of search path to
    # ensure it preempts an already-installed version
    sys.path.insert(0, parent_path)

# isort: split
from pyonepassword import OP  # noqa: E402
from pyonepassword.api.exceptions import \
    OPSvcAcctCommandNotSupportedException  # noqa: E402


def do_signin():
    # load environment with OP_SERVICE_ACCOUNT_TOKEN
    dotenv.load_dotenv("./.env_secret")
    # There should be no authentication prompt
    op = OP()
    return op


if __name__ == "__main__":
    op = do_signin()

    # item get succeeds if we provide vault= kwarg
    item = op.item_get("Example Login 1", vault="Test Data")

    try:
        # fails if we leave out vault, since 'op item get' requires a vault
        # when a service account is in use
        item = op.item_get("Example Login 1")
    except OPSvcAcctCommandNotSupportedException as e:
        print(f"caught exception: {e}")
