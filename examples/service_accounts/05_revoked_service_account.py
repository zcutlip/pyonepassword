import os
import sys
from pprint import pprint

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
from pyonepassword.api.exceptions import (  # noqa: E402
    OPRevokedSvcAcctTokenException
)


def do_pprint(obj):
    pprint(obj, sort_dicts=False, indent=2)


def do_signin():
    # load environment with OP_SERVICE_ACCOUNT_TOKEN
    env_revoked_service_account = os.path.join(parent_path, "tests", "config",
                                               "dot_env", "env_revoked_svc_account")
    dotenv.load_dotenv(env_revoked_service_account)
    # There should be no authentication prompt
    op = OP()
    return op


if __name__ == "__main__":
    # op object gets created with no problem
    op = do_signin()

    # subsequent operatons fail do to service account being revoked
    try:
        # vault_list with group_name_or_id= kwarg is not supported
        vault_list = op.vault_list()
    except OPRevokedSvcAcctTokenException as e:
        print(f"caught exception: {e}")
        print(f"op CLI error message: {e.err_output}")
