import pytest

from pyonepassword import OP
from pyonepassword.api.exceptions import OPNotFoundException, OPSigninException


@pytest.mark.usefixtures("valid_op_cli_config_homedir")
def test_missing_op():
    with pytest.raises(OPNotFoundException):
        OP(op_path="no-such-op")


@pytest.mark.usefixtures("valid_op_cli_config_homedir")
@pytest.mark.usefixtures("setup_normal_op_env_signin_failure")
def test_signin_fail():
    with pytest.raises(OPSigninException):
        OP(op_path="mock-op")
