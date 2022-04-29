# __future__.annotaitons, and typing.TYPE_CHECKING
# enable anything imported for type hinting to disappear at run time
from __future__ import annotations
from typing import TYPE_CHECKING

from .test_support.util import digest


# make imports for type-hinting disappear at run-time to avoid
# circular imports.
# this also reduced exercising tested code simply by importing
if TYPE_CHECKING:
    from .fixtures.expected_server import ExpectedServer, ExpectedServerSSHKeys
    from pyonepassword import OPServerItem, OP


def _lookup_ssh_key_data(expected_server_data, server_name, keyname) -> ExpectedServerSSHKeys:
    expected = expected_server_data.data_for_server(server_name)
    key_data = expected.ssh_keys_for_id(keyname)
    return key_data


def test_admin_user_01(signed_in_op: OP, expected_server_data: ExpectedServer):
    # get item "Example Login 1" --vault "Test Data"
    server_name = "Example Server"
    vault = "Test Data"
    expected = expected_server_data.data_for_server(server_name)
    result: OPServerItem = signed_in_op.item_get(server_name, vault=vault)
    assert result.username == expected.username


def test_admin_password_01(signed_in_op: OP, expected_server_data: ExpectedServer):
    server_name = "Example Server"
    vault = "Test Data"
    expected = expected_server_data.data_for_server(server_name)
    result: OPServerItem = signed_in_op.item_get(server_name, vault=vault)
    assert result.password == expected.password


def test_ssh_key_passphrase_01(signed_in_op: OP, expected_server_data: ExpectedServer):
    server_name = "Example Server"
    vault = "Test Data"
    keyname = "id_ed25519"
    passphrase_field = f"{keyname} passphrase"

    expected_key_data = _lookup_ssh_key_data(
        expected_server_data, server_name, keyname)

    server_item: OPServerItem = signed_in_op.item_get(server_name, vault=vault)

    passphrase = server_item.field_value_by_section_title(
        "SSH Keys", passphrase_field)
    assert passphrase == expected_key_data.passphrase


def test_ssh_priv_key_01(signed_in_op: OP, expected_server_data: ExpectedServer):
    server_name = "Example Server"
    vault = "Test Data"
    keyname = "id_ed25519"
    expected_key_data = _lookup_ssh_key_data(
        expected_server_data, server_name, keyname)
    server_item: OPServerItem = signed_in_op.item_get(server_name, vault=vault)

    priv_key = server_item.field_value_by_section_title(
        "SSH Keys", keyname)
    priv_key_digest = digest(priv_key.encode("utf-8"))
    assert priv_key_digest == expected_key_data.pivkey_digest


def test_ssh_pub_key_01(signed_in_op: OP, expected_server_data: ExpectedServer):
    server_name = "Example Server"
    vault = "Test Data"
    keyname = "id_ed25519"
    pub_keyname = f"{keyname}.pub"
    expected_key_data = _lookup_ssh_key_data(
        expected_server_data, server_name, keyname)
    server_item: OPServerItem = signed_in_op.item_get(server_name, vault=vault)

    pub_key = server_item.field_value_by_section_title(
        "SSH Keys", pub_keyname)
    pub_key_digest = digest(pub_key.encode("utf-8"))
    assert pub_key_digest == expected_key_data.pubkey_digest
