"""
Tests to excercise authentication paths that involve service accounts
"""

import pytest

from pyonepassword import OP
from pyonepassword.api.exceptions import OPCmdFailedException


@pytest.mark.usefixtures("valid_op_cli_config_homedir")
@pytest.mark.usefixtures("setup_svc_acct_env")
def test_svc_acct_auth_01(console_logger):
    """
    Simulate an pyonepassword environment that has a service account token set
    via the OP_SERVICE_ACCOUNT_TOKEN environment variable

    Check that an OP() object can be instantiated
    """

    try:
        OP(op_path='mock-op', logger=console_logger)
    except OPCmdFailedException as e:
        print(e.err_output)
        assert False, f"OP() raised an exception {e}"
