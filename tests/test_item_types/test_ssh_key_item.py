# __future__.annotaitons, and typing.TYPE_CHECKING
# enable anything imported for type hinting to disappear at run time
from __future__ import annotations

from typing import TYPE_CHECKING

# make imports for type-hinting disappear at run-time to avoid
# circular imports.
# this also reduced exercising tested code simply by importing
if TYPE_CHECKING:
    from ..fixtures.expected_ssh_key_data import ExpectedSSHKeyData
    from ..fixtures.valid_data import ValidData

from pyonepassword.api.object_types import OPSSHKeyItem


def test_item_get_ssh_key_010(valid_data: ValidData, expected_ssh_key_data: ExpectedSSHKeyData):
    item_name = "Example SSH Key"
    item_dict = valid_data.data_for_name("example-ssh-key")

    expected = expected_ssh_key_data.data_for_ssh_key(item_name)
    result = OPSSHKeyItem(item_dict)
    assert result.unique_id == expected.unique_id


def test_item_get_ssh_key_020(valid_data: ValidData, expected_ssh_key_data: ExpectedSSHKeyData):
    item_name = "Example SSH Key"
    item_dict = valid_data.data_for_name("example-ssh-key")

    expected = expected_ssh_key_data.data_for_ssh_key(item_name)
    result = OPSSHKeyItem(item_dict)
    assert result.title == expected.title


def test_item_get_ssh_key_030(valid_data: ValidData, expected_ssh_key_data: ExpectedSSHKeyData):
    item_name = "Example SSH Key"
    item_dict = valid_data.data_for_name("example-ssh-key")

    expected = expected_ssh_key_data.data_for_ssh_key(item_name)
    result = OPSSHKeyItem(item_dict)
    assert result.category == expected.category


def test_item_get_ssh_key_040(valid_data: ValidData, expected_ssh_key_data: ExpectedSSHKeyData):
    item_name = "Example SSH Key"
    item_dict = valid_data.data_for_name("example-ssh-key")

    expected = expected_ssh_key_data.data_for_ssh_key(item_name)
    result = OPSSHKeyItem(item_dict)
    assert result.last_edited_by == expected.last_edited_by


def test_item_get_ssh_key_050(valid_data: ValidData, expected_ssh_key_data: ExpectedSSHKeyData):
    item_name = "Example SSH Key"
    item_dict = valid_data.data_for_name("example-ssh-key")

    expected = expected_ssh_key_data.data_for_ssh_key(item_name)
    result = OPSSHKeyItem(item_dict)
    assert result.public_key == expected.public_key


def test_item_get_ssh_key_060(valid_data: ValidData, expected_ssh_key_data: ExpectedSSHKeyData):
    item_name = "Example SSH Key"
    item_dict = valid_data.data_for_name("example-ssh-key")

    expected = expected_ssh_key_data.data_for_ssh_key(item_name)
    result = OPSSHKeyItem(item_dict)
    assert result.public_key_reference == expected.public_key_ref


def test_item_get_ssh_key_070(valid_data: ValidData, expected_ssh_key_data: ExpectedSSHKeyData):
    item_name = "Example SSH Key"
    item_dict = valid_data.data_for_name("example-ssh-key")

    expected = expected_ssh_key_data.data_for_ssh_key(item_name)
    result = OPSSHKeyItem(item_dict)
    assert result.fingerprint == expected.fingerprint


def test_item_get_ssh_key_080(valid_data: ValidData, expected_ssh_key_data: ExpectedSSHKeyData):
    item_name = "Example SSH Key"
    item_dict = valid_data.data_for_name("example-ssh-key")

    expected = expected_ssh_key_data.data_for_ssh_key(item_name)
    result = OPSSHKeyItem(item_dict)
    assert result.fingerprint_reference == expected.fingerprint_ref


def test_item_get_ssh_key_090(valid_data: ValidData, expected_ssh_key_data: ExpectedSSHKeyData):
    item_name = "Example SSH Key"
    item_dict = valid_data.data_for_name("example-ssh-key")

    expected = expected_ssh_key_data.data_for_ssh_key(item_name)
    result = OPSSHKeyItem(item_dict)
    assert result.private_key == expected.private_key


def test_item_get_ssh_key_100(valid_data: ValidData, expected_ssh_key_data: ExpectedSSHKeyData):
    item_name = "Example SSH Key"
    item_dict = valid_data.data_for_name("example-ssh-key")

    expected = expected_ssh_key_data.data_for_ssh_key(item_name)
    result = OPSSHKeyItem(item_dict)
    assert result.private_key_reference == expected.private_key_ref


def test_item_get_ssh_key_110(valid_data: ValidData, expected_ssh_key_data: ExpectedSSHKeyData):
    item_name = "Example SSH Key"
    item_dict = valid_data.data_for_name("example-ssh-key")

    expected = expected_ssh_key_data.data_for_ssh_key(item_name)
    result = OPSSHKeyItem(item_dict)
    assert result.key_type == expected.key_type


def test_item_get_ssh_key_120(valid_data: ValidData, expected_ssh_key_data: ExpectedSSHKeyData):
    item_name = "Example SSH Key"
    item_dict = valid_data.data_for_name("example-ssh-key")

    expected = expected_ssh_key_data.data_for_ssh_key(item_name)
    result = OPSSHKeyItem(item_dict)
    assert result.key_type_reference == expected.key_type_ref
