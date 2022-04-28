from __future__ import annotations
from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from pyonepassword import OP

from pyonepassword import OPGetVaultException


def _lookup_item_data(data, vault_id: str) -> Dict:
    item = data.data_for_vault(vault_id)
    return item


def test_get_vault_01(signed_in_op: OP, expected_vault_data):
    # get vault "Test Data"
    vault_name = "Test Data"
    expected = _lookup_item_data(expected_vault_data, vault_name)
    result = signed_in_op.vault_get(vault_name)
    assert result.unique_id == expected.unique_id
    assert result.description == expected.description


def test_get_vault_02(signed_in_op: OP, expected_vault_data):
    # get vault "jqnwwnagfbhe5h2ky6k3rm3peu"
    vault_uuid = "jqnwwnagfbhe5h2ky6k3rm3peu"
    expected = _lookup_item_data(expected_vault_data, vault_uuid)
    result = signed_in_op.vault_get(vault_uuid)
    assert result.name == expected.name
    assert result.description == expected.description


def test_get_invalid_vault_01(signed_in_op: OP, expected_vault_data):
    vault_name = "Invalid Vault"
    expected = _lookup_item_data(expected_vault_data, vault_name)
    try:
        _ = signed_in_op.vault_get(vault_name)
        assert False, "We should have caught an exception"
    except OPGetVaultException as e:
        print(e)
        assert e.returncode == expected.returncode
