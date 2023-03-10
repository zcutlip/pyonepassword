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


def test_item_get_database_13(signed_in_op: OP, expected_database_data: ExpectedDatabaseItemData):
    """
    call OP.item_get() to get a database item

    Verify:
        expected username matches actual username
    """
    item_name = "Example Database 2"
    vault = "Test Data"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)
    result = signed_in_op.item_get(item_name, vault=vault)
    assert isinstance(result, OPDatabaseItem)
    assert result.username
    assert result.username == expected.username


def test_item_get_database_14(signed_in_op: OP, expected_database_data: ExpectedDatabaseItemData):
    """
    call OP.item_get() to get a database item

    Verify:
        expected password matches actual password
    """
    item_name = "Example Database 2"
    vault = "Test Data"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)
    result = signed_in_op.item_get(item_name, vault=vault)
    assert isinstance(result, OPDatabaseItem)
    assert result.password
    assert result.password == expected.password


def test_item_get_database_15(signed_in_op: OP, expected_database_data: ExpectedDatabaseItemData):
    """
    call OP.item_get() to get a database item

    Verify:
        expected database_type matches actual database_type
    """
    item_name = "Example Database 2"
    vault = "Test Data"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)
    result = signed_in_op.item_get(item_name, vault=vault)
    assert isinstance(result, OPDatabaseItem)
    assert result.database_type
    assert result.database_type == expected.database_type


def test_item_get_database_16(signed_in_op: OP, expected_database_data: ExpectedDatabaseItemData):
    """
    call OP.item_get() to get a database item

    Verify:
        expected databse_type matches actual convience property "type"
    """
    item_name = "Example Database 2"
    vault = "Test Data"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)
    result = signed_in_op.item_get(item_name, vault=vault)
    assert isinstance(result, OPDatabaseItem)
    assert result.type
    assert result.type == expected.database_type


def test_item_get_database_17(signed_in_op: OP, expected_database_data: ExpectedDatabaseItemData):
    """
    call OP.item_get() to get a database item

    Verify:
        expected hostname matches actual hostname
    """
    item_name = "Example Database 2"
    vault = "Test Data"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)
    result: OPDatabaseItem = signed_in_op.item_get(item_name, vault=vault)
    assert isinstance(result, OPDatabaseItem)
    assert result.hostname
    assert result.hostname == expected.hostname


def test_item_get_database_18(signed_in_op: OP, expected_database_data: ExpectedDatabaseItemData):
    """
    call OP.item_get() to get a database item

    Verify:
        expected hostname matches actual convenience property "server"
    """
    item_name = "Example Database 2"
    vault = "Test Data"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)
    result: OPDatabaseItem = signed_in_op.item_get(item_name, vault=vault)
    assert isinstance(result, OPDatabaseItem)
    assert result.server
    assert result.server == expected.hostname


def test_item_get_database_19(signed_in_op: OP, expected_database_data: ExpectedDatabaseItemData):
    """
    call OP.item_get() to get a database item

    Verify:
        expected port matches actual port
    """
    item_name = "Example Database 2"
    vault = "Test Data"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)
    result: OPDatabaseItem = signed_in_op.item_get(item_name, vault=vault)
    assert isinstance(result, OPDatabaseItem)
    assert result.port
    assert result.port == expected.port


def test_item_get_database_20(signed_in_op: OP, expected_database_data: ExpectedDatabaseItemData):
    """
    call OP.item_get() to get a database item

    Verify:
        expected database field matches actual database field
    """
    item_name = "Example Database 2"
    vault = "Test Data"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)
    result: OPDatabaseItem = signed_in_op.item_get(item_name, vault=vault)
    assert isinstance(result, OPDatabaseItem)
    assert result.database
    assert result.database == expected.database


def test_item_get_database_21(signed_in_op: OP):
    """
    call OP.item_get() to get a database item

    Verify:
        expected sid matches actual sid
    """
    item_name = "Example Database 2"
    vault = "Test Data"

    result: OPDatabaseItem = signed_in_op.item_get(item_name, vault=vault)
    assert isinstance(result, OPDatabaseItem)
    assert result.sid is None


def test_item_get_database_22(signed_in_op: OP):
    """
    call OP.item_get() to get a database item

    Verify:
        expected alias matches actual alias
    """
    item_name = "Example Database 2"
    vault = "Test Data"

    result: OPDatabaseItem = signed_in_op.item_get(item_name, vault=vault)
    assert isinstance(result, OPDatabaseItem)
    assert result.alias is None


def test_item_get_database_23(signed_in_op: OP):
    """
    call OP.item_get() to get a database item

    Verify:
        expected options matches actual options
    """
    item_name = "Example Database 2"
    vault = "Test Data"

    result: OPDatabaseItem = signed_in_op.item_get(item_name, vault=vault)
    assert isinstance(result, OPDatabaseItem)
    assert result.options is None


def test_item_get_database_24(signed_in_op: OP, expected_database_data: ExpectedDatabaseItemData):
    """
    call OP.item_get() to get a database item

    Verify:
        expected options matches actual convenience property "connection_options"
    """
    item_name = "Example Database 2"
    vault = "Test Data"

    result: OPDatabaseItem = signed_in_op.item_get(item_name, vault=vault)
    assert isinstance(result, OPDatabaseItem)
    assert result.connection_options is None


# For the following tests, the database item
# was created from a template with most fields missing
# as a result the resulting item has most fields missing
# these tests verify the field values returned are None
def test_item_get_database_25(signed_in_op: OP):
    """
    call OP.item_get() to get a database item

    Verify:
        username is None
    """
    item_name = "Example Database Missing Fields"
    vault = "Test Data"

    result = signed_in_op.item_get(item_name, vault=vault)
    assert isinstance(result, OPDatabaseItem)
    assert result.username is None


def test_item_get_database_26(signed_in_op: OP):
    """
    call OP.item_get() to get a database item

    Verify:
        password is None
    """
    item_name = "Example Database Missing Fields"
    vault = "Test Data"
    result = signed_in_op.item_get(item_name, vault=vault)
    assert isinstance(result, OPDatabaseItem)
    assert result.password is None


def test_item_get_database_27(signed_in_op: OP, expected_database_data: ExpectedDatabaseItemData):
    """
    call OP.item_get() to get a database item

    Verify:
        expected database_type matches actual database_type
    """
    item_name = "Example Database Missing Fields"
    vault = "Test Data"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)
    result = signed_in_op.item_get(item_name, vault=vault)
    assert isinstance(result, OPDatabaseItem)
    assert result.database_type
    assert result.database_type == expected.database_type


def test_item_get_database_28(signed_in_op):
    """
    call OP.item_get() to get a database item

    Verify:
        hostname is None
    """
    item_name = "Example Database Missing Fields"
    vault = "Test Data"

    result: OPDatabaseItem = signed_in_op.item_get(item_name, vault=vault)
    assert isinstance(result, OPDatabaseItem)
    assert result.hostname is None


def test_item_get_database_29(signed_in_op: OP):
    """
    call OP.item_get() to get a database item

    Verify:
        convenience property "server" returns None
    """
    item_name = "Example Database Missing Fields"
    vault = "Test Data"
    result: OPDatabaseItem = signed_in_op.item_get(item_name, vault=vault)
    assert isinstance(result, OPDatabaseItem)
    assert result.server is None


def test_item_get_database_30(signed_in_op: OP):
    """
    call OP.item_get() to get a database item

    Verify:
        port is None
    """
    item_name = "Example Database Missing Fields"
    vault = "Test Data"

    result: OPDatabaseItem = signed_in_op.item_get(item_name, vault=vault)
    assert isinstance(result, OPDatabaseItem)
    assert result.port is None


def test_item_get_database_31(signed_in_op: OP):
    """
    call OP.item_get() to get a database item

    Verify:
        "database" property returns None
    """
    item_name = "Example Database Missing Fields"
    vault = "Test Data"

    result: OPDatabaseItem = signed_in_op.item_get(item_name, vault=vault)
    assert isinstance(result, OPDatabaseItem)
    assert result.database is None


def test_item_get_database_32(signed_in_op: OP):
    """
    call OP.item_get() to get a database item

    Verify:
        sid property returns None
    """
    item_name = "Example Database Missing Fields"
    vault = "Test Data"

    result: OPDatabaseItem = signed_in_op.item_get(item_name, vault=vault)
    assert isinstance(result, OPDatabaseItem)
    assert result.sid is None


def test_item_get_database_33(signed_in_op: OP):
    """
    call OP.item_get() to get a database item

    Verify:
        alias property returns None
    """
    item_name = "Example Database Missing Fields"
    vault = "Test Data"

    result: OPDatabaseItem = signed_in_op.item_get(item_name, vault=vault)
    assert isinstance(result, OPDatabaseItem)
    assert result.alias is None


def test_item_get_database_34(signed_in_op: OP):
    """
    call OP.item_get() to get a database item

    Verify:
        options property returns None
    """
    item_name = "Example Database Missing Fields"
    vault = "Test Data"

    result: OPDatabaseItem = signed_in_op.item_get(item_name, vault=vault)
    assert isinstance(result, OPDatabaseItem)
    assert result.options is None


def test_item_get_database_35(signed_in_op: OP):
    """
    call OP.item_get() to get a database item

    Verify:
        convenience property "connection_options" returns None
    """
    item_name = "Example Database Missing Fields"
    vault = "Test Data"

    result: OPDatabaseItem = signed_in_op.item_get(item_name, vault=vault)
    assert isinstance(result, OPDatabaseItem)
    assert result.connection_options is None
