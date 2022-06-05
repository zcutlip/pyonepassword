from __future__ import annotations

import pytest

from pyonepassword import OP, OPNotSignedInException
from pyonepassword._op_cli_config import OPCLIConfig

# ensure HOME env variable is set, and there's a valid op config present
# pytestmark = pytest.mark.usefixtures("valid_op_cli_config_homedir")


@pytest.mark.usefixtures("valid_op_cli_config_homedir")
def test_get_account_shorthand_01(signed_in_op: OP):
    """
    - provide an standard 'op' config that has a "latest sign-in"
    - ensure _get_account_shorthand() gets the proper shorthand string
    """
    op_config = OPCLIConfig()
    shorthand = signed_in_op._get_account_shorthand(op_config)
    assert shorthand == "example_shorthand"


@pytest.mark.usefixtures("valid_op_cli_config_no_shorthand")
def test_get_account_shorthand_02(signed_in_op: OP):
    """
    - provide an standard 'op' config that does not have a "latest sign-in"
    - ensure _get_account_shorthand() returns None
    """
    op_config = OPCLIConfig()
    shorthand = signed_in_op._get_account_shorthand(op_config)
    assert shorthand is None


@pytest.mark.usefixtures("valid_op_cli_config_homedir")
@pytest.mark.usefixtures("setup_alt_op_env")
def test_uses_bio_property_01():
    """
    simulate an pyonepassword environment that doesn't use biometric auth
    check that op.uses_bio is False
    """
    op = OP(op_path='mock-op', account_shorthand="example_shorthand")
    assert not op.uses_bio


@pytest.mark.usefixtures("valid_op_cli_config_homedir")
@pytest.mark.usefixtures("setup_alt_op_env")
def test_session_var_property_01(expected_misc_data):
    """
    OP_SESSION_<session ID> environment variable is set only if biometric auth is not enabled, so:
    - Simulate an pyonepassword environment that doesn't use biometric auth
    - Check that op.session_var gets set properly
    """
    expected_var_name = expected_misc_data.data_for_key("op-session-var")
    op = OP(op_path='mock-op', account_shorthand="example_shorthand")
    assert op.session_var == expected_var_name


@pytest.mark.usefixtures("valid_op_cli_config_homedir")
@pytest.mark.usefixtures("setup_alt_op_env")
def test_use_existing_session_01():
    """
    Simulate an pyonepassword environment that doesn't use biometric auth, and doesn't have
    OP_SESSION_<session ID> env variable set
    check that OP() fails with OPNotSignedIn
    """
    with pytest.raises(OPNotSignedInException):
        OP(op_path='mock-op', use_existing_session=True, password_prompt=False)


@pytest.mark.usefixtures("valid_op_cli_config_homedir")
@pytest.mark.usefixtures("setup_op_sess_var_alt_env")
def test_use_existing_session_02():
    """
    Simulate a pyonepassword environment that:
    - doesn't use biometric
    - DOES have OP_SESSION_<user uuid> env variable set
    Check that OP(use_existing_session=True) succeeds
    """
    # with pytest.raises(OPNotSignedInException):
    _ = OP(op_path='mock-op', use_existing_session=True, password_prompt=False)


@pytest.mark.usefixtures("valid_op_cli_config_homedir")
@pytest.mark.usefixtures("setup_op_sess_var_unauth_env")
def test_use_existing_session_03():
    """
    Simulate a pyonepassword environment that:
    - doesn't use biometric
    - DOES have OP_SESSION_<user uuid> env variable set
    - session token not valid
    Check that OP(use_existing_session=True) fails
    """
    # with pytest.raises(OPNotSignedInException):
    _ = OP(op_path='mock-op', use_existing_session=True,
           account_shorthand="example_shorthand", password_prompt=False)


@pytest.mark.usefixtures("valid_op_cli_config_no_shorthand")
@pytest.mark.usefixtures("setup_alt_op_env")
def test_no_shorthand_no_bio_01():
    """
    If biometric is disabled, a shorthand is required, so:
    - Simulate an pyonepassword environment that doesn't use biometric auth
    - Provide a config that doesn't have a "latest sign-in", so no shorthand
    - Check that OP() fails with OPNotSignedInException
    """
    with pytest.raises(OPNotSignedInException):
        OP(op_path='mock-op')
