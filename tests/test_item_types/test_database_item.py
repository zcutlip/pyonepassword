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

# missing all fields excapt database_type
VALID_DATABASE_MISSING_FIELDS = "example-database-missing-fields"


def test_database_item_010(valid_data: ValidData, expected_database_data: ExpectedDatabaseItemData):
    """
    Create:
        - database item object from "example database 1"
    Verify:
        - username property matches expected value
    """
    item_name = "Example Database 1"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)
    item_dict = valid_data.data_for_name(VALID_DATABASE_1)
    result = OPDatabaseItem(item_dict)
    assert result.username == expected.username


def test_database_item_020(valid_data: ValidData, expected_database_data: ExpectedDatabaseItemData):
    """
    Create:
        - database item object from "example database 1"
    Verify:
        - password property matches expected value
    """
    item_name = "Example Database 1"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)
    item_dict = valid_data.data_for_name(VALID_DATABASE_1)
    result = OPDatabaseItem(item_dict)

    assert result.password == expected.password


def test_database_item_030(valid_data: ValidData, expected_database_data: ExpectedDatabaseItemData):
    """
    Create:
        - database item object from "example database 1"
    Verify:
        - database_type property matches expected value
    """
    item_name = "Example Database 1"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)

    item_dict = valid_data.data_for_name(VALID_DATABASE_1)
    result = OPDatabaseItem(item_dict)

    assert result.database_type == expected.database_type


def test_database_item_031(valid_data: ValidData, expected_database_data: ExpectedDatabaseItemData):
    """
    Create:
        - database item object from "example database 1"
    Verify:
        - type convenience property property matches database_type expected value
    """
    item_name = "Example Database 1"

    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)
    item_dict = valid_data.data_for_name(VALID_DATABASE_1)
    result = OPDatabaseItem(item_dict)

    assert result.type == expected.database_type


def test_database_item_040(valid_data: ValidData, expected_database_data: ExpectedDatabaseItemData):
    """
    Create:
        - database item object from "example database 1"
    Verify:
        - hostname property matches expected value
    """
    item_name = "Example Database 1"

    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)

    item_dict = valid_data.data_for_name(VALID_DATABASE_1)
    result = OPDatabaseItem(item_dict)

    assert result.hostname == expected.hostname


def test_database_item_041(valid_data: ValidData, expected_database_data: ExpectedDatabaseItemData):
    """
    Create:
        - database item object from "example database 1"
    Verify:
        - server convenience property property matches hostname expected value
    """
    item_name = "Example Database 1"

    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)

    item_dict = valid_data.data_for_name(VALID_DATABASE_1)
    result = OPDatabaseItem(item_dict)

    assert result.server == expected.hostname


def test_database_item_050(valid_data: ValidData, expected_database_data: ExpectedDatabaseItemData):
    """
    Create:
        - database item object from "example database 1"
    Verify:
        - port property matches expected value
    """
    item_name = "Example Database 1"

    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)
    item_dict = valid_data.data_for_name(VALID_DATABASE_1)
    result = OPDatabaseItem(item_dict)

    assert result.port == expected.port


def test_database_item_060(valid_data: ValidData, expected_database_data: ExpectedDatabaseItemData):
    """
    Create:
        - database item object from "example database 1"
    Verify:
        - database property matches expected value
    """
    item_name = "Example Database 1"

    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)

    item_dict = valid_data.data_for_name(VALID_DATABASE_1)
    result = OPDatabaseItem(item_dict)

    assert result.database == expected.database


def test_database_item_070(valid_data: ValidData, expected_database_data: ExpectedDatabaseItemData):
    """
    Create:
        - database item object from "example database 1"
    Verify:
        - sid property is None
    """
    item_name = "Example Database 1"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)

    item_dict = valid_data.data_for_name(VALID_DATABASE_1)
    result = OPDatabaseItem(item_dict)

    assert result.sid is None
    assert result.sid == expected.sid


def test_database_item_080(valid_data: ValidData, expected_database_data: ExpectedDatabaseItemData):
    """
    Create:
        - database item object from "example database 1"
    Verify:
        - alias property matches expected value
    """
    item_name = "Example Database 1"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)

    item_dict = valid_data.data_for_name(VALID_DATABASE_1)
    result = OPDatabaseItem(item_dict)

    assert result.alias == expected.alias


def test_database_item_090(valid_data: ValidData, expected_database_data: ExpectedDatabaseItemData):
    """
    Create:
        - database item object from "example database 1"
    Verify:
        - options property matches expected value
    """
    item_name = "Example Database 1"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)

    item_dict = valid_data.data_for_name(VALID_DATABASE_1)
    result = OPDatabaseItem(item_dict)

    assert result.options == expected.options


def test_database_item_091(valid_data: ValidData, expected_database_data: ExpectedDatabaseItemData):
    """
    Create:
        - database item object from "example database 1"
    Verify:
        - connection_options convenience property property matches options expected value
    """
    item_name = "Example Database 1"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)

    item_dict = valid_data.data_for_name(VALID_DATABASE_1)
    result = OPDatabaseItem(item_dict)

    assert result.connection_options == expected.options


def test_database_item_100(valid_data: ValidData, expected_database_data: ExpectedDatabaseItemData):
    """
    Create:
        - database item object from "example database 2"
    Verify:
        - username property is not None
        - username property matches expected value
    """
    item_name = "Example Database 2"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)

    item_dict = valid_data.data_for_name(VALID_DATABASE_2)
    result = OPDatabaseItem(item_dict)

    assert result.username
    assert result.username == expected.username


def test_database_item_110(valid_data: ValidData, expected_database_data: ExpectedDatabaseItemData):
    """
    Create:
        - database item object from "example database 2"
    Verify:
        - password property is not None
        - password property matches expected value
    """
    item_name = "Example Database 2"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)

    item_dict = valid_data.data_for_name(VALID_DATABASE_2)
    result = OPDatabaseItem(item_dict)

    assert result.password
    assert result.password == expected.password


def test_database_item_120(valid_data: ValidData, expected_database_data: ExpectedDatabaseItemData):
    """
    Create:
        - database item object from "example database 2"
    Verify:
        - database_type property is not None
        - database_type property matches expected value
    """
    item_name = "Example Database 2"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)

    item_dict = valid_data.data_for_name(VALID_DATABASE_2)
    result = OPDatabaseItem(item_dict)

    assert result.database_type
    assert result.database_type == expected.database_type


def test_database_item_121(valid_data: ValidData, expected_database_data: ExpectedDatabaseItemData):
    """
    Create:
        - database item object from "example database 1"
    Verify:
        - type convenience property is not None
        - type convenience property property matches database_type expected value
    """
    item_name = "Example Database 2"

    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)

    item_dict = valid_data.data_for_name(VALID_DATABASE_2)
    result = OPDatabaseItem(item_dict)

    assert result.type
    assert result.type == expected.database_type


def test_database_item_130(valid_data: ValidData, expected_database_data: ExpectedDatabaseItemData):
    """
    Create:
        - database item object from "example database 2"
    Verify:
        - hostname property is not None
        - hostname property matches expected value
    """
    item_name = "Example Database 2"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)

    item_dict = valid_data.data_for_name(VALID_DATABASE_2)
    result = OPDatabaseItem(item_dict)

    assert result.hostname
    assert result.hostname == expected.hostname


def test_database_item_131(valid_data: ValidData, expected_database_data: ExpectedDatabaseItemData):
    """
    Create:
        - database item object from "example database 2"
    Verify:
        - server convenience property is not None
        - server convenience property matches hostname expected value
    """
    item_name = "Example Database 2"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)

    item_dict = valid_data.data_for_name(VALID_DATABASE_2)
    result = OPDatabaseItem(item_dict)

    assert result.server
    assert result.server == expected.hostname


def test_database_item_140(valid_data: ValidData, expected_database_data: ExpectedDatabaseItemData):
    """
    Create:
        - database item object from "example database 2"
    Verify:
        - port property is not None
        - port property matches expected value
    """
    item_name = "Example Database 2"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)

    item_dict = valid_data.data_for_name(VALID_DATABASE_2)
    result = OPDatabaseItem(item_dict)

    assert result.port
    assert result.port == expected.port


def test_database_item_150(valid_data: ValidData, expected_database_data: ExpectedDatabaseItemData):
    """
    Create:
        - database item object from "example database 2"
    Verify:
        - hostname property is not None
        - hostname property matches expected value
    """
    item_name = "Example Database 2"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)

    item_dict = valid_data.data_for_name(VALID_DATABASE_2)
    result = OPDatabaseItem(item_dict)

    assert result.database
    assert result.database == expected.database


def test_database_item_160(valid_data: ValidData):
    """
    Create:
        - database item object from "example database 2"
    Verify:
        - sid property is None
    """

    item_dict = valid_data.data_for_name(VALID_DATABASE_2)
    result = OPDatabaseItem(item_dict)

    assert result.sid is None


def test_database_item_170(valid_data: ValidData):
    """
    Create:
        - database item object from "example database 2"
    Verify:
        - alias property is None
    """

    item_dict = valid_data.data_for_name(VALID_DATABASE_2)
    result = OPDatabaseItem(item_dict)

    assert result.alias is None


def test_database_item_180(valid_data: ValidData):
    """
    Create:
        - database item object from "example database 2"
    Verify:
        - options property is None
    """

    item_dict = valid_data.data_for_name(VALID_DATABASE_2)
    result = OPDatabaseItem(item_dict)

    assert result.options is None


def test_database_item_181(valid_data: ValidData):
    """
    Create:
        - database item object from "example database 2"
    Verify:
        - connection_options convenience property is None
    """

    item_dict = valid_data.data_for_name(VALID_DATABASE_2)
    result = OPDatabaseItem(item_dict)

    assert result.connection_options is None


# For the following tests, the database item
# was created from a template with most fields missing
# as a result the resulting item has most fields missing
# these tests verify the field values returned are None
def test_database_item_190(valid_data: ValidData):
    """
    Create:
        - database item object from "Example Database Missing Fields"
    Verify:
        - username property is None
    """
    item_dict = valid_data.data_for_name(VALID_DATABASE_MISSING_FIELDS)
    result = OPDatabaseItem(item_dict)

    assert result.username is None


def test_database_item_200(valid_data: ValidData):
    """
    Create:
        - database item object from "example database 2"
    Verify:
        - password property is None
    """

    item_dict = valid_data.data_for_name(VALID_DATABASE_MISSING_FIELDS)
    result = OPDatabaseItem(item_dict)

    assert result.password is None


def test_database_item_210(valid_data: ValidData, expected_database_data: ExpectedDatabaseItemData):
    """
    Create:
        - database item object from "example database 2"
    Verify:
        - username property is None
    """
    item_name = "Example Database Missing Fields"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)

    item_dict = valid_data.data_for_name(VALID_DATABASE_MISSING_FIELDS)
    result = OPDatabaseItem(item_dict)

    assert result.database_type == expected.database_type


def test_database_item_220(valid_data: ValidData):
    """
    Create:
        - database item object from "example database 2"
    Verify:
        - hostname property is None
    """

    item_dict = valid_data.data_for_name(VALID_DATABASE_MISSING_FIELDS)
    result = OPDatabaseItem(item_dict)

    assert result.hostname is None


def test_database_item_221(valid_data: ValidData):
    """
    Create:
        - database item object from "example database 2"
    Verify:
        - server convenience property matches hostname expected value
    """

    item_dict = valid_data.data_for_name(VALID_DATABASE_MISSING_FIELDS)
    result = OPDatabaseItem(item_dict)

    assert result.server is None


def test_database_item_230(valid_data: ValidData):
    """
    Create:
        - database item object from "example database 2"
    Verify:
        - port property is None
    """

    item_dict = valid_data.data_for_name(VALID_DATABASE_MISSING_FIELDS)
    result = OPDatabaseItem(item_dict)

    assert result.port is None


def test_database_item_240(valid_data: ValidData):
    """
    Create:
        - database item object from "example database 2"
    Verify:
        - database property is None
    """

    item_dict = valid_data.data_for_name(VALID_DATABASE_MISSING_FIELDS)
    result = OPDatabaseItem(item_dict)

    assert result.database is None


def test_database_item_250(valid_data: ValidData):
    """
    Create:
        - database item object from "example database 2"
    Verify:
        - sid property returns None
    """
    item_dict = valid_data.data_for_name(VALID_DATABASE_MISSING_FIELDS)
    result = OPDatabaseItem(item_dict)

    assert result.sid is None


def test_database_item_260(valid_data: ValidData):
    """
    Create:
        - database item object from "example database 2"
    Verify:
        - alias property returns None
    """
    item_dict = valid_data.data_for_name(VALID_DATABASE_MISSING_FIELDS)
    result = OPDatabaseItem(item_dict)

    assert result.alias is None


def test_database_item_270(valid_data: ValidData):
    """
    Create:
        - database item object from "example database 2"
    Verify:
        - options property returns None
    """
    item_dict = valid_data.data_for_name(VALID_DATABASE_MISSING_FIELDS)
    result = OPDatabaseItem(item_dict)
    assert result.options is None


def test_database_item_271(valid_data: ValidData):
    """
    Create:
        - database item object from "example database 2"
    Verify:
        - convenience property "connection_options" returns None
    """
    item_dict = valid_data.data_for_name(VALID_DATABASE_MISSING_FIELDS)
    result = OPDatabaseItem(item_dict)

    assert result.connection_options is None
