from __future__ import annotations

from typing import TYPE_CHECKING, Dict

import pytest

if TYPE_CHECKING:
    from pyonepassword import OP, OPLoginItem

from pyonepassword import OPItemGetException

from .fixtures.expected_data import ExpectedData

# ensure HOME env variable is set, and there's a valid op config present
pytestmark = pytest.mark.usefixtures("valid_op_cli_config_homedir")


def _lookup_item_data(data: ExpectedData, item_id: str) -> Dict:
    item = data.lookup_item(item_id)
    return item


def test_get_item_login_01(signed_in_op: OP, expected_login_item_data):
    # get item "Example Login 1" --vault "Test Data"
    item_name = "Example Login 1"
    vault = "Test Data"
    expected = expected_login_item_data.data_for_login(item_name)
    result = signed_in_op.item_get(item_name, vault=vault)
    assert result.username == expected.username
    assert result.password == expected.password
    assert result.primary_url.href == expected.primary_url.href
    assert result.primary_url.label == expected.primary_url.label


def test_get_item_login_02(signed_in_op: OP, expected_login_item_data):
    # get item nok7367v4vbsfgg2fczwu4ei44
    item_uuid = "nok7367v4vbsfgg2fczwu4ei44"
    expected = expected_login_item_data.data_for_login(item_uuid)
    result = signed_in_op.item_get(item_uuid)
    assert result.username == expected.username
    assert result.password == expected.password


def test_get_item_login_03(signed_in_op: OP, expected_login_item_data):
    # get item "Example Login" --vault "Test Data 2"
    item_name = "Example Login"
    vault = "Test Data 2"
    expected = expected_login_item_data.data_for_login(item_name)
    result: OPLoginItem = signed_in_op.item_get(item_name, vault=vault)
    assert result.username == expected.username
    assert result.password == expected.password


def test_get_invalid_item_login_01(signed_in_op: OP, expected_data):
    item_name = "Invalid Item"
    expected = _lookup_item_data(expected_data, item_name)
    try:
        _ = signed_in_op.item_get(item_name)
        assert False, "We should have caught an exception"
    except OPItemGetException as e:
        print(e)
        print(e.err_output)
        assert e.returncode == expected["returncode"]


def test_get_item_login_url_list_01(signed_in_op: OP, expected_login_item_data):
    item_name = "Example Login 1"
    vault = "Test Data"
    expected = expected_login_item_data.data_for_login(item_name)
    result: OPLoginItem = signed_in_op.item_get(item_name, vault=vault)
    url_list = result.urls
    url = url_list[0]
    assert url.primary
    assert url.href == expected.primary_url.href
    assert url.label == expected.primary_url.label
