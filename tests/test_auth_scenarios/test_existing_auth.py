"""
Module for testing pyonepassword.api.authentication constants, including:
- use existing authenticaiton if available
- existing authentication is required
"""
from __future__ import annotations

import pytest

from pyonepassword import OP
from pyonepassword.api.authentication import (
    EXISTING_AUTH_AVAIL,
    EXISTING_AUTH_REQD
)
from pyonepassword.api.exceptions import OPAuthenticationException

# ensure HOME env variable is set, and there's a valid op config present
# pytestmark = pytest.mark.usefixtures("valid_op_cli_config_homedir")


@pytest.mark.usefixtures("valid_op_cli_config_homedir")
@pytest.mark.usefixtures("setup_unauth_op_env")
def test_use_existing_session_01():
    """
    Simulate an pyonepassword environment that doesn't use biometric auth, and doesn't have
    OP_SESSION_<session ID> env variable set
    check that OP() fails with OPNotSignedIn
    """
    with pytest.raises(OPAuthenticationException):
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
    with pytest.raises(OPAuthenticationException):
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
    with pytest.raises(OPAuthenticationException):
        OP(op_path='mock-op', existing_auth=EXISTING_AUTH_REQD,
           account="example_shorthand")
