from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from ..fixtures.valid_data import ValidData

    from ..fixtures.expected_login import ExpectedLogin, ExpectedLoginItemData

from pyonepassword.api.object_types import OPLoginItem

# ensure HOME env variable is set, and there's a valid op config present
pytestmark = pytest.mark.usefixtures("valid_op_cli_config_homedir")


VALID_LOGIN_1 = "example-login-1"
VALID_LOGIN_2 = "example-login-2"


def test_item_get_login_01(valid_data: ValidData, expected_login_item_data: ExpectedLoginItemData):
    item_name = "Example Login 1"
    item_dict = valid_data.data_for_name(VALID_LOGIN_1)
    expected = expected_login_item_data.data_for_login(item_name)
    result = OPLoginItem(item_dict)

    assert result.username == expected.username


def test_item_get_login_02(valid_data: ValidData, expected_login_item_data):
    # get item "Example Login 1" --vault "Test Data"
    item_name = "Example Login 1"
    item_dict = valid_data.data_for_name(VALID_LOGIN_1)
    expected = expected_login_item_data.data_for_login(item_name)
    result = OPLoginItem(item_dict)

    assert result.password == expected.password


def test_item_get_login_03(valid_data: ValidData, expected_login_item_data):
    # get item "Example Login 1" --vault "Test Data"
    item_name = "Example Login 1"
    item_dict = valid_data.data_for_name(VALID_LOGIN_1)
    expected = expected_login_item_data.data_for_login(item_name)
    result = OPLoginItem(item_dict)

    assert result.primary_url.href == expected.primary_url.href


def test_item_get_login_04(valid_data: ValidData, expected_login_item_data):
    # get item "Example Login 1" --vault "Test Data"
    item_name = "Example Login 1"
    item_dict = valid_data.data_for_name(VALID_LOGIN_1)
    expected = expected_login_item_data.data_for_login(item_name)
    result = OPLoginItem(item_dict)

    assert result.primary_url.label == expected.primary_url.label


def test_item_get_login_05(valid_data: ValidData, expected_login_item_data):
    # get item "Example Login 1" --vault "Test Data"
    item_name = "Example Login 1"
    item_dict = valid_data.data_for_name(VALID_LOGIN_1)
    expected = expected_login_item_data.data_for_login(item_name)
    result = OPLoginItem(item_dict)

    assert result.primary_url.label == expected.primary_url.label


def test_item_get_login_06(valid_data: ValidData, expected_login_item_data):
    # get item "Example Login 1" --vault "Test Data"
    item_name = "Example Login 1"
    item_dict = valid_data.data_for_name(VALID_LOGIN_1)
    expected: ExpectedLogin = expected_login_item_data.data_for_login(
        item_name)
    result = OPLoginItem(item_dict)

    # "favorite" is true for Example Login 1
    assert result.favorite == expected.favorite


def test_item_get_login_07(valid_data: ValidData, expected_login_item_data):
    # get item "Example Login 1" --vault "Test Data"
    item_name = "Example Login 1"
    item_dict = valid_data.data_for_name(VALID_LOGIN_1)
    expected: ExpectedLogin = expected_login_item_data.data_for_login(
        item_name)
    result = OPLoginItem(item_dict)

    assert result.version == expected.version


# Example Login 2 has no URLs and favorite is not set

def test_login_item_08(valid_data: ValidData):
    item_dict = valid_data.data_for_name(VALID_LOGIN_2)
    result = OPLoginItem(item_dict)

    assert result.urls == []


def test_login_item_09(valid_data: ValidData):
    item_dict = valid_data.data_for_name(VALID_LOGIN_2)
    result = OPLoginItem(item_dict)

    assert result.primary_url is None


def test_login_item_10(valid_data: ValidData):
    item_dict = valid_data.data_for_name(VALID_LOGIN_2)
    result = OPLoginItem(item_dict)

    # "favorite" is unset for Example Login 2
    assert result.favorite is False
