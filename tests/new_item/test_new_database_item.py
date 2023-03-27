from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any, Dict, List

from pyonepassword.api.object_types import OPDatabaseItemTemplate

if TYPE_CHECKING:
    from ..fixtures.expected_database import (
        ExpectedDatabaseItem,
        ExpectedDatabaseItemData
    )
    from ..fixtures.valid_data import ValidData


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


def _valid_field_value_for_id(fields: List[Dict[str, Any]], field_id: str):
    """
    Field order may not be reliable, so we have to hunt for the right one
    """
    value = None
    for f in fields:
        if f["id"] == field_id:
            value = f["value"]
    return value


# Sparsely number tests in 10s (10, 20, 30...) instead of 1, 2, 3,...
# so we can add missing tests in between if necessary without
# having to renumber
def test_new_database_item_010(valid_data: ValidData, expected_database_data: ExpectedDatabaseItemData):
    """
    Create:
        - database template from "example database 1"
    Verify:
        - database_type property matches expected value
    """
    item_dict = valid_data.data_for_name(VALID_DATABASE_1)
    field_dicts = item_dict["fields"]
    item_name = "Example Database 1"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)

    database_type = _valid_field_value_for_id(field_dicts, "database_type")
    hostanme = _valid_field_value_for_id(field_dicts, "hostname")
    port = _valid_field_value_for_id(field_dicts, "port")
    database_name = _valid_field_value_for_id(field_dicts, "database")
    username = _valid_field_value_for_id(field_dicts, "username")
    password = _valid_field_value_for_id(field_dicts, "password")
    sid = _valid_field_value_for_id(field_dicts, "sid")
    alias = _valid_field_value_for_id(field_dicts, "alias")
    options = _valid_field_value_for_id(field_dicts, "options")

    database_template = OPDatabaseItemTemplate(item_name,
                                               database_type=database_type,
                                               hostname=hostanme,
                                               port=port,
                                               database=database_name,
                                               username=username,
                                               password=password,
                                               sid=sid,
                                               alias=alias,
                                               options=options)

    assert database_template.database_type == expected.database_type


def test_new_database_item_011(valid_data: ValidData, expected_database_data: ExpectedDatabaseItemData):
    """
    Create:
        - database template from "example database 1"
    Verify:
        - type convenience property property matches databas_type expected value
    """
    item_dict = valid_data.data_for_name(VALID_DATABASE_1)
    field_dicts = item_dict["fields"]
    item_name = "Example Database 1"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)

    database_type = _valid_field_value_for_id(field_dicts, "database_type")
    hostanme = _valid_field_value_for_id(field_dicts, "hostname")
    port = _valid_field_value_for_id(field_dicts, "port")
    database_name = _valid_field_value_for_id(field_dicts, "database")
    username = _valid_field_value_for_id(field_dicts, "username")
    password = _valid_field_value_for_id(field_dicts, "password")
    sid = _valid_field_value_for_id(field_dicts, "sid")
    alias = _valid_field_value_for_id(field_dicts, "alias")
    options = _valid_field_value_for_id(field_dicts, "options")

    database_template = OPDatabaseItemTemplate(item_name,
                                               database_type=database_type,
                                               hostname=hostanme,
                                               port=port,
                                               database=database_name,
                                               username=username,
                                               password=password,
                                               sid=sid,
                                               alias=alias,
                                               options=options)

    assert database_template.type == expected.database_type


def test_new_database_item_020(valid_data: ValidData, expected_database_data: ExpectedDatabaseItemData):
    """
    Create:
        - database template from "example database 1"
    Verify:
        - hostname property matches expected value
    """
    item_dict = valid_data.data_for_name(VALID_DATABASE_1)
    field_dicts = item_dict["fields"]

    item_name = "Example Database 1"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)

    database_type = _valid_field_value_for_id(field_dicts, "database_type")
    hostanme = _valid_field_value_for_id(field_dicts, "hostname")
    port = _valid_field_value_for_id(field_dicts, "port")
    database_name = _valid_field_value_for_id(field_dicts, "database")
    username = _valid_field_value_for_id(field_dicts, "username")
    password = _valid_field_value_for_id(field_dicts, "password")
    sid = _valid_field_value_for_id(field_dicts, "sid")
    alias = _valid_field_value_for_id(field_dicts, "alias")
    options = _valid_field_value_for_id(field_dicts, "options")

    database_template = OPDatabaseItemTemplate(item_name,
                                               database_type=database_type,
                                               hostname=hostanme,
                                               port=port,
                                               database=database_name,
                                               username=username,
                                               password=password,
                                               sid=sid,
                                               alias=alias,
                                               options=options)
    assert database_template.hostname == expected.hostname


def test_new_database_item_021(valid_data: ValidData, expected_database_data: ExpectedDatabaseItemData):
    """
    Create:
        - database template from "example database 1"
    Verify:
        - server convenience property matches expected hostname value
    """
    item_dict = valid_data.data_for_name(VALID_DATABASE_1)
    field_dicts = item_dict["fields"]

    item_name = "Example Database 1"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)

    database_type = _valid_field_value_for_id(field_dicts, "database_type")
    hostanme = _valid_field_value_for_id(field_dicts, "hostname")
    port = _valid_field_value_for_id(field_dicts, "port")
    database_name = _valid_field_value_for_id(field_dicts, "database")
    username = _valid_field_value_for_id(field_dicts, "username")
    password = _valid_field_value_for_id(field_dicts, "password")
    sid = _valid_field_value_for_id(field_dicts, "sid")
    alias = _valid_field_value_for_id(field_dicts, "alias")
    options = _valid_field_value_for_id(field_dicts, "options")

    database_template = OPDatabaseItemTemplate(item_name,
                                               database_type=database_type,
                                               hostname=hostanme,
                                               port=port,
                                               database=database_name,
                                               username=username,
                                               password=password,
                                               sid=sid,
                                               alias=alias,
                                               options=options)
    assert database_template.server == expected.hostname


def test_new_database_item_030(valid_data: ValidData, expected_database_data: ExpectedDatabaseItemData):
    """
    Create:
        - database template from "example database 1"
    Verify:
        - port property matches expected value
    """
    item_dict = valid_data.data_for_name(VALID_DATABASE_1)
    field_dicts = item_dict["fields"]

    item_name = "Example Database 1"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)

    database_type = _valid_field_value_for_id(field_dicts, "database_type")
    hostanme = _valid_field_value_for_id(field_dicts, "hostname")
    port = _valid_field_value_for_id(field_dicts, "port")
    database_name = _valid_field_value_for_id(field_dicts, "database")
    username = _valid_field_value_for_id(field_dicts, "username")
    password = _valid_field_value_for_id(field_dicts, "password")
    sid = _valid_field_value_for_id(field_dicts, "sid")
    alias = _valid_field_value_for_id(field_dicts, "alias")
    options = _valid_field_value_for_id(field_dicts, "options")

    database_template = OPDatabaseItemTemplate(item_name,
                                               database_type=database_type,
                                               hostname=hostanme,
                                               port=port,
                                               database=database_name,
                                               username=username,
                                               password=password,
                                               sid=sid,
                                               alias=alias,
                                               options=options)
    assert database_template.port == expected.port


def test_new_database_item_031(valid_data: ValidData, expected_database_data: ExpectedDatabaseItemData):
    """
    Create:
        - database template from "example database 1"
        - using an integer instead of a numeric string
    Verify:
        - port property is a string
        - port property matches expected value
    """
    item_dict = valid_data.data_for_name(VALID_DATABASE_1)
    field_dicts = item_dict["fields"]

    item_name = "Example Database 1"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)

    database_type = _valid_field_value_for_id(field_dicts, "database_type")
    hostanme = _valid_field_value_for_id(field_dicts, "hostname")
    port = _valid_field_value_for_id(field_dicts, "port")
    database_name = _valid_field_value_for_id(field_dicts, "database")
    username = _valid_field_value_for_id(field_dicts, "username")
    password = _valid_field_value_for_id(field_dicts, "password")
    sid = _valid_field_value_for_id(field_dicts, "sid")
    alias = _valid_field_value_for_id(field_dicts, "alias")
    options = _valid_field_value_for_id(field_dicts, "options")

    numeric_port = int(port, 0)

    database_template = OPDatabaseItemTemplate(item_name,
                                               database_type=database_type,
                                               hostname=hostanme,
                                               port=numeric_port,
                                               database=database_name,
                                               username=username,
                                               password=password,
                                               sid=sid,
                                               alias=alias,
                                               options=options)
    assert isinstance(database_template.port, str)
    assert database_template.port == expected.port


def test_new_database_item_032(valid_data: ValidData):
    """
    Create:
        - database template from "example database 1"
        - using an '0x'-prefixed hexadecimal string
    Verify:
        - port property has retained the hexadecimal string formatting
        - numeric conversion of the port property matches expected numeric value
    """
    item_dict = valid_data.data_for_name(VALID_DATABASE_1)
    field_dicts = item_dict["fields"]

    item_name = "Example Database 1"

    database_type = _valid_field_value_for_id(field_dicts, "database_type")
    hostanme = _valid_field_value_for_id(field_dicts, "hostname")
    port = _valid_field_value_for_id(field_dicts, "port")
    database_name = _valid_field_value_for_id(field_dicts, "database")
    username = _valid_field_value_for_id(field_dicts, "username")
    password = _valid_field_value_for_id(field_dicts, "password")
    sid = _valid_field_value_for_id(field_dicts, "sid")
    alias = _valid_field_value_for_id(field_dicts, "alias")
    options = _valid_field_value_for_id(field_dicts, "options")

    numeric_port = int(port, 0)
    hex_port = f"{numeric_port:#x}"

    database_template = OPDatabaseItemTemplate(item_name,
                                               database_type=database_type,
                                               hostname=hostanme,
                                               port=hex_port,
                                               database=database_name,
                                               username=username,
                                               password=password,
                                               sid=sid,
                                               alias=alias,
                                               options=options)
    assert database_template.port == hex_port
    assert int(database_template.port, 0) == numeric_port


def test_new_database_item_040(valid_data: ValidData, expected_database_data: ExpectedDatabaseItemData):
    """
    Create:
        - database template from "example database 1"
    Verify:
        - database template property matches expected value
    """
    item_dict = valid_data.data_for_name(VALID_DATABASE_1)
    field_dicts = item_dict["fields"]

    item_name = "Example Database 1"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)

    database_type = _valid_field_value_for_id(field_dicts, "database_type")
    hostanme = _valid_field_value_for_id(field_dicts, "hostname")
    port = _valid_field_value_for_id(field_dicts, "port")
    database_name = _valid_field_value_for_id(field_dicts, "database")
    username = _valid_field_value_for_id(field_dicts, "username")
    password = _valid_field_value_for_id(field_dicts, "password")
    sid = _valid_field_value_for_id(field_dicts, "sid")
    alias = _valid_field_value_for_id(field_dicts, "alias")
    options = _valid_field_value_for_id(field_dicts, "options")

    database_template = OPDatabaseItemTemplate(item_name,
                                               database_type=database_type,
                                               hostname=hostanme,
                                               port=port,
                                               database=database_name,
                                               username=username,
                                               password=password,
                                               sid=sid,
                                               alias=alias,
                                               options=options)
    assert database_template.database == expected.database


def test_new_database_item_050(valid_data: ValidData, expected_database_data: ExpectedDatabaseItemData):
    """
    Create:
        - database template from "example database 1"
    Verify:
        - username property matches expected value
    """
    item_dict = valid_data.data_for_name(VALID_DATABASE_1)
    field_dicts = item_dict["fields"]

    item_name = "Example Database 1"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)

    database_type = _valid_field_value_for_id(field_dicts, "database_type")
    hostanme = _valid_field_value_for_id(field_dicts, "hostname")
    port = _valid_field_value_for_id(field_dicts, "port")
    database_name = _valid_field_value_for_id(field_dicts, "database")
    username = _valid_field_value_for_id(field_dicts, "username")
    password = _valid_field_value_for_id(field_dicts, "password")
    sid = _valid_field_value_for_id(field_dicts, "sid")
    alias = _valid_field_value_for_id(field_dicts, "alias")
    options = _valid_field_value_for_id(field_dicts, "options")

    database_template = OPDatabaseItemTemplate(item_name,
                                               database_type=database_type,
                                               hostname=hostanme,
                                               port=port,
                                               database=database_name,
                                               username=username,
                                               password=password,
                                               sid=sid,
                                               alias=alias,
                                               options=options)
    assert database_template.username == expected.username


def test_new_database_item_060(valid_data: ValidData, expected_database_data: ExpectedDatabaseItemData):
    """
    Create:
        - database template from "example database 1"
    Verify:
        - database template property matches expected value
    """
    item_dict = valid_data.data_for_name(VALID_DATABASE_1)
    field_dicts = item_dict["fields"]

    item_name = "Example Database 1"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)

    database_type = _valid_field_value_for_id(field_dicts, "database_type")
    hostanme = _valid_field_value_for_id(field_dicts, "hostname")
    port = _valid_field_value_for_id(field_dicts, "port")
    database_name = _valid_field_value_for_id(field_dicts, "database")
    username = _valid_field_value_for_id(field_dicts, "username")
    password = _valid_field_value_for_id(field_dicts, "password")
    sid = _valid_field_value_for_id(field_dicts, "sid")
    alias = _valid_field_value_for_id(field_dicts, "alias")
    options = _valid_field_value_for_id(field_dicts, "options")

    database_template = OPDatabaseItemTemplate(item_name,
                                               database_type=database_type,
                                               hostname=hostanme,
                                               port=port,
                                               database=database_name,
                                               username=username,
                                               password=password,
                                               sid=sid,
                                               alias=alias,
                                               options=options)
    assert database_template.password == expected.password


def test_new_database_item_070(valid_data: ValidData, expected_database_data: ExpectedDatabaseItemData):
    """
    Create:
        - database template from "example database 1"
    Verify:
        - sid template property matches expected value
    """
    item_dict = valid_data.data_for_name(VALID_DATABASE_1)
    field_dicts = item_dict["fields"]

    item_name = "Example Database 1"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)

    database_type = _valid_field_value_for_id(field_dicts, "database_type")
    hostanme = _valid_field_value_for_id(field_dicts, "hostname")
    port = _valid_field_value_for_id(field_dicts, "port")
    database_name = _valid_field_value_for_id(field_dicts, "database")
    username = _valid_field_value_for_id(field_dicts, "username")
    password = _valid_field_value_for_id(field_dicts, "password")
    sid = _valid_field_value_for_id(field_dicts, "sid")
    alias = _valid_field_value_for_id(field_dicts, "alias")
    options = _valid_field_value_for_id(field_dicts, "options")

    database_template = OPDatabaseItemTemplate(item_name,
                                               database_type=database_type,
                                               hostname=hostanme,
                                               port=port,
                                               database=database_name,
                                               username=username,
                                               password=password,
                                               sid=sid,
                                               alias=alias,
                                               options=options)
    assert database_template.sid == expected.sid


def test_new_database_item_080(valid_data: ValidData, expected_database_data: ExpectedDatabaseItemData):
    """
    Create:
        - database template from "example database 1"
    Verify:
        - alias template property matches expected value
    """
    item_dict = valid_data.data_for_name(VALID_DATABASE_1)
    field_dicts = item_dict["fields"]

    item_name = "Example Database 1"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)

    database_type = _valid_field_value_for_id(field_dicts, "database_type")
    hostanme = _valid_field_value_for_id(field_dicts, "hostname")
    port = _valid_field_value_for_id(field_dicts, "port")
    database_name = _valid_field_value_for_id(field_dicts, "database")
    username = _valid_field_value_for_id(field_dicts, "username")
    password = _valid_field_value_for_id(field_dicts, "password")
    sid = _valid_field_value_for_id(field_dicts, "sid")
    alias = _valid_field_value_for_id(field_dicts, "alias")
    options = _valid_field_value_for_id(field_dicts, "options")

    database_template = OPDatabaseItemTemplate(item_name,
                                               database_type=database_type,
                                               hostname=hostanme,
                                               port=port,
                                               database=database_name,
                                               username=username,
                                               password=password,
                                               sid=sid,
                                               alias=alias,
                                               options=options)
    assert database_template.alias == expected.alias


def test_new_database_item_090(valid_data: ValidData, expected_database_data: ExpectedDatabaseItemData):
    """
    Create:
        - database template from "example database 1"
    Verify:
        - options template property matches expected value
    """
    item_dict = valid_data.data_for_name(VALID_DATABASE_1)
    field_dicts = item_dict["fields"]

    item_name = "Example Database 1"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)

    database_type = _valid_field_value_for_id(field_dicts, "database_type")
    hostanme = _valid_field_value_for_id(field_dicts, "hostname")
    port = _valid_field_value_for_id(field_dicts, "port")
    database_name = _valid_field_value_for_id(field_dicts, "database")
    username = _valid_field_value_for_id(field_dicts, "username")
    password = _valid_field_value_for_id(field_dicts, "password")
    sid = _valid_field_value_for_id(field_dicts, "sid")
    alias = _valid_field_value_for_id(field_dicts, "alias")
    options = _valid_field_value_for_id(field_dicts, "options")

    database_template = OPDatabaseItemTemplate(item_name,
                                               database_type=database_type,
                                               hostname=hostanme,
                                               port=port,
                                               database=database_name,
                                               username=username,
                                               password=password,
                                               sid=sid,
                                               alias=alias,
                                               options=options)
    assert database_template.options == expected.options


def test_new_database_item_091(valid_data: ValidData, expected_database_data: ExpectedDatabaseItemData):
    """
    Create:
        - database template from "example database 1"
    Verify:
        - connection_options convenience property matches expected options value
    """
    item_dict = valid_data.data_for_name(VALID_DATABASE_1)
    field_dicts = item_dict["fields"]

    item_name = "Example Database 1"
    expected: ExpectedDatabaseItem = expected_database_data.data_for_database(
        item_name)

    database_type = _valid_field_value_for_id(field_dicts, "database_type")
    hostanme = _valid_field_value_for_id(field_dicts, "hostname")
    port = _valid_field_value_for_id(field_dicts, "port")
    database_name = _valid_field_value_for_id(field_dicts, "database")
    username = _valid_field_value_for_id(field_dicts, "username")
    password = _valid_field_value_for_id(field_dicts, "password")
    sid = _valid_field_value_for_id(field_dicts, "sid")
    alias = _valid_field_value_for_id(field_dicts, "alias")
    options = _valid_field_value_for_id(field_dicts, "options")

    database_template = OPDatabaseItemTemplate(item_name,
                                               database_type=database_type,
                                               hostname=hostanme,
                                               port=port,
                                               database=database_name,
                                               username=username,
                                               password=password,
                                               sid=sid,
                                               alias=alias,
                                               options=options)
    assert database_template.connection_options == expected.options


def test_new_database_item_100(valid_data: ValidData):
    """
    Create:
        - database template from "example database 2"
    Verify:
        - missing property values return None
        - sid
        - alias
        - options
    """
    item_dict = valid_data.data_for_name(VALID_DATABASE_2)
    field_dicts = item_dict["fields"]

    item_name = "Example Database 2"

    database_type = _valid_field_value_for_id(field_dicts, "database_type")
    hostanme = _valid_field_value_for_id(field_dicts, "hostname")
    port = _valid_field_value_for_id(field_dicts, "port")
    database_name = _valid_field_value_for_id(field_dicts, "database")
    username = _valid_field_value_for_id(field_dicts, "username")
    password = _valid_field_value_for_id(field_dicts, "password")

    database_template = OPDatabaseItemTemplate(item_name,
                                               database_type=database_type,
                                               hostname=hostanme,
                                               port=port,
                                               database=database_name,
                                               username=username,
                                               password=password)

    assert database_template.sid is None
    assert database_template.alias is None
    assert database_template.options is None


def test_new_database_item_temp_file_010():
    """
    Create:
        - An OPDatabaseItemTemplate object
        - request a secure temp file with the object serialized as JSON
        - release the new object
    Verify:
        - the temp file exists
        - the temp file has been deleted when the object is released
    """
    username = "test_username"
    title = "Test Database Item"

    database_template = OPDatabaseItemTemplate(title, username)
    temp_file_path = database_template.secure_tempfile()
    assert os.path.isfile(temp_file_path)

    database_template = None
    assert not os.path.exists(temp_file_path)


def test_new_database_item_temp_file_020():
    """
    Create:
        - An OPDatabaseItemTemplate object
        - request a secure temp file with the object serialized as JSON
        - delete the temp file from under the object
        - release the object
    Verify:
        - the temp file exists
        - no exception is raised when object is released
    """
    username = "test_username"
    title = "Test Database Item"

    database_template = OPDatabaseItemTemplate(title, username)
    temp_file_path = database_template.secure_tempfile()
    assert os.path.isfile(temp_file_path)

    # dirty trick; this shouldn't happen. But we need to be robust against it anyway
    os.remove(temp_file_path)
    try:
        database_template = None
    except Exception as e:
        assert False, f"new_login = None raised an exception {e}"


def test_new_database_item_tags_010(valid_data: ValidData):
    """
    Create:
        - An OPDatabaseItemTemplate object with two tags
    Verify:
        - the resulting object has the same two tags
    """
    item_dict = valid_data.data_for_name(VALID_DATABASE_1)
    field_dicts = item_dict["fields"]
    item_name = "Example Database 1"
    tags = ["tag_1", "tag_1"]

    database_type = _valid_field_value_for_id(field_dicts, "database_type")
    hostanme = _valid_field_value_for_id(field_dicts, "hostname")
    port = _valid_field_value_for_id(field_dicts, "port")
    database_name = _valid_field_value_for_id(field_dicts, "database")
    username = _valid_field_value_for_id(field_dicts, "username")
    password = _valid_field_value_for_id(field_dicts, "password")
    sid = _valid_field_value_for_id(field_dicts, "sid")
    alias = _valid_field_value_for_id(field_dicts, "alias")
    options = _valid_field_value_for_id(field_dicts, "options")

    database_template = OPDatabaseItemTemplate(item_name,
                                               database_type=database_type,
                                               hostname=hostanme,
                                               port=port,
                                               database=database_name,
                                               username=username,
                                               password=password,
                                               sid=sid,
                                               alias=alias,
                                               options=options,
                                               tags=tags)
    expected_tags = set(tags)
    actual_tags = set(database_template.tags)

    assert expected_tags == actual_tags


def test_new_database_item_tags_020(valid_data: ValidData):
    """
    Create:
        - An OPDatabaseItemTemplate object with two tags
    Verify:
        - the resulting object has the same two tags
    """
    item_dict = valid_data.data_for_name(VALID_DATABASE_1)
    field_dicts = item_dict["fields"]
    item_name = "Example Database 1"
    tags = ["tag_1", "tag_1"]

    database_type = _valid_field_value_for_id(field_dicts, "database_type")
    hostanme = _valid_field_value_for_id(field_dicts, "hostname")
    port = _valid_field_value_for_id(field_dicts, "port")
    database_name = _valid_field_value_for_id(field_dicts, "database")
    username = _valid_field_value_for_id(field_dicts, "username")
    password = _valid_field_value_for_id(field_dicts, "password")
    sid = _valid_field_value_for_id(field_dicts, "sid")
    alias = _valid_field_value_for_id(field_dicts, "alias")
    options = _valid_field_value_for_id(field_dicts, "options")

    database_template = OPDatabaseItemTemplate(item_name,
                                               database_type=database_type,
                                               hostname=hostanme,
                                               port=port,
                                               database=database_name,
                                               username=username,
                                               password=password,
                                               sid=sid,
                                               alias=alias,
                                               options=options,
                                               tags=tags)
    expected_tags = set(tags)
    actual_tags = set(database_template.tags)

    assert len(actual_tags) == 1
    assert expected_tags == actual_tags
