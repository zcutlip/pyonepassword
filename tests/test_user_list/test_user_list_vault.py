from __future__ import annotations

from typing import TYPE_CHECKING, List

import pytest

# make imports for type-hinting disappear at run-time to avoid
# circular imports.
# this also reduced exercising tested code simply by importing
if TYPE_CHECKING:
    from ..fixtures.expected_user_data import ExpectedUserListEntry, ExpectedUserListData
    from pyonepassword import OP

from pyonepassword import OPUserDescriptorList

# ensure HOME env variable is set, and there's a valid op config present
pytestmark = pytest.mark.usefixtures("valid_op_cli_config_homedir")


def _sanity_check_user_list(user_list, expected_list):
    assert isinstance(user_list, OPUserDescriptorList)
    assert len(user_list) > 0
    assert len(user_list) == len(expected_list)


def test_user_list_vault_test_data_01(signed_in_op: OP, expected_user_list_data: ExpectedUserListData):
    user_list_key = "vault-test-data"
    expected_user_list: List[ExpectedUserListEntry]
    expected_user_list = expected_user_list_data.data_for_key(user_list_key)
    expected = expected_user_list[0]
    result = signed_in_op.user_list(vault_name_or_id="Test Data")
    _sanity_check_user_list(result, expected_user_list)

    user_entry = result[0]
    assert user_entry.unique_id == expected.unique_id


def test_user_list_vault_test_data_02(signed_in_op: OP, expected_user_list_data: ExpectedUserListData):
    user_list_key = "vault-test-data"
    expected_user_list: List[ExpectedUserListEntry]
    expected_user_list = expected_user_list_data.data_for_key(user_list_key)
    expected = expected_user_list[0]
    result = signed_in_op.user_list(vault_name_or_id="Test Data")
    _sanity_check_user_list(result, expected_user_list)

    user_entry = result[0]
    assert user_entry.email == expected.email


def test_user_list_vault_test_data_03(signed_in_op: OP, expected_user_list_data: ExpectedUserListData):
    user_list_key = "vault-test-data"
    expected_user_list: List[ExpectedUserListEntry]
    expected_user_list = expected_user_list_data.data_for_key(user_list_key)
    expected = expected_user_list[0]
    result = signed_in_op.user_list(vault_name_or_id="Test Data")
    _sanity_check_user_list(result, expected_user_list)

    user_entry = result[0]
    assert user_entry.name == expected.name


def test_user_list_vault_test_data_04(signed_in_op: OP, expected_user_list_data: ExpectedUserListData):
    user_list_key = "vault-test-data"
    expected_user_list: List[ExpectedUserListEntry]
    expected_user_list = expected_user_list_data.data_for_key(user_list_key)
    expected = expected_user_list[0]
    result = signed_in_op.user_list(vault_name_or_id="Test Data")
    _sanity_check_user_list(result, expected_user_list)

    user_entry = result[0]
    assert user_entry.type == expected.type


def test_user_list_vault_test_data_05(signed_in_op: OP, expected_user_list_data: ExpectedUserListData):
    user_list_key = "vault-test-data"
    expected_user_list: List[ExpectedUserListEntry]
    expected_user_list = expected_user_list_data.data_for_key(user_list_key)
    expected = expected_user_list[0]
    result = signed_in_op.user_list(vault_name_or_id="Test Data")
    _sanity_check_user_list(result, expected_user_list)

    user_entry = result[0]
    assert user_entry.state == expected.state
