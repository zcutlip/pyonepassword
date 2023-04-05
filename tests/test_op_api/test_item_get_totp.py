# __future__.annotations, and typing.TYPE_CHECKING
# enable anything imported for type hinting to disappear at run time
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

# make imports for type-hinting disappear at run-time to avoid
# circular imports.
# this also reduced exercising tested code simply by importing
if TYPE_CHECKING:
    from ..fixtures.expected_totp_data import ExpectedTOTP, ExpectedTOTPData
    from pyonepassword import OP

from pyonepassword.api.exceptions import OPItemGetException
from pyonepassword.api.object_types import OPTOTPItem

# ensure HOME env variable is set, and there's a valid op config present
pytestmark = pytest.mark.usefixtures("valid_op_cli_config_homedir")


def test_item_get_totp_01(signed_in_op: OP, expected_totp_data: ExpectedTOTPData):
    login_name = "Login With TOTP"
    expected: ExpectedTOTP
    result: OPTOTPItem

    expected = expected_totp_data.totp_data_for_login(login_name)
    result = signed_in_op.item_get_totp(login_name, vault="Test Data")
    assert isinstance(result, OPTOTPItem)
    assert result.totp == expected.totp
    assert len(result.totp) == 6


def test_item_get_totp_02(signed_in_op: OP, expected_totp_data: ExpectedTOTPData):
    login_name = "Login With TOTP"
    expected: ExpectedTOTP
    result: OPTOTPItem

    expected = expected_totp_data.totp_data_for_login(login_name)
    result = signed_in_op.item_get_totp(login_name, vault="Test Data")
    assert isinstance(result, OPTOTPItem)
    assert result.unique_id == expected.unique_id


def test_item_get_totp_03(signed_in_op: OP, expected_totp_data: ExpectedTOTPData):
    login_name = "Login With TOTP"
    expected: ExpectedTOTP
    result: OPTOTPItem

    expected = expected_totp_data.totp_data_for_login(login_name)
    result = signed_in_op.item_get_totp(login_name, vault="Test Data")
    assert isinstance(result, OPTOTPItem)
    assert result.reference == expected.reference


def test_item_get_totp_04(signed_in_op: OP, expected_totp_data: ExpectedTOTPData):
    login_name = "Login With TOTP"
    expected: ExpectedTOTP
    result: OPTOTPItem

    expected = expected_totp_data.totp_data_for_login(login_name)
    result = signed_in_op.item_get_totp(login_name, vault="Test Data")
    assert isinstance(result, OPTOTPItem)
    assert result.value == expected.value


def test_item_get_totp_05(signed_in_op: OP, expected_totp_data: ExpectedTOTPData):
    login_name = "Login With TOTP"
    expected: ExpectedTOTP
    result: OPTOTPItem

    expected = expected_totp_data.totp_data_for_login(login_name)
    result = signed_in_op.item_get_totp(login_name, vault="Test Data")
    assert isinstance(result, OPTOTPItem)
    assert result.label == expected.label


def test_item_get_totp_invalid_01(signed_in_op: OP):
    login_name = "Invalid TOTP Login"
    vault = "Test Data"
    with pytest.raises(OPItemGetException):
        signed_in_op.item_get_totp(login_name, vault=vault)
