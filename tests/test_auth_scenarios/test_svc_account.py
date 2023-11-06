"""
Tests to excercise authentication paths that involve service accounts
"""

import pytest

from pyonepassword import OP
from pyonepassword.api.authentication import EXISTING_AUTH_REQD
from pyonepassword.api.exceptions import OPCmdFailedException


@pytest.mark.usefixtures("valid_op_cli_config_homedir")
@pytest.mark.usefixtures("setup_svc_acct_env")
def test_svc_acct_auth_010(console_logger):
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


@pytest.mark.usefixtures("valid_op_cli_config_homedir")
@pytest.mark.usefixtures("setup_stateful_svc_acct_auth")
def test_svc_account_not_yet_auth_020(console_logger):
    """
    In 'op' version >= 2.20.0, if a successful operation hasn't been completed in the past
    30 minutes, 'whoami' will fail with "not yet authenticated"

    Simulate a pyonepassword environment that has a service account token set
    via the OP_SERVICE_ACCOUNT_TOKEN environment variable

    Using a stateful response directory, simulate:
        - 'op whoami' failing with a "not yet authenticated" error
        - 'op item template list' triggering svc account authentication
        - 'op whoami' succeeding

    Verify that an OP() object can be instantiated

    NOTE: This test currently doesn't ensure that:
        - 'op whoami' fails the first itme
        - the 'op item template list' followed by a second 'op whoami' get executed
    """
    assert OP(op_path="mock-op", logger=console_logger,
              existing_auth=EXISTING_AUTH_REQD)
