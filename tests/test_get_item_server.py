from typing import Dict
from pyonepassword import OPServerItem, OP
from .fixtures.expected_data import ExpectedData
from .test_support.util import digest


def _lookup_item_data(data: ExpectedData, item_id: str) -> Dict:
    item = data.lookup_item(item_id)
    return item

def _lookup_ssh_key_data(data: ExpectedData, server_name, keyname) -> Dict:
    item = _lookup_item_data(data, server_name)
    all_keys = item["ssh_keys"]
    key_dict = all_keys[keyname]
    return key_dict

def test_admin_user_01(signed_in_op: OP, expected_data):
    # get item "Example Login 1" --vault "Test Data"
    server_name = "Example Server"
    vault = "Test Data"
    expected = _lookup_item_data(expected_data, server_name)
    result: OPServerItem = signed_in_op.get_item(server_name, vault=vault)
    assert result.username == expected["username"]

def test_admin_password_01(signed_in_op: OP, expected_data):
    server_name = "Example Server"
    vault = "Test Data"
    expected = _lookup_item_data(expected_data, server_name)
    result: OPServerItem = signed_in_op.get_item(server_name, vault=vault)
    assert result.password == expected["password"]


def test_ssh_key_passphrase_01(signed_in_op: OP, expected_data):
    server_name = "Example Server"
    vault = "Test Data"
    keyname = "id_ed25519"
    passphrase_field = f"{keyname} passphrase"
    expected_key_data = _lookup_ssh_key_data(expected_data, server_name, keyname)
    server_item: OPServerItem = signed_in_op.get_item(server_name, vault=vault)

    passphrase = server_item.field_value_by_section_title("SSH Keys", passphrase_field)
    assert passphrase == expected_key_data["passphrase"]


def test_ssh_priv_key_01(signed_in_op: OP, expected_data):
    server_name = "Example Server"
    vault = "Test Data"
    keyname = "id_ed25519"
    expected_key_data = _lookup_ssh_key_data(
        expected_data, server_name, keyname)
    server_item: OPServerItem = signed_in_op.get_item(server_name, vault=vault)

    priv_key = server_item.field_value_by_section_title(
        "SSH Keys", keyname)
    priv_key_digest = digest(priv_key.encode("utf-8"))
    assert priv_key_digest == expected_key_data["privkey_digest"]


def test_ssh_pub_key_01(signed_in_op: OP, expected_data):
    server_name = "Example Server"
    vault = "Test Data"
    keyname = "id_ed25519"
    pub_keyname = f"{keyname}.pub"
    expected_key_data = _lookup_ssh_key_data(
        expected_data, server_name, keyname)
    server_item: OPServerItem = signed_in_op.get_item(server_name, vault=vault)

    pub_key = server_item.field_value_by_section_title(
        "SSH Keys", pub_keyname)
    pub_key_digest = digest(pub_key.encode("utf-8"))
    assert pub_key_digest == expected_key_data["pubkey_digest"]
