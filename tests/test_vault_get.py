from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pyonepassword import OP
    from .fixtures.expected_vault_data import (
        ExpectedVaultData,
        ExpectedVault
    )

from pyonepassword.api.exceptions import (
    OPInvalidVaultException,
    OPVaultGetException
)
from pyonepassword.api.object_types import OPVault

# ensure HOME env variable is set, and there's a valid op config present
pytestmark = pytest.mark.usefixtures("valid_op_cli_config_homedir")


def test_vault_get_01(signed_in_op: OP, expected_vault_data: ExpectedVaultData):
    # get vault "Test Data"
    expected: ExpectedVault
    result: OPVault

    vault_name = "Test Data"
    expected = expected_vault_data.data_for_vault(vault_name)
    result = signed_in_op.vault_get(vault_name)

    assert isinstance(result, OPVault)
    assert result.unique_id == expected.unique_id


def test_vault_get_02(signed_in_op: OP, expected_vault_data: ExpectedVaultData):
    # get vault "Test Data"
    expected: ExpectedVault
    result: OPVault

    vault_name = "Test Data"
    expected = expected_vault_data.data_for_vault(vault_name)
    result = signed_in_op.vault_get(vault_name)
    assert isinstance(result, OPVault)
    assert result.description == expected.description


def test_vault_get_03(signed_in_op: OP, expected_vault_data: ExpectedVaultData):
    # get vault "Test Data"
    expected: ExpectedVault
    result: OPVault

    vault_name = "Test Data"
    expected = expected_vault_data.data_for_vault(vault_name)
    result = signed_in_op.vault_get(vault_name)
    assert isinstance(result, OPVault)
    assert result.item_count > 0
    assert result.item_count == expected.item_count


def test_vault_get_04(signed_in_op: OP, expected_vault_data: ExpectedVaultData):
    # get vault "Test Data"
    expected: ExpectedVault
    result: OPVault

    vault_name = "Test Data"
    expected = expected_vault_data.data_for_vault(vault_name)
    result = signed_in_op.vault_get(vault_name)
    assert isinstance(result, OPVault)
    assert result.type == expected.type


def test_vault_get_05(signed_in_op: OP, expected_vault_data: ExpectedVaultData):
    # get vault "Test Data"
    expected: ExpectedVault
    result: OPVault

    vault_name = "Test Data"
    expected = expected_vault_data.data_for_vault(vault_name)
    result = signed_in_op.vault_get(vault_name)
    assert isinstance(result, OPVault)
    assert result.created_at == expected.created_at


def test_vault_get_06(signed_in_op: OP, expected_vault_data: ExpectedVaultData):
    # get vault "Test Data"
    expected: ExpectedVault
    result: OPVault

    vault_name = "Test Data"
    expected = expected_vault_data.data_for_vault(vault_name)
    result = signed_in_op.vault_get(vault_name)
    assert isinstance(result, OPVault)
    assert result.updated_at == expected.updated_at


def test_vault_get_07(signed_in_op: OP, expected_vault_data: ExpectedVaultData):
    expected: ExpectedVault
    result: OPVault

    vault_uuid = "yv7w5ijyxbdhxgh3njphwsxujy"
    expected = expected_vault_data.data_for_vault(vault_uuid)
    result = signed_in_op.vault_get(vault_uuid)
    assert isinstance(result, OPVault)
    assert result.unique_id == expected.unique_id


def test_vault_get_08(signed_in_op: OP, expected_vault_data: ExpectedVaultData):
    expected: ExpectedVault
    result: OPVault

    vault_uuid = "yv7w5ijyxbdhxgh3njphwsxujy"
    expected = expected_vault_data.data_for_vault(vault_uuid)
    result = signed_in_op.vault_get(vault_uuid)
    assert isinstance(result, OPVault)
    assert result.name == expected.name


def test_vault_get_09(signed_in_op: OP, expected_vault_data: ExpectedVaultData):
    expected: ExpectedVault
    result: OPVault

    vault_uuid = "yv7w5ijyxbdhxgh3njphwsxujy"
    expected = expected_vault_data.data_for_vault(vault_uuid)
    result = signed_in_op.vault_get(vault_uuid)
    assert isinstance(result, OPVault)
    assert result.description == expected.description


def test_vault_get_10(signed_in_op: OP, expected_vault_data: ExpectedVaultData):
    expected: ExpectedVault
    result: OPVault

    vault_uuid = "yv7w5ijyxbdhxgh3njphwsxujy"
    expected = expected_vault_data.data_for_vault(vault_uuid)
    result = signed_in_op.vault_get(vault_uuid)
    assert isinstance(result, OPVault)
    assert result.item_count > 0
    assert result.item_count == expected.item_count


def test_vault_get_11(signed_in_op: OP, expected_vault_data: ExpectedVaultData):
    expected: ExpectedVault
    result: OPVault

    vault_uuid = "yv7w5ijyxbdhxgh3njphwsxujy"
    expected = expected_vault_data.data_for_vault(vault_uuid)
    result = signed_in_op.vault_get(vault_uuid)
    assert isinstance(result, OPVault)
    assert result.type == expected.type


def test_vault_get_12(signed_in_op: OP, expected_vault_data: ExpectedVaultData):
    expected: ExpectedVault
    result: OPVault

    vault_uuid = "yv7w5ijyxbdhxgh3njphwsxujy"
    expected = expected_vault_data.data_for_vault(vault_uuid)
    result = signed_in_op.vault_get(vault_uuid)
    assert isinstance(result, OPVault)
    assert result.created_at == expected.created_at


def test_vault_get_13(signed_in_op: OP, expected_vault_data: ExpectedVaultData):
    expected: ExpectedVault
    result: OPVault

    vault_uuid = "yv7w5ijyxbdhxgh3njphwsxujy"
    expected = expected_vault_data.data_for_vault(vault_uuid)
    result = signed_in_op.vault_get(vault_uuid)
    assert isinstance(result, OPVault)
    assert result.updated_at == expected.updated_at


def test_vault_get_invalid_01(signed_in_op: OP, expected_vault_data):
    vault_name = "Invalid Vault"
    expected = expected_vault_data.data_for_vault(vault_name)
    try:
        _ = signed_in_op.vault_get(vault_name)
        assert False, "We should have caught an exception"
    except OPVaultGetException as e:
        print(e)
        assert e.returncode == expected.returncode


def test_vault_get_malformed_json_01(invalid_data):
    malformed_json = invalid_data.data_for_name("malformed-vault-json")
    with pytest.raises(OPInvalidVaultException):
        OPVault(malformed_json)
