from __future__ import annotations

import pytest

from pyonepassword import OP
from pyonepassword.api.exceptions import OPUnknownAccountException


@pytest.mark.usefixtures("valid_op_cli_config_homedir")
@pytest.mark.usefixtures("setup_alt_op_env")
def test_session_var_property_01(expected_misc_data):
    """
    OP_SESSION_<session ID> environment variable is set only if biometric auth is not enabled, so:
    - Simulate an pyonepassword environment that doesn't use biometric auth
    - Check that op.session_var gets set properly
    """
    expected_var_name = expected_misc_data.data_for_key("op-session-var")
    op = OP(op_path='mock-op', account="example_shorthand")
    assert op.session_var == expected_var_name


@pytest.mark.usefixtures("valid_op_cli_config_homedir")
@pytest.mark.usefixtures("setup_normal_op_env")
def test_unknown_account_identifier_01(console_logger):
    """
    Simulate signing in with a non-existent account

    Verify:
        - OPUnknownAccountException is raised
    """
    unknown_account = "made-up-account"
    with pytest.raises(OPUnknownAccountException):
        OP(op_path="mock-op", account=unknown_account)


@pytest.mark.usefixtures("valid_op_cli_config_no_account_list")
@pytest.mark.usefixtures("setup_normal_op_env")
def test_op_sign_in_no_account_list_01():
    """
    Simulate an environment that:
      - has biometric enabled
      - op config's "accounts" is null
    Verify:
      - OP() doesn't raise an exception
    """
    try:
        OP(op_path="mock-op")
    except Exception as e:
        assert False, f"OP() raised an exception {e}"
