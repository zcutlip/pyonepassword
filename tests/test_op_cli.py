import os

import pytest

from pyonepassword import OP
from pyonepassword.api.exceptions import OPNotFoundException, OPSigninException

from .fixtures.paths import RESP_DIRECTORY_PATH


def test_missing_op():
    with pytest.raises(OPNotFoundException):
        OP(op_path="no-such-op")


def test_signin_fail():
    os.environ["MOCK_OP_RESPONSE_DIRECTORY"] = str(RESP_DIRECTORY_PATH)
    os.environ["LOG_OP_ERR"] = "1"
    os.environ["MOCK_OP_SIGNIN_SUCCEED"] = "0"
    with pytest.raises(OPSigninException):
        OP(op_path="mock-op")
