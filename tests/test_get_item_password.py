from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pyonepassword import OP

from pyonepassword import OPPasswordItem


def _lookup_password_data(data, password_identifier: str):
    item = data.data_for_password(password_identifier)
    return item


def test_get_item_password_01(signed_in_op: OP, expected_item_password_data):
    password_identifier = "Example Password"
    vault = "Test Data"
    expected = _lookup_password_data(
        expected_item_password_data, password_identifier)
    result: OPPasswordItem = signed_in_op.get_item(
        password_identifier, vault=vault)
    assert isinstance(result, OPPasswordItem)
    assert result.password == expected.password
    assert result.uuid == expected.uuid
    assert result.title == expected.title
    assert result.created_at == expected.created_at
    assert result.updated_at == expected.updated_at
    assert result.changer_uuid == expected.changer_uuid
    assert result.vault_uuid == expected.vault_uuid
    assert result.trashed == expected.trashed
