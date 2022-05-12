from __future__ import annotations

from typing import TYPE_CHECKING, List

import pytest

# make imports for type-hinting disappear at run-time to avoid
# circular imports.
# this also reduced exercising tested code simply by importing
if TYPE_CHECKING:
    from .fixtures.expected_user_data import ExpectedUserListEntry, ExpectedUserListData
    from pyonepassword import OP

from pyonepassword import OPInvalidUserListException, OPUserDescriptorList


def test_user_list_01(signed_in_op: OP, expected_user_list_data: ExpectedUserListData):
    user_list_key = "all-users"
    expected_user_list: List[ExpectedUserListEntry]
    expected_user_list = expected_user_list_data.data_for_key(user_list_key)
    expected = expected_user_list[0]
    result = signed_in_op.user_list()
    user_entry = result[0]

    assert user_entry.unique_id == expected.unique_id
    assert user_entry.email == expected.email
    assert user_entry.name == expected.name
    assert user_entry.type == expected.type
    assert user_entry.state == expected.state


def test_user_list_malformed_json_01(invalid_data):
    malformed_json = invalid_data.data_for_name("malformed-user-list-json")
    with pytest.raises(OPInvalidUserListException):
        OPUserDescriptorList(malformed_json)
