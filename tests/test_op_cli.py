import pytest

from pyonepassword import OP
from pyonepassword.api.exceptions import (
    OPCLIPanicException,
    OPNotFoundException,
    OPSigninException
)


@pytest.mark.usefixtures("valid_op_cli_config_homedir")
def test_missing_op():
    with pytest.raises(OPNotFoundException):
        OP(op_path="no-such-op")


@pytest.mark.usefixtures("valid_op_cli_config_homedir")
@pytest.mark.usefixtures("setup_normal_op_env_signin_failure")
def test_signin_fail():
    with pytest.raises(OPSigninException):
        OP(op_path="mock-op")


@pytest.mark.usefixtures("valid_op_cli_config_homedir")
@pytest.mark.usefixtures("setup_svc_acct_corrupt_env")
def test_op_cli_crash(console_logger):
    expected_argv = ['mock-op', '--format', 'json', 'whoami']
    try:
        OP(op_path="mock-op", logger=console_logger)
        assert False, "Should have raised OPCLIPanicException"
    except OPCLIPanicException as e:
        assert expected_argv == e.argv
