from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pyonepassword import OP
    from ..fixtures.expected_database import ExpectedDatabaseItem, ExpectedDatabaseItemData

from pyonepassword.api.object_types import OPDatabaseItem

# ensure HOME env variable is set, and there's a valid op config present
pytestmark = pytest.mark.usefixtures("valid_op_cli_config_homedir")

# connection_options


def test_item_get_database_01(signed_in_op: OP, expected_database_data: ExpectedDatabaseItemData):
    """
    call OP.item_get() to get a database item

    Verify:
        expected username matches actual username
    """
    item_name = "Example Database 1"
    vault = "Test Data"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)
    result = signed_in_op.item_get(item_name, vault=vault)
    assert isinstance(result, OPDatabaseItem)
    assert result.username == expected.username


def test_item_get_database_02(signed_in_op: OP, expected_database_data: ExpectedDatabaseItemData):
    """
    call OP.item_get() to get a database item

    Verify:
        expected password matches actual password
    """
    item_name = "Example Database 1"
    vault = "Test Data"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)
    result = signed_in_op.item_get(item_name, vault=vault)
    assert isinstance(result, OPDatabaseItem)
    assert result.password == expected.password


def test_item_get_database_03(signed_in_op: OP, expected_database_data: ExpectedDatabaseItemData):
    """
    call OP.item_get() to get a database item

    Verify:
        expected database_type matches actual database_type
    """
    item_name = "Example Database 1"
    vault = "Test Data"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)
    result = signed_in_op.item_get(item_name, vault=vault)
    assert isinstance(result, OPDatabaseItem)
    assert result.database_type == expected.database_type


def test_item_get_database_04(signed_in_op: OP, expected_database_data: ExpectedDatabaseItemData):
    """
    call OP.item_get() to get a database item

    Verify:
        expected databse_type matches actual convience property "type"
    """
    item_name = "Example Database 1"
    vault = "Test Data"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)
    result = signed_in_op.item_get(item_name, vault=vault)
    assert isinstance(result, OPDatabaseItem)
    assert result.type == expected.database_type


def test_item_get_database_05(signed_in_op: OP, expected_database_data: ExpectedDatabaseItemData):
    """
    call OP.item_get() to get a database item

    Verify:
        expected hostname matches actual hostname
    """
    item_name = "Example Database 1"
    vault = "Test Data"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)
    result: OPDatabaseItem = signed_in_op.item_get(item_name, vault=vault)
    assert isinstance(result, OPDatabaseItem)
    assert result.hostname == expected.hostname


def test_item_get_database_06(signed_in_op: OP, expected_database_data: ExpectedDatabaseItemData):
    """
    call OP.item_get() to get a database item

    Verify:
        expected hostname matches actual convenience property "server"
    """
    item_name = "Example Database 1"
    vault = "Test Data"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)
    result: OPDatabaseItem = signed_in_op.item_get(item_name, vault=vault)
    assert isinstance(result, OPDatabaseItem)
    assert result.server == expected.hostname


def test_item_get_database_07(signed_in_op: OP, expected_database_data: ExpectedDatabaseItemData):
    """
    call OP.item_get() to get a database item

    Verify:
        expected port matches actual port
    """
    item_name = "Example Database 1"
    vault = "Test Data"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)
    result: OPDatabaseItem = signed_in_op.item_get(item_name, vault=vault)
    assert isinstance(result, OPDatabaseItem)
    assert result.port == expected.port


def test_item_get_database_08(signed_in_op: OP, expected_database_data: ExpectedDatabaseItemData):
    """
    call OP.item_get() to get a database item

    Verify:
        expected database field matches actual database field
    """
    item_name = "Example Database 1"
    vault = "Test Data"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)
    result: OPDatabaseItem = signed_in_op.item_get(item_name, vault=vault)
    assert isinstance(result, OPDatabaseItem)
    assert result.database == expected.database


def test_item_get_database_09(signed_in_op: OP, expected_database_data: ExpectedDatabaseItemData):
    """
    call OP.item_get() to get a database item

    Verify:
        expected sid matches actual sid
    """
    item_name = "Example Database 1"
    vault = "Test Data"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)
    result: OPDatabaseItem = signed_in_op.item_get(item_name, vault=vault)
    assert isinstance(result, OPDatabaseItem)
    assert result.sid is None
    assert result.sid == expected.sid


def test_item_get_database_10(signed_in_op: OP, expected_database_data: ExpectedDatabaseItemData):
    """
    call OP.item_get() to get a database item

    Verify:
        expected alias matches actual alias
    """
    item_name = "Example Database 1"
    vault = "Test Data"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)
    result: OPDatabaseItem = signed_in_op.item_get(item_name, vault=vault)
    assert isinstance(result, OPDatabaseItem)
    assert result.alias == expected.alias


def test_item_get_database_11(signed_in_op: OP, expected_database_data: ExpectedDatabaseItemData):
    """
    call OP.item_get() to get a database item

    Verify:
        expected options matches actual options
    """
    item_name = "Example Database 1"
    vault = "Test Data"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)
    result: OPDatabaseItem = signed_in_op.item_get(item_name, vault=vault)
    assert isinstance(result, OPDatabaseItem)
    assert result.options == expected.options


def test_item_get_database_12(signed_in_op: OP, expected_database_data: ExpectedDatabaseItemData):
    """
    call OP.item_get() to get a database item

    Verify:
        expected options matches actual convenience property "connection_options"
    """
    item_name = "Example Database 1"
    vault = "Test Data"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)
    result: OPDatabaseItem = signed_in_op.item_get(item_name, vault=vault)
    assert isinstance(result, OPDatabaseItem)
    assert result.connection_options == expected.options
