import os
import sys

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
from pyonepassword.api.exceptions import (  # noqa: E402
    OPCmdMalformedSvcAcctTokenException
)

if __name__ == "__main__":
    # set service account tokent o something nonsense
    os.environ["OP_SERVICE_ACCOUNT_TOKEN"] = "invalid-toke"

    try:
        op = OP()
    except OPCmdMalformedSvcAcctTokenException as e:
        print(f"caught exception: {e}")
        print(f"op CLI error message: {e.err_output}")
