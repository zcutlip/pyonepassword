from __future__ import annotations

import pytest

from pyonepassword import OP
from pyonepassword.api.authentication import (
    EXISTING_AUTH_AVAIL,
    EXISTING_AUTH_REQD
)
from pyonepassword.api.exceptions import (
    OPNotSignedInException,
    OPUnknownAccountException
)

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
    OP(op_path='mock-op', existing_auth=EXISTING_AUTH_AVAIL, password_prompt=False)


@pytest.mark.usefixtures("valid_op_cli_config_homedir")
@pytest.mark.usefixtures("setup_op_sess_var_unauth_env")
def test_use_existing_session_03():
    """
    Simulate a pyonepassword environment that:
    - doesn't use biometric
    - DOES have OP_SESSION_<user uuid> env variable set
    - session token not valid
    Tell OP to use an exsiting session if available, but don't provide a password

    Check that OP(use_existing_session=True) fails
    """
    with pytest.raises(OPNotSignedInException):
        _ = OP(op_path='mock-op', existing_auth=EXISTING_AUTH_AVAIL,
               account="example_shorthand", password_prompt=False)


@pytest.mark.usefixtures("valid_op_cli_config_no_shorthand")
@pytest.mark.usefixtures("setup_op_sess_var_alt_env")
def test_use_existing_session_04():
    """
    Simulate a pyonepassword environment that:
    - no "latest_signin" to infer account identifier from
    - doesn't use biometric
    - DOES have OP_SESSION_<user uuid> env variable set
    - session token is valid

    test that OP_SESSION environment variable name is inferred at set without providing shorthand
    """

    OP(op_path='mock-op', existing_auth=EXISTING_AUTH_AVAIL, password_prompt=False)


@pytest.mark.usefixtures("valid_op_cli_config_homedir")
@pytest.mark.usefixtures("setup_op_sess_var_unauth_env")
def test_use_existing_session_05():
    """
    Simulate a pyonepassword environment that:
    - doesn't use biometric
    - DOES have OP_SESSION_<user uuid> env variable set
    - session token not valid
    Tell OP it MUST use an existing session.
    Check that OP(use_existing_session=True) fails
    """
    with pytest.raises(OPNotSignedInException):
        OP(op_path='mock-op', existing_auth=EXISTING_AUTH_REQD,
           account="example_shorthand")


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


@pytest.mark.usefixtures("valid_op_cli_config_no_shorthand")
@pytest.mark.usefixtures("setup_no_bio_alt_op_env")
def test_no_bio_no_account_02(console_logger):
    """
    test the conditions:
      - biometric is not enabled
      - no password provided
    """
    with pytest.raises(OPNotSignedInException):
        OP(op_path='mock-op', password_prompt=False, logger=console_logger)


@pytest.mark.usefixtures("valid_op_cli_config_homedir")
@pytest.mark.usefixtures("setup_normal_op_env")
def test_uses_biometric_class_method_01(console_logger):
    """
    Test calling OP.uses_biometric() as a class method
    """

    assert OP.uses_biometric(op_path="mock-op")


@pytest.mark.usefixtures("valid_op_cli_config_homedir")
@pytest.mark.usefixtures("setup_normal_op_env")
def test_unknown_accound_identifier_01(console_logger):
    """
    Test calling OP.uses_biometric() as a class method
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
