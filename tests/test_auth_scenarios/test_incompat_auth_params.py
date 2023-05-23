"""
Module for testing incompatible authentication parameters, including:
- password argument passed in when service account token is set
- password passed in allong with existing_auth=EXISTING_AUTH_REQD
"""
import pytest

from pyonepassword import OP
from pyonepassword.api.authentication import EXISTING_AUTH_REQD
from pyonepassword.api.exceptions import OPAuthenticationException


@pytest.mark.usefixtures("valid_op_cli_config_homedir")
@pytest.mark.usefixtures("setup_svc_acct_env")
def test_password_incompat_svc_acct_010(console_logger):
    """
    Simulate an pyonepassword environment that has a service account token set
    via the OP_SERVICE_ACCOUNT_TOKEN environment variable

    Attempt to instantiate an OP object, passing in a 'password' argument

    Verify that OPAuthenticationException
    """
    password = "made-up-password"
    with pytest.raises(OPAuthenticationException):
        OP(op_path='mock-op', logger=console_logger, password=password)


@pytest.mark.usefixtures("valid_op_cli_config_homedir")
@pytest.mark.usefixtures("setup_normal_op_env")
def test_password_incompat_auth_param_020(console_logger):
    """
    Attempt to instantiate an OP object with incompatible password and existing_auth arguments

    Verify that OPAuthenticationException
    """
    password = "made-up-password"
    with pytest.raises(OPAuthenticationException):
        OP(op_path='mock-op', logger=console_logger,
           password=password, existing_auth=EXISTING_AUTH_REQD)
