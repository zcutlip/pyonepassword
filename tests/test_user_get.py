from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pyonepassword import OP

from pyonepassword import OPGetUserException, OPInvalidUserException, OPUser

# ensure HOME env variable is set, and there's a valid op config present
pytestmark = pytest.mark.usefixtures("valid_op_cli_config_homedir")


def _lookup_user_data(data, user_identifier: str):
    item = data.data_for_user(user_identifier)
    return item


def test_get_user_01(signed_in_op: OP, expected_user_data):
    # get vault "Test Data"
    user_identifier = "Example User"
    expected = _lookup_user_data(expected_user_data, user_identifier)
    result = signed_in_op.user_get(user_identifier)
    assert isinstance(result, OPUser)
    assert result.unique_id == expected.unique_id


def test_get_user_02(signed_in_op: OP, expected_user_data):
    # get vault "Test Data"
    user_identifier = "Example User"
    expected = _lookup_user_data(expected_user_data, user_identifier)
    result = signed_in_op.user_get(user_identifier)
    assert isinstance(result, OPUser)
    assert result.name == expected.name


def test_get_user_03(signed_in_op: OP, expected_user_data):
    # get vault "Test Data"
    user_identifier = "Example User"
    expected = _lookup_user_data(expected_user_data, user_identifier)
    result = signed_in_op.user_get(user_identifier)
    assert isinstance(result, OPUser)
    assert result.email == expected.email


def test_get_user_04(signed_in_op: OP, expected_user_data):
    # get vault "Test Data"
    user_identifier = "Example User"
    expected = _lookup_user_data(expected_user_data, user_identifier)
    result = signed_in_op.user_get(user_identifier)
    assert isinstance(result, OPUser)
    assert result.updated_at == expected.updated_at


def test_get_user_05(signed_in_op: OP, expected_user_data):
    # get vault "Test Data"
    user_identifier = "Example User"
    expected = _lookup_user_data(expected_user_data, user_identifier)
    result = signed_in_op.user_get(user_identifier)
    assert isinstance(result, OPUser)
    assert result.created_at == expected.created_at


def test_get_user_06(signed_in_op: OP, expected_user_data):
    # get vault "Test Data"
    user_identifier = "Example User"
    expected = _lookup_user_data(expected_user_data, user_identifier)
    result = signed_in_op.user_get(user_identifier)
    assert isinstance(result, OPUser)
    assert result.last_auth_at == expected.last_auth_at


def test_get_user_07(signed_in_op: OP, expected_user_data):
    # get vault "Test Data"
    user_identifier = "Example User"
    expected = _lookup_user_data(expected_user_data, user_identifier)
    result = signed_in_op.user_get(user_identifier)
    assert isinstance(result, OPUser)
    assert result.state == expected.state


def test_get_user_08(signed_in_op: OP, expected_user_data):
    # get vault "Test Data"
    user_identifier = "Example User"
    expected = _lookup_user_data(expected_user_data, user_identifier)
    result = signed_in_op.user_get(user_identifier)
    assert isinstance(result, OPUser)
    assert result.type == expected.type


def test_get_invalid_user_01(signed_in_op: OP, expected_user_data):
    user_identifier = "No Such User"
    expected = _lookup_user_data(expected_user_data, user_identifier)
    try:
        signed_in_op.user_get(user_identifier)
        assert False, "We should have caught an OPGetUserException"
    except OPGetUserException as e:
        assert e.returncode == expected.returncode


def test_user_get_malformed_json_01(invalid_data):
    malformed_json = invalid_data.data_for_name("malformed-user-json")
    with pytest.raises(OPInvalidUserException):
        OPUser(malformed_json)
