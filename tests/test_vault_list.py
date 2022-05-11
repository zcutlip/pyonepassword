from __future__ import annotations

from typing import TYPE_CHECKING, List

# make imports for type-hinting disappear at run-time to avoid
# circular imports.
# this also reduced exercising tested code simply by importing
if TYPE_CHECKING:
    from pyonepassword import OP

    from .fixtures.expected_vault_data import (
        ExpectedVaultListData,
        ExpectedVaultListEntry
    )

from pyonepassword import OPVaultDescriptorList


def test_vault_list_01(signed_in_op: OP, expected_vault_list_data: ExpectedVaultListData):
    expected: List[ExpectedVaultListEntry]
    result: OPVaultDescriptorList

    expected = expected_vault_list_data.data_for_key("all-vaults")
    result = signed_in_op.vault_list()
    assert isinstance(result, OPVaultDescriptorList)
    assert len(result) > 0
    assert len(result) == len(expected)
    result_ids = {vault_obj.unique_id for vault_obj in result}
    expected_ids = {entry.unique_id for entry in expected}
    assert result_ids == expected_ids
