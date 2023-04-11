from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..fixtures.valid_data import ValidData
    from ..fixtures.expected_vault_data import ExpectedVaultData


from pyonepassword.api.object_types import OPVault


def test_op_vault_010(valid_data: ValidData, expected_vault_data: ExpectedVaultData):
    expected = expected_vault_data.data_for_vault("Test Data")

    vault_dict = valid_data.data_for_name("example-vault-test-data")
    result = OPVault(vault_dict)

    assert isinstance(result, OPVault)
    assert result.unique_id == expected.unique_id


def test_op_vault_020(valid_data: ValidData, expected_vault_data: ExpectedVaultData):
    expected = expected_vault_data.data_for_vault("Test Data")

    vault_dict = valid_data.data_for_name("example-vault-test-data")
    result = OPVault(vault_dict)

    assert isinstance(result, OPVault)
    assert result.description == expected.description


def test_op_vault_030(valid_data: ValidData, expected_vault_data: ExpectedVaultData):
    expected = expected_vault_data.data_for_vault("Test Data")

    vault_dict = valid_data.data_for_name("example-vault-test-data")
    result = OPVault(vault_dict)

    assert isinstance(result, OPVault)
    assert result.item_count > 0
    assert result.item_count == expected.item_count


def test_op_vault_040(valid_data: ValidData, expected_vault_data: ExpectedVaultData):
    expected = expected_vault_data.data_for_vault("Test Data")

    vault_dict = valid_data.data_for_name("example-vault-test-data")
    result = OPVault(vault_dict)

    assert isinstance(result, OPVault)
    assert result.type == expected.type


def test_op_vault_050(valid_data: ValidData, expected_vault_data: ExpectedVaultData):
    expected = expected_vault_data.data_for_vault("Test Data")

    vault_dict = valid_data.data_for_name("example-vault-test-data")
    result = OPVault(vault_dict)

    assert isinstance(result, OPVault)
    assert result.created_at == expected.created_at


def test_op_vault_060(valid_data: ValidData, expected_vault_data: ExpectedVaultData):
    expected = expected_vault_data.data_for_vault("Test Data")

    vault_dict = valid_data.data_for_name("example-vault-test-data")
    result = OPVault(vault_dict)

    assert isinstance(result, OPVault)
    assert result.updated_at == expected.updated_at
