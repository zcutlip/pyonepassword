from __future__ import annotations

from typing import TYPE_CHECKING, List

import pytest

# make imports for type-hinting disappear at run-time to avoid
# circular imports.
# this also reduced exercising tested code simply by importing
if TYPE_CHECKING:
    from pyonepassword import OP

    from ....fixtures.expected_vault_data import (
        ExpectedVaultListData,
        ExpectedVaultListEntry
    )

from pyonepassword.api.descriptor_types import (
    OPVaultDescriptor,
    OPVaultDescriptorList
)

pytestmark = pytest.mark.usefixtures("valid_op_cli_config_homedir")


def _sanity_check_vault_list(vault_list, expected_list):
    assert isinstance(vault_list, OPVaultDescriptorList)
    assert len(vault_list) > 0
    assert len(vault_list) == len(expected_list)


def _vault_entry_for_name_or_id(vault_list: OPVaultDescriptorList, identifier):
    # 'op vault list' doesn't guarantee a particular order, so our expected data may not be
    # sorted the same as the result data
    # so we need to comb over the result data to locate the object we want to test
    vault_entry = None
    for v in vault_list:
        if identifier in (v["id"], v["name"]):
            vault_entry = v
            break
    return vault_entry


def test_vault_list_all_vaults_01(signed_in_op: OP, expected_vault_list_data: ExpectedVaultListData):
    expected: List[ExpectedVaultListEntry]
    result: OPVaultDescriptorList
    expected = expected_vault_list_data.data_for_key("all-vaults")
    result = signed_in_op.vault_list()

    _sanity_check_vault_list(result, expected)

    result_ids = {vault_obj.unique_id for vault_obj in result}
    expected_ids = {entry.unique_id for entry in expected}
    assert result_ids == expected_ids


def test_vault_list_all_vaults_02(signed_in_op: OP, expected_vault_list_data: ExpectedVaultListData):
    expected: ExpectedVaultListEntry

    # just pick one expected data entry. doesn't matter which
    ARBITRARY_EXPECTED_IDX = 0

    expected_vault_list = expected_vault_list_data.data_for_key("all-vaults")
    expected = expected_vault_list[ARBITRARY_EXPECTED_IDX]

    # since we're testing vault_entry.unique_id property
    # let's instead use the expected 'name' value to locate the right vault
    # we'll flip it around when we test the name property
    identifier = expected.name

    result = signed_in_op.vault_list()
    _sanity_check_vault_list(result, expected_vault_list)
    vault_entry = _vault_entry_for_name_or_id(result, identifier)

    assert isinstance(vault_entry, OPVaultDescriptor)
    assert vault_entry.unique_id == expected.unique_id


def test_vault_list_all_vaults_03(signed_in_op: OP, expected_vault_list_data: ExpectedVaultListData):
    expected: ExpectedVaultListEntry

    # just pick one expected data entry. doesn't matter which
    ARBITRARY_EXPECTED_IDX = 2

    expected_vault_list = expected_vault_list_data.data_for_key("all-vaults")
    expected = expected_vault_list[ARBITRARY_EXPECTED_IDX]

    # since we're testing vault_entry.name property
    # let's instead use the expected 'id' value to locate the right vault
    identifier = expected.name

    result = signed_in_op.vault_list()
    _sanity_check_vault_list(result, expected_vault_list)
    vault_entry = _vault_entry_for_name_or_id(result, identifier)

    assert isinstance(vault_entry, OPVaultDescriptor)
    assert vault_entry.name == expected.name
