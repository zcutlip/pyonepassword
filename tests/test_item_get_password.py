from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pyonepassword import OP

from pyonepassword.api.object_types import OPPasswordItem

# ensure HOME env variable is set, and there's a valid op config present
pytestmark = pytest.mark.usefixtures("valid_op_cli_config_homedir")


def _lookup_password_data(data, password_identifier: str):
    item = data.data_for_password(password_identifier)
    return item


def test_item_getpassword_01(signed_in_op: OP, expected_item_password_data):
    password_identifier = "Example Password"
    vault = "Test Data"
    expected = _lookup_password_data(
        expected_item_password_data, password_identifier)
    result: OPPasswordItem = signed_in_op.item_get(
        password_identifier, vault=vault)
    assert isinstance(result, OPPasswordItem)
    assert result.password == expected.password
    assert result.unique_id == expected.unique_id
    assert result.title == expected.title
    assert result.created_at == expected.created_at
    assert result.updated_at == expected.updated_at
    assert result.last_edited_by == expected.last_edited_by
    assert result.vault_id == expected.vault_id
