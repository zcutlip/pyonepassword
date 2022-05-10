from __future__ import annotations

from typing import TYPE_CHECKING, List

from pyonepassword.op_objects import OPGroupDescriptor

# make imports for type-hinting disappear at run-time to avoid
# circular imports.
# this also reduced exercising tested code simply by importing
if TYPE_CHECKING:
    from pyonepassword import OP

from .fixtures.expected_group_data import ExpectedGroupListEntry, ExpectedGroupListData

from pyonepassword import OPGroupDescriptorList


def test_group_list_01(signed_in_op: OP, expected_group_list_data: ExpectedGroupListData):
    group_list_key = "all-groups"
    expected_group_list: List[ExpectedGroupListEntry]
    expected_group_list = expected_group_list_data.data_for_key(group_list_key)
    expected = expected_group_list[0]
    result = signed_in_op.group_list()
    group_entry = result[0]
    assert isinstance(result, OPGroupDescriptorList)
    assert isinstance(group_entry, OPGroupDescriptor)

    assert group_entry.unique_id == expected.unique_id
    assert group_entry.description == expected.description
    assert group_entry.state == expected.state
    assert group_entry.created_at == expected.created_at
