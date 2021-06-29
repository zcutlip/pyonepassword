from typing import Dict
from pyonepassword import OP, OPGetItemException
from pyonepassword import OPLoginItem
from .fixtures.expected_data import ExpectedData


def _lookup_item_data(data: ExpectedData, item_id: str) -> Dict:
    item = data.lookup_item(item_id)
    return item


def test_get_item_login_01(signed_in_op: OP, expected_data):
    # get item "Example Login 1" --vault "Test Data"
    item_name = "Example Login 1"
    vault = "Test Data"
    expected = _lookup_item_data(expected_data, item_name)
    result = signed_in_op.get_item(item_name, vault=vault)
    assert result.username == expected["username"]
    assert result.password == expected["password"]

def test_get_item_login_02(signed_in_op: OP, expected_data):
    # get item nok7367v4vbsfgg2fczwu4ei44
    item_uuid = "nok7367v4vbsfgg2fczwu4ei44"
    expected = _lookup_item_data(expected_data, item_uuid)
    result = signed_in_op.get_item(item_uuid)
    assert result.username == expected["username"]
    assert result.password == expected["password"]


def test_get_item_login_03(signed_in_op: OP, expected_data):
    # get item "Example Login" --vault "Test Data 2"
    item_name = "Example Login"
    vault = "Test Data 2"
    expected = _lookup_item_data(expected_data, item_name)
    result: OPLoginItem = signed_in_op.get_item(item_name, vault=vault)
    assert result.username == expected["username"]
    assert result.password == expected["password"]


def test_get_invalid_item_login_01(signed_in_op: OP, expected_data):
    item_name = "Invalid Item"
    expected = _lookup_item_data(expected_data, item_name)
    try:
        _ = signed_in_op.get_item(item_name)
        assert False, "We should have caught an exception"
    except OPGetItemException as e:
        print(e)
        assert e.returncode == expected["returncode"]
