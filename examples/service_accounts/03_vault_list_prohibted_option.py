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
from pyonepassword.api.exceptions import \
    OPSvcAcctCommandNotSupportedException  # noqa: E402


def do_pprint(obj):
    pprint(obj, sort_dicts=False, indent=2)
    print("")


def do_signin():
    # load environment with OP_SERVICE_ACCOUNT_TOKEN
    dotenv.load_dotenv("./.env_secret")
    # There should be no authentication prompt
    op = OP()
    return op


if __name__ == "__main__":
    op = do_signin()
    # vault_list on its own is pefectly fine
    vault_list = op.vault_list()
    print("Vault list:")
    do_pprint(vault_list)

    try:
        # vault_list with group_name_or_id= kwarg is not supported
        vault_list = op.vault_list(group_name_or_id="Team Members")
    except OPSvcAcctCommandNotSupportedException as e:
        print(f"caught exception: {e}")
