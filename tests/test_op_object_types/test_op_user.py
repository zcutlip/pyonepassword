from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from ..fixtures.valid_data import ValidData
    from ..fixtures.expected_user_data import ExpectedUserData

from pyonepassword.api.exceptions import OPInvalidUserException
from pyonepassword.api.object_types import OPUser


def test_op_user_01(valid_data: ValidData, expected_user_data: ExpectedUserData):
    """
    Create:
        - OPUser object from "example-user"
    Verify:
        - unique_id property matches expected value
    """
    expected = expected_user_data.data_for_user("Example User")
    user_dict = valid_data.data_for_name("example-user")
    result = OPUser(user_dict)
    assert isinstance(result, OPUser)
    assert result.unique_id == expected.unique_id


def test_op_user_02(valid_data: ValidData, expected_user_data: ExpectedUserData):
    """
    Create:
        - OPUser object from "example-user"
    Verify:
        - name property matches expected value
    """
    expected = expected_user_data.data_for_user("Example User")
    user_dict = valid_data.data_for_name("example-user")
    result = OPUser(user_dict)
    assert isinstance(result, OPUser)
    assert result.name == expected.name


def test_op_user_03(valid_data: ValidData, expected_user_data: ExpectedUserData):
    """
    Create:
        - OPUser object from "example-user"
    Verify:
        - email property matches expected value
    """
    expected = expected_user_data.data_for_user("Example User")
    user_dict = valid_data.data_for_name("example-user")
    result = OPUser(user_dict)
    assert isinstance(result, OPUser)
    assert result.email == expected.email


def test_op_user_04(valid_data: ValidData, expected_user_data: ExpectedUserData):
    """
    Create:
        - OPUser object from "example-user"
    Verify:
        - updated_at property matches expected value
    """
    expected = expected_user_data.data_for_user("Example User")
    user_dict = valid_data.data_for_name("example-user")
    result = OPUser(user_dict)
    assert isinstance(result, OPUser)
    assert result.updated_at == expected.updated_at


def test_op_user_05(valid_data: ValidData, expected_user_data: ExpectedUserData):
    """
    Create:
        - OPUser object from "example-user"
    Verify:
        - created_at property matches expected value
    """
    expected = expected_user_data.data_for_user("Example User")
    user_dict = valid_data.data_for_name("example-user")
    result = OPUser(user_dict)
    assert isinstance(result, OPUser)
    assert result.created_at == expected.created_at


def test_op_user_06(valid_data: ValidData, expected_user_data: ExpectedUserData):
    """
    Create:
        - OPUser object from "example-user"
    Verify:
        - last_auth_at property matches expected value
    """
    expected = expected_user_data.data_for_user("Example User")
    user_dict = valid_data.data_for_name("example-user")
    result = OPUser(user_dict)
    assert isinstance(result, OPUser)
    assert result.last_auth_at == expected.last_auth_at


def test_op_user_07(valid_data: ValidData, expected_user_data: ExpectedUserData):
    """
    Create:
        - OPUser object from "example-user"
    Verify:
        - state property matches expected value
    """
    expected = expected_user_data.data_for_user("Example User")
    user_dict = valid_data.data_for_name("example-user")
    result = OPUser(user_dict)
    assert isinstance(result, OPUser)
    assert result.state == expected.state


def test_op_user_08(valid_data: ValidData, expected_user_data: ExpectedUserData):
    """
    Create:
        - OPUser object from "example-user"
    Verify:
        - type property matches expected value
    """
    expected = expected_user_data.data_for_user("Example User")
    user_dict = valid_data.data_for_name("example-user")
    result = OPUser(user_dict)
    assert isinstance(result, OPUser)
    assert result.type == expected.type


def test_op_user_malformed_json_01(invalid_data):
    """
    Attempt to create OPUser object from malformed group JSON

    Verify:
        OPInvalidUserException is raised
    """
    malformed_json = invalid_data.data_for_name("malformed-user-json")
    with pytest.raises(OPInvalidUserException):
        OPUser(malformed_json)
