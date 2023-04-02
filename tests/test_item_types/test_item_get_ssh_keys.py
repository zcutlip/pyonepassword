# __future__.annotaitons, and typing.TYPE_CHECKING
# enable anything imported for type hinting to disappear at run time
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

# make imports for type-hinting disappear at run-time to avoid
# circular imports.
# this also reduced exercising tested code simply by importing
if TYPE_CHECKING:
    from ..fixtures.expected_ssh_key_data import ExpectedSSHKey, ExpectedSSHKeyData
    from pyonepassword import OP

from pyonepassword.api.object_types import OPSSHKeyItem

# ensure HOME env variable is set, and there's a valid op config present
pytestmark = pytest.mark.usefixtures("valid_op_cli_config_homedir")


def test_item_get_ssh_key_01(signed_in_op: OP, expected_ssh_key_data: ExpectedSSHKeyData):
    item_name = "Example SSH Key"
    expected: ExpectedSSHKey
    result: OPSSHKeyItem

    expected = expected_ssh_key_data.data_for_ssh_key(item_name)
    result = signed_in_op.item_get(item_name)
    assert isinstance(result, OPSSHKeyItem)
    assert result.unique_id == expected.unique_id


def test_item_get_ssh_key_02(signed_in_op: OP, expected_ssh_key_data: ExpectedSSHKeyData):
    item_name = "Example SSH Key"
    expected: ExpectedSSHKey
    result: OPSSHKeyItem

    expected = expected_ssh_key_data.data_for_ssh_key(item_name)
    result = signed_in_op.item_get(item_name)
    assert isinstance(result, OPSSHKeyItem)
    assert result.title == expected.title


def test_item_get_ssh_key_03(signed_in_op: OP, expected_ssh_key_data: ExpectedSSHKeyData):
    item_name = "Example SSH Key"
    expected: ExpectedSSHKey
    result: OPSSHKeyItem

    expected = expected_ssh_key_data.data_for_ssh_key(item_name)
    result = signed_in_op.item_get(item_name)
    assert isinstance(result, OPSSHKeyItem)
    assert result.category == expected.category


def test_item_get_ssh_key_04(signed_in_op: OP, expected_ssh_key_data: ExpectedSSHKeyData):
    item_name = "Example SSH Key"
    expected: ExpectedSSHKey
    result: OPSSHKeyItem

    expected = expected_ssh_key_data.data_for_ssh_key(item_name)
    result = signed_in_op.item_get(item_name)
    assert isinstance(result, OPSSHKeyItem)
    assert result.last_edited_by == expected.last_edited_by


def test_item_get_ssh_key_05(signed_in_op: OP, expected_ssh_key_data: ExpectedSSHKeyData):
    item_name = "Example SSH Key"
    expected: ExpectedSSHKey
    result: OPSSHKeyItem

    expected = expected_ssh_key_data.data_for_ssh_key(item_name)
    result = signed_in_op.item_get(item_name)
    assert isinstance(result, OPSSHKeyItem)
    assert result.public_key == expected.public_key


def test_item_get_ssh_key_06(signed_in_op: OP, expected_ssh_key_data: ExpectedSSHKeyData):
    item_name = "Example SSH Key"
    expected: ExpectedSSHKey
    result: OPSSHKeyItem

    expected = expected_ssh_key_data.data_for_ssh_key(item_name)
    result = signed_in_op.item_get(item_name)
    assert isinstance(result, OPSSHKeyItem)
    assert result.public_key_reference == expected.public_key_ref


def test_item_get_ssh_key_07(signed_in_op: OP, expected_ssh_key_data: ExpectedSSHKeyData):
    item_name = "Example SSH Key"
    expected: ExpectedSSHKey
    result: OPSSHKeyItem

    expected = expected_ssh_key_data.data_for_ssh_key(item_name)
    result = signed_in_op.item_get(item_name)
    assert isinstance(result, OPSSHKeyItem)
    assert result.fingerprint == expected.fingerprint


def test_item_get_ssh_key_08(signed_in_op: OP, expected_ssh_key_data: ExpectedSSHKeyData):
    item_name = "Example SSH Key"
    expected: ExpectedSSHKey
    result: OPSSHKeyItem

    expected = expected_ssh_key_data.data_for_ssh_key(item_name)
    result = signed_in_op.item_get(item_name)
    assert isinstance(result, OPSSHKeyItem)
    assert result.fingerprint_reference == expected.fingerprint_ref


def test_item_get_ssh_key_09(signed_in_op: OP, expected_ssh_key_data: ExpectedSSHKeyData):
    item_name = "Example SSH Key"
    expected: ExpectedSSHKey
    result: OPSSHKeyItem

    expected = expected_ssh_key_data.data_for_ssh_key(item_name)
    result = signed_in_op.item_get(item_name)
    assert isinstance(result, OPSSHKeyItem)
    assert result.private_key == expected.private_key


def test_item_get_ssh_key_10(signed_in_op: OP, expected_ssh_key_data: ExpectedSSHKeyData):
    item_name = "Example SSH Key"
    expected: ExpectedSSHKey
    result: OPSSHKeyItem

    expected = expected_ssh_key_data.data_for_ssh_key(item_name)
    result = signed_in_op.item_get(item_name)
    assert isinstance(result, OPSSHKeyItem)
    assert result.private_key_reference == expected.private_key_ref


def test_item_get_ssh_key_11(signed_in_op: OP, expected_ssh_key_data: ExpectedSSHKeyData):
    item_name = "Example SSH Key"
    expected: ExpectedSSHKey
    result: OPSSHKeyItem

    expected = expected_ssh_key_data.data_for_ssh_key(item_name)
    result = signed_in_op.item_get(item_name)
    assert isinstance(result, OPSSHKeyItem)
    assert result.key_type == expected.key_type


def test_item_get_ssh_key_12(signed_in_op: OP, expected_ssh_key_data: ExpectedSSHKeyData):
    item_name = "Example SSH Key"
    expected: ExpectedSSHKey
    result: OPSSHKeyItem

    expected = expected_ssh_key_data.data_for_ssh_key(item_name)
    result = signed_in_op.item_get(item_name)
    assert isinstance(result, OPSSHKeyItem)
    assert result.key_type_reference == expected.key_type_ref
