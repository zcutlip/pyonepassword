from __future__ import annotations

import pytest

from pyonepassword import OP
from pyonepassword.api.authentication import EXISTING_AUTH_AVAIL
from pyonepassword.api.exceptions import OPNotSignedInException

# ensure HOME env variable is set, and there's a valid op config present
# pytestmark = pytest.mark.usefixtures("valid_op_cli_config_homedir")


@pytest.mark.usefixtures("valid_op_cli_config_homedir")
@pytest.mark.usefixtures("setup_alt_op_env")
def test_uses_bio_property_01():
    """
    simulate an pyonepassword environment that doesn't use biometric auth
    check that op.uses_bio is False
    """
    op = OP(op_path='mock-op', account="example_shorthand")
    assert not op._uses_bio


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
@pytest.mark.usefixtures("setup_unauth_op_env")
def test_use_existing_session_01():
    """
    Simulate an pyonepassword environment that doesn't use biometric auth, and doesn't have
    OP_SESSION_<session ID> env variable set
    check that OP() fails with OPNotSignedIn
    """
    with pytest.raises(OPNotSignedInException):
        OP(op_path='mock-op', existing_auth=EXISTING_AUTH_AVAIL, password_prompt=False)


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
    _ = OP(op_path='mock-op', existing_auth=EXISTING_AUTH_AVAIL,
           password_prompt=False)


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
    with pytest.raises(OPNotSignedInException):
        _ = OP(op_path='mock-op', existing_auth=EXISTING_AUTH_AVAIL,
               account="example_shorthand", password_prompt=False)


@pytest.mark.usefixtures("valid_op_cli_config_no_shorthand")
@pytest.mark.usefixtures("setup_no_bio_alt_op_env")
def test_no_bio_no_account_01(console_logger):
    """
    test the conditions:
      - biometric is not enabled
      - no account identifier provided during sign-in
      - no "latest_signin" to infer account identifier from
    """

    OP(op_path='mock-op', password="made-up-password", logger=console_logger)


@pytest.mark.usefixtures("valid_op_cli_config_homedir")
@pytest.mark.usefixtures("setup_normal_op_env")
def test_uses_biometric_class_method_01(console_logger):
    """
    Test calling OP.uses_biometric() as a class method
    """

    assert OP.uses_biometric(op_path="mock-op")
