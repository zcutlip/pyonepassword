from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pyonepassword import OP

    from ..fixtures.expected_item import ExpectedItemData
    from ..fixtures.expected_login import ExpectedLoginItemData

from pyonepassword.api.exceptions import OPItemGetException
from pyonepassword.api.object_types import OPLoginItem

# ensure HOME env variable is set, and there's a valid op config present
pytestmark = pytest.mark.usefixtures("valid_op_cli_config_homedir")


# TODO: All of the tests that were essentially just testing OPLoginItem have been moved
# to test_item_types/test_login_item.py
# what remains doesn't really fit there
# most of these remaining tests are kind of dumb and don't appear to test anything meaninful
# so what we need to do is:
# - figure out what if anything they were intended to test
# - update the tests to meaninfully test those things
# - move the tests to proper test modules
# - remove whatever tests that aren't meaningful


def test_item_get_login_password_01(signed_in_op: OP,
                                    expected_login_item_data: ExpectedLoginItemData):
    """
    Test:
        - get password from login item via item_get_password() convenience method
        - verify resulting password matches expected password
    """
    item_name = "Example Login 1"
    vault = "Test Data"
    expected = expected_login_item_data.data_for_login(item_name)
    result = signed_in_op.item_get_password(item_name, vault=vault)

    assert result == expected.password


def test_item_get_login_by_uuid_01(signed_in_op: OP, expected_login_item_data):
    # get item nok7367v4vbsfgg2fczwu4ei44
    item_uuid = "nok7367v4vbsfgg2fczwu4ei44"
    expected = expected_login_item_data.data_for_login(item_uuid)
    result = signed_in_op.item_get(item_uuid)
    assert isinstance(result, OPLoginItem)
    assert result.username == expected.username


def test_item_get_login_by_uuid_02(signed_in_op: OP, expected_login_item_data):
    # get item nok7367v4vbsfgg2fczwu4ei44
    item_uuid = "nok7367v4vbsfgg2fczwu4ei44"
    expected = expected_login_item_data.data_for_login(item_uuid)
    result = signed_in_op.item_get(item_uuid)
    assert isinstance(result, OPLoginItem)
    assert result.password == expected.password


def test_item_get_login_alt_vault_01(signed_in_op: OP, expected_login_item_data):
    # get item "Example Login" --vault "Test Data 2"
    item_name = "Example Login"
    vault = "Test Data 2"
    expected = expected_login_item_data.data_for_login(item_name)
    result: OPLoginItem = signed_in_op.item_get(item_name, vault=vault)
    assert isinstance(result, OPLoginItem)
    assert result.username == expected.username
    assert result.password == expected.password


def test_item_get_login_alt_vault_02(signed_in_op: OP, expected_login_item_data):
    # get item "Example Login" --vault "Test Data 2"
    item_name = "Example Login"
    vault = "Test Data 2"
    expected = expected_login_item_data.data_for_login(item_name)
    result: OPLoginItem = signed_in_op.item_get(item_name, vault=vault)
    assert isinstance(result, OPLoginItem)
    assert result.password == expected.password


def test_item_get_invalid_login_01(signed_in_op: OP, expected_item_data: ExpectedItemData):
    item_name = "Invalid Item"
    expected = expected_item_data.data_for_name(item_name)
    try:
        _ = signed_in_op.item_get(item_name)
        assert False, "We should have caught an exception"
    except OPItemGetException as e:
        print(e)
        print(e.err_output)
        assert e.returncode == expected["returncode"]
