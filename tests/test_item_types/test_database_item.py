from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from ..fixtures.expected_database import ExpectedDatabaseItem, ExpectedDatabaseItemData
    from ..fixtures.valid_data import ValidData

from pyonepassword.api.object_types import OPDatabaseItem

# ensure HOME env variable is set, and there's a valid op config present
pytestmark = pytest.mark.usefixtures("valid_op_cli_config_homedir")


# database 1 is a postgres database the following fields populated
# database_type
# hostname
# port
# database
# username
# password
# sid (set to string "none")
# alias
# options
VALID_DATABASE_1 = "example-database-1"
# database 2 is a postgres database all except the following fields populated
# sid (set to string "none")
# alias
# options
VALID_DATABASE_2 = "example-database-2"


def test_database_item_010(valid_data: ValidData, expected_database_data: ExpectedDatabaseItemData):
    """
    call OP.item_get() to get a database item

    Verify:
        expected username matches actual username
    """
    item_name = "Example Database 1"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)
    item_dict = valid_data.data_for_name(VALID_DATABASE_1)
    result = OPDatabaseItem(item_dict)
    assert result.username == expected.username


def test_database_item_020(valid_data: ValidData, expected_database_data: ExpectedDatabaseItemData):
    """
    call OP.item_get() to get a database item

    Verify:
        expected password matches actual password
    """
    item_name = "Example Database 1"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)
    item_dict = valid_data.data_for_name(VALID_DATABASE_1)
    result = OPDatabaseItem(item_dict)

    assert result.password == expected.password


def test_database_item_030(valid_data: ValidData, expected_database_data: ExpectedDatabaseItemData):
    """
    call OP.item_get() to get a database item

    Verify:
        expected database_type matches actual database_type
    """
    item_name = "Example Database 1"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)

    item_dict = valid_data.data_for_name(VALID_DATABASE_1)
    result = OPDatabaseItem(item_dict)

    assert result.database_type == expected.database_type


def test_database_item_04(valid_data: ValidData, expected_database_data: ExpectedDatabaseItemData):
    """
    call OP.item_get() to get a database item

    Verify:
        expected databse_type matches actual convenience property "type"
    """
    item_name = "Example Database 1"

    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)
    item_dict = valid_data.data_for_name(VALID_DATABASE_1)
    result = OPDatabaseItem(item_dict)

    assert result.type == expected.database_type


def test_database_item_050(valid_data: ValidData, expected_database_data: ExpectedDatabaseItemData):
    """
    call OP.item_get() to get a database item

    Verify:
        expected hostname matches actual hostname
    """
    item_name = "Example Database 1"

    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)

    item_dict = valid_data.data_for_name(VALID_DATABASE_1)
    result = OPDatabaseItem(item_dict)

    assert result.hostname == expected.hostname


def test_database_item_060(valid_data: ValidData, expected_database_data: ExpectedDatabaseItemData):
    """
    call OP.item_get() to get a database item

    Verify:
        expected hostname matches actual convenience property "server"
    """
    item_name = "Example Database 1"

    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)

    item_dict = valid_data.data_for_name(VALID_DATABASE_1)
    result = OPDatabaseItem(item_dict)

    assert result.server == expected.hostname


def test_database_item_070(valid_data: ValidData, expected_database_data: ExpectedDatabaseItemData):
    """
    call OP.item_get() to get a database item

    Verify:
        expected port matches actual port
    """
    item_name = "Example Database 1"

    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)
    item_dict = valid_data.data_for_name(VALID_DATABASE_1)
    result = OPDatabaseItem(item_dict)

    assert result.port == expected.port


def test_database_item_080(valid_data: ValidData, expected_database_data: ExpectedDatabaseItemData):
    """
    call OP.item_get() to get a database item

    Verify:
        expected database field matches actual database field
    """
    item_name = "Example Database 1"

    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)

    item_dict = valid_data.data_for_name(VALID_DATABASE_1)
    result = OPDatabaseItem(item_dict)

    assert result.database == expected.database


def test_database_item_090(valid_data: ValidData, expected_database_data: ExpectedDatabaseItemData):
    """
    call OP.item_get() to get a database item

    Verify:
        expected sid matches actual sid
    """
    item_name = "Example Database 1"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)

    item_dict = valid_data.data_for_name(VALID_DATABASE_1)
    result = OPDatabaseItem(item_dict)

    assert result.sid is None
    assert result.sid == expected.sid


def test_database_item_100(valid_data: ValidData, expected_database_data: ExpectedDatabaseItemData):
    """
    call OP.item_get() to get a database item

    Verify:
        expected alias matches actual alias
    """
    item_name = "Example Database 1"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)

    item_dict = valid_data.data_for_name(VALID_DATABASE_1)
    result = OPDatabaseItem(item_dict)

    assert result.alias == expected.alias


def test_database_item_110(valid_data: ValidData, expected_database_data: ExpectedDatabaseItemData):
    """
    call OP.item_get() to get a database item

    Verify:
        expected options matches actual options
    """
    item_name = "Example Database 1"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)

    item_dict = valid_data.data_for_name(VALID_DATABASE_1)
    result = OPDatabaseItem(item_dict)

    assert result.options == expected.options


def test_database_item_120(valid_data: ValidData, expected_database_data: ExpectedDatabaseItemData):
    """
    call OP.item_get() to get a database item

    Verify:
        expected options matches actual convenience property "connection_options"
    """
    item_name = "Example Database 1"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)

    item_dict = valid_data.data_for_name(VALID_DATABASE_1)
    result = OPDatabaseItem(item_dict)

    assert result.connection_options == expected.options


def test_database_item_130(valid_data: ValidData, expected_database_data: ExpectedDatabaseItemData):
    """
    call OP.item_get() to get a database item

    Verify:
        expected username matches actual username
    """
    item_name = "Example Database 2"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)

    item_dict = valid_data.data_for_name(VALID_DATABASE_2)
    result = OPDatabaseItem(item_dict)

    assert result.username
    assert result.username == expected.username


def test_database_item_140(valid_data: ValidData, expected_database_data: ExpectedDatabaseItemData):
    """
    call OP.item_get() to get a database item

    Verify:
        expected password matches actual password
    """
    item_name = "Example Database 2"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)

    item_dict = valid_data.data_for_name(VALID_DATABASE_2)
    result = OPDatabaseItem(item_dict)

    assert result.password
    assert result.password == expected.password


def test_database_item_150(valid_data: ValidData, expected_database_data: ExpectedDatabaseItemData):
    """
    call OP.item_get() to get a database item

    Verify:
        expected database_type matches actual database_type
    """
    item_name = "Example Database 2"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)

    item_dict = valid_data.data_for_name(VALID_DATABASE_2)
    result = OPDatabaseItem(item_dict)

    assert result.database_type
    assert result.database_type == expected.database_type


def test_database_item_160(valid_data: ValidData, expected_database_data: ExpectedDatabaseItemData):
    """
    call OP.item_get() to get a database item

    Verify:
        expected database_type matches actual convenience property "type"
    """
    item_name = "Example Database 2"

    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)

    item_dict = valid_data.data_for_name(VALID_DATABASE_2)
    result = OPDatabaseItem(item_dict)

    assert result.type
    assert result.type == expected.database_type


def test_database_item_170(valid_data: ValidData, expected_database_data: ExpectedDatabaseItemData):
    """
    call OP.item_get() to get a database item

    Verify:
        expected hostname matches actual hostname
    """
    item_name = "Example Database 2"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)

    item_dict = valid_data.data_for_name(VALID_DATABASE_2)
    result = OPDatabaseItem(item_dict)

    assert result.hostname
    assert result.hostname == expected.hostname


def test_database_item_180(valid_data: ValidData, expected_database_data: ExpectedDatabaseItemData):
    """
    call OP.item_get() to get a database item

    Verify:
        expected hostname matches actual convenience property "server"
    """
    item_name = "Example Database 2"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)

    item_dict = valid_data.data_for_name(VALID_DATABASE_2)
    result = OPDatabaseItem(item_dict)

    assert result.server
    assert result.server == expected.hostname


def test_database_item_190(valid_data: ValidData, expected_database_data: ExpectedDatabaseItemData):
    """
    call OP.item_get() to get a database item

    Verify:
        expected port matches actual port
    """
    item_name = "Example Database 2"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)

    item_dict = valid_data.data_for_name(VALID_DATABASE_2)
    result = OPDatabaseItem(item_dict)

    assert result.port
    assert result.port == expected.port


def test_database_item_200(valid_data: ValidData, expected_database_data: ExpectedDatabaseItemData):
    """
    call OP.item_get() to get a database item

    Verify:
        expected database field matches actual database field
    """
    item_name = "Example Database 2"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)

    item_dict = valid_data.data_for_name(VALID_DATABASE_2)
    result = OPDatabaseItem(item_dict)

    assert result.database
    assert result.database == expected.database


def test_database_item_210(valid_data: ValidData):
    """
    call OP.item_get() to get a database item

    Verify:
        expected sid matches actual sid
    """

    item_dict = valid_data.data_for_name(VALID_DATABASE_2)
    result = OPDatabaseItem(item_dict)

    assert result.sid is None


def test_database_item_220(valid_data: ValidData):
    """
    call OP.item_get() to get a database item

    Verify:
        expected alias matches actual alias
    """

    item_dict = valid_data.data_for_name(VALID_DATABASE_2)
    result = OPDatabaseItem(item_dict)

    assert result.alias is None


def test_database_item_230(valid_data: ValidData):
    """
    call OP.item_get() to get a database item

    Verify:
        expected options matches actual options
    """

    item_dict = valid_data.data_for_name(VALID_DATABASE_2)
    result = OPDatabaseItem(item_dict)

    assert result.options is None


def test_database_item_240(valid_data: ValidData):
    """
    call OP.item_get() to get a database item

    Verify:
        expected options matches actual convenience property "connection_options"
    """

    item_dict = valid_data.data_for_name(VALID_DATABASE_2)
    result = OPDatabaseItem(item_dict)

    assert result.connection_options is None


# For the following tests, the database item
# was created from a template with most fields missing
# as a result the resulting item has most fields missing
# these tests verify the field values returned are None
def test_database_item_250(valid_data: ValidData, expected_database_data: ExpectedDatabaseItemData):
    """
    call OP.item_get() to get a database item

    Verify:
        username is None
    """
    item_name = "Example Database 2"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)
    item_dict = valid_data.data_for_name(VALID_DATABASE_2)
    result = OPDatabaseItem(item_dict)

    assert result.username == expected.username


def test_database_item_260(valid_data: ValidData, expected_database_data: ExpectedDatabaseItemData):
    """
    call OP.item_get() to get a database item

    Verify:
        password is None
    """
    item_name = "Example Database 2"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)

    item_dict = valid_data.data_for_name(VALID_DATABASE_2)
    result = OPDatabaseItem(item_dict)

    assert result.password == expected.password


def test_database_item_270(valid_data: ValidData, expected_database_data: ExpectedDatabaseItemData):
    """
    call OP.item_get() to get a database item

    Verify:
        expected database_type matches actual database_type
    """
    item_name = "Example Database Missing Fields"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)

    item_dict = valid_data.data_for_name(VALID_DATABASE_2)
    result = OPDatabaseItem(item_dict)

    assert result.database_type
    assert result.database_type == expected.database_type


def test_database_item_280(valid_data: ValidData, expected_database_data: ExpectedDatabaseItemData):
    """
    call OP.item_get() to get a database item

    Verify:
        hostname is None
    """
    item_name = "Example Database 2"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)
    item_dict = valid_data.data_for_name(VALID_DATABASE_2)
    result = OPDatabaseItem(item_dict)

    assert result.hostname == expected.hostname


def test_database_item_290(valid_data: ValidData, expected_database_data: ExpectedDatabaseItemData):
    """
    call OP.item_get() to get a database item

    Verify:
        convenience property "server" returns None
    """
    item_name = "Example Database 2"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)
    item_dict = valid_data.data_for_name(VALID_DATABASE_2)
    result = OPDatabaseItem(item_dict)

    assert result.server == expected.hostname


def test_database_item_300(valid_data: ValidData, expected_database_data: ExpectedDatabaseItemData):
    """
    call OP.item_get() to get a database item

    Verify:
        port is None
    """
    item_name = "Example Database 2"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)
    item_dict = valid_data.data_for_name(VALID_DATABASE_2)
    result = OPDatabaseItem(item_dict)

    assert result.port == expected.port


def test_database_item_310(valid_data: ValidData, expected_database_data: ExpectedDatabaseItemData):
    """
    call OP.item_get() to get a database item

    Verify:
        "database" property returns None
    """
    item_name = "Example Database 2"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)
    item_dict = valid_data.data_for_name(VALID_DATABASE_2)
    result = OPDatabaseItem(item_dict)

    assert result.database == expected.database


def test_database_item_320(valid_data: ValidData):
    """
    call OP.item_get() to get a database item

    Verify:
        sid property returns None
    """
    item_dict = valid_data.data_for_name(VALID_DATABASE_2)
    result = OPDatabaseItem(item_dict)

    assert result.sid is None


def test_database_item_330(valid_data: ValidData):
    """
    call OP.item_get() to get a database item

    Verify:
        alias property returns None
    """
    item_dict = valid_data.data_for_name(VALID_DATABASE_2)
    result = OPDatabaseItem(item_dict)

    assert result.alias is None


def test_database_item_340(valid_data: ValidData):
    """
    call OP.item_get() to get a database item

    Verify:
        options property returns None
    """
    item_dict = valid_data.data_for_name(VALID_DATABASE_2)
    result = OPDatabaseItem(item_dict)
    assert result.options is None


def test_database_item_350(valid_data: ValidData):
    """
    call OP.item_get() to get a database item

    Verify:
        convenience property "connection_options" returns None
    """
    item_dict = valid_data.data_for_name(VALID_DATABASE_2)
    result = OPDatabaseItem(item_dict)

    assert result.connection_options is None
